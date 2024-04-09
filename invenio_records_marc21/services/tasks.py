# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Celery tasks."""

from datetime import datetime, timedelta
from functools import partial

import arrow
from celery import shared_task
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_search.engine import dsl
from invenio_search.proxies import current_search_client
from invenio_search.utils import prefix_index
from invenio_stats.bookmark import BookmarkAPI

from ..proxies import current_records_marc21
from .errors import EmbargoNotLiftedError


@shared_task(ignore_result=True)
def update_expired_embargos():
    """Release expired embargoes."""
    service = current_records_marc21.records_service
    embargoed_q = (
        "access.embargo.active:true AND access.embargo.until:"
        f"{{* TO {arrow.utcnow().datetime.strftime('%Y-%m-%d')}}}"
    )

    restricted_records = service.scan(identity=system_identity, q=embargoed_q)
    for restricted_record in restricted_records.hits:
        try:
            service.lift_embargo(_id=restricted_record["id"], identity=system_identity)
        except EmbargoNotLiftedError:
            current_app.logger.warning(
                "Embargo from record with id"
                f" {restricted_record['id']} was not"
                " lifted"
            )
            continue


@shared_task(ignore_result=True)
def marc21_reindex_stats(stats_indices):
    """Reindex the documents where the stats have changed."""
    bm = BookmarkAPI(current_search_client, "marc21_stats_reindex", "day")
    last_run = bm.get_bookmark()
    if not last_run:
        # If this is the first time that we run, let's do it for the documents of the last week
        last_run = (datetime.utcnow() - timedelta(days=7)).isoformat()
    reindex_start_time = datetime.utcnow().isoformat()
    indices = ",".join(map(lambda x: prefix_index(x) + "*", stats_indices))

    all_parents = set()
    query = dsl.Search(
        using=current_search_client,
        index=indices,
    ).filter({"range": {"updated_timestamp": {"gte": last_run}}})

    for result in query.scan():
        parent_id = result.parent_recid
        all_parents.add(parent_id)

    if all_parents:
        all_parents_list = list(all_parents)
        step = 10000
        end = len(list(all_parents))
        for i in range(0, end, step):
            records_q = dsl.Q("terms", parent__id=all_parents_list[i : i + step])
            current_records_marc21.record_service.reindex(
                params={"allversions": True},
                identity=system_identity,
                search_query=records_q,
            )
    bm.set_bookmark(reindex_start_time)
    return "%d documents reindexed" % len(all_parents)
