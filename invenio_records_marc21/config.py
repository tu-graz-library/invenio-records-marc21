# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from celery.schedules import crontab

INVENIO_MARC21_BASE_TEMPLATE = "invenio_records_marc21/base.html"

INVENIO_MARC21_REST_ENDPOINTS = {}
"""REST API for invenio-records-marc21."""

INVENIO_MARC21_RECORD_EXPORTERS = {
    "json": {
        "name": "JSON",
        "serializer": (
            "invenio_records_marc21.resources.serializers:" "Marc21JSONSerializer"
        ),
    },
    "marcxml": {
        "name": "MARCXML",
        "serializer": (
            "invenio_records_marc21.resources.serializers:" "Marc21XMLSerializer"
        ),
    },
}
"""Marc21 Record export serializers."""

INVENIO_MARC21_RECORD_EXPORTER_OPTIONS = {
    "indent": 4,
    "sort_keys": True,
}
"""Marc21 Record export options."""

INVENIO_MARC21_UI_ENDPOINTS = {
    "record-detail": "/<pid_value>",
    "record-export": "/<pid_value>/export/<export_format>",
    "record_file_preview": "marc21/<pid_value>/preview/<path:filename>",
    "record_file_download": "marc21/<pid_value>/files/<path:filename>",
}
"""Marc21 Record ui endpoints."""

INVENIO_MARC21_UI_THEME_ENDPOINTS = {
    "index": "/",
    "record-search": "/search",
}
"""Records UI for invenio-records-marc21."""

SEARCH_UI_JSTEMPLATE_RESULTS = "templates/invenio_records_marc21/results.html"
"""Result list template."""

INVENIO_MARC21_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""

CELERY_BEAT_SCHEDULE = {
    "marc21_service_embargo_lift": {
        "task": "invenio_records_marc21.services.tasks.update_expired_embargos",
        "schedule": crontab(
            minute="5",
            hour="0",
        ),
    },
}
"""Celery tasks for the module."""
