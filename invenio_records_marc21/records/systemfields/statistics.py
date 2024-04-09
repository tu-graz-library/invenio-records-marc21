# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 TU Wien.
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Cached transient field for record statistics."""

from invenio_rdm_records.records.systemfields import RecordStatisticsField
from invenio_search.proxies import current_search_client
from invenio_search.utils import build_alias_name

from ..statistics import Marc21Statistics


class Marc21RecordStatisticsField(RecordStatisticsField):
    """Field for lazy fetching and caching (but not storing) of tugraz record statistics."""

    api = Marc21Statistics
    """"""

    def _get_record_stats(self, record):
        """Get the record's statistics from either record or aggregation index."""
        stats = None
        recid, parent_recid = record["id"], record.parent["id"]

        try:
            # for more consistency between search results and each record's details,
            # we try to get the statistics from the record's search index first
            # note: this field is dumped into the record's data before indexing
            #       by the search dumper extension "StatisticsDumperExt"
            res = current_search_client.get(
                index=build_alias_name(record.index._name),
                id=record.id,
                params={"_source_includes": "stats"},
            )
            stats = res["_source"]["stats"]
        except Exception:
            stats = None

        # as a fallback, use the more up-to-date aggregations indices
        return stats or self.api.get_record_stats(
            recid=recid, parent_recid=parent_recid
        )
