# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2019 CERN.
# Copyright (C) 2022 TU Wien.
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permission factories for invenio-records-marc21.

In contrast to the very liberal defaults provided by Invenio-Stats, these permission
factories deny access unless otherwise specified.
"""

from flask import current_app
from invenio_stats.proxies import current_stats


class Marc21Statistics:
    """Statistics API class."""

    prefix = "marc21-record"

    @classmethod
    def _get_query(cls, query_name):
        """Build the statistics query from configuration."""
        query_config = current_stats.queries[query_name]
        return query_config.cls(name=query_config.name, **query_config.params)

    @classmethod
    def get_record_stats(cls, recid, parent_recid):
        """Fetch the statistics for the given record."""
        try:
            views = cls._get_query(f"{cls.prefix}-view").run(recid=recid)
            views_all = cls._get_query(f"{cls.prefix}-view-all-versions").run(
                parent_recid=parent_recid
            )
        except Exception as e:
            # e.g. opensearchpy.exceptions.NotFoundError
            # when the aggregation search index hasn't been created yet
            current_app.logger.warning(e)

            fallback_result = {
                "views": 0,
                "unique_views": 0,
            }
            views = views_all = downloads = downloads_all = fallback_result

        try:
            downloads = cls._get_query(f"{cls.prefix}-download").run(recid=recid)
            downloads_all = cls._get_query(f"{cls.prefix}-download-all-versions").run(
                parent_recid=parent_recid
            )
        except Exception as e:
            # same as above, but for failure in the download statistics
            # because they are a separate index that can fail independently
            current_app.logger.warning(e)

            fallback_result = {
                "downloads": 0,
                "unique_downloads": 0,
                "data_volume": 0,
            }
            downloads = downloads_all = fallback_result

        stats = {
            "this_version": {
                "views": views["views"],
                "unique_views": views["unique_views"],
                "downloads": downloads["downloads"],
                "unique_downloads": downloads["unique_downloads"],
                "data_volume": downloads["data_volume"],
            },
            "all_versions": {
                "views": views_all["views"],
                "unique_views": views_all["unique_views"],
                "downloads": downloads_all["downloads"],
                "unique_downloads": downloads_all["unique_downloads"],
                "data_volume": downloads_all["data_volume"],
            },
        }

        return stats
