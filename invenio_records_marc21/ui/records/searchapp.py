# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Configuration helper for React-SearchKit."""

from functools import partial

from flask import current_app
from invenio_search_ui.searchconfig import search_app_config


def search_app_context():
    """Marc21 Search app context processor."""
    return {
        "search_app_marc21_config": partial(
            search_app_config,
            "MARC21_SEARCH",
            current_app.config["MARC21_FACETS"],
            current_app.config["MARC21_SORT_OPTIONS"],
            "/api/publications",
            {"Accept": "application/vnd.inveniomarc21.v1+json"},
            app_id="Marc21Records.Search",  # unique id to distinguish amongst search-apps
        ),
        "search_app_marc21_user_uploads_config": partial(
            search_app_config,
            "MARC21_SEARCH_DRAFTS",
            current_app.config["MARC21_FACETS"],
            current_app.config["MARC21_SORT_OPTIONS"],
            "/api/user/publications",
            {"Accept": "application/vnd.inveniomarc21.v1+json"},
            # initial_filters=[["is_published", "false"]],
            app_id="Marc21Records.DashboardSearch",  # unique id to distinguish amongst search-apps
        ),
    }
