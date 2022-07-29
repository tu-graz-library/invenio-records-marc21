# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-records-lom is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Configuration helper for React-SearchKit."""

from functools import partial

from flask import current_app
from invenio_search_ui.searchconfig import search_app_config


def search_app_context():
    """Search app context processor."""
    return {
        "search_app_marc21_config": partial(
            search_app_config,
            "INVENIO_MARC21_SEARCH",
            current_app.config["INVENIO_MARC21_FACETS"],
            current_app.config["INVENIO_MARC21_SORT_OPTIONS"],
            "/api/marc21",
            {"Accept": "application/vnd.inveniomarc21.v1+json"},
        )
    }
