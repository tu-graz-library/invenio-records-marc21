# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Default configuration."""

from __future__ import absolute_import, print_function

import idutils
from celery.schedules import crontab
from flask_principal import RoleNeed
from invenio_i18n import lazy_gettext as _
from invenio_rdm_records.services import facets as rdm_facets
from invenio_rdm_records.services.pids import providers

from .resources.serializers.datacite import Marc21DataCite43JSONSerializer
from .services import facets
from .services.pids import Marc21DataCitePIDProvider

MARC21_FACETS = {
    "access_status": {
        "facet": rdm_facets.access_status,
        "ui": {
            "field": "access.status",
        },
    },
    "is_published": {
        "facet": facets.is_published,
        "ui": {
            "field": "is_published",
        },
    },
    "file_type": {
        "facet": facets.filetype,
        "ui": {
            "field": "files.types",
        },
    },
}

MARC21_SORT_OPTIONS = {
    "bestmatch": dict(
        title=_("Best match"),
        fields=["_score"],  # search defaults to desc on `_score` field
    ),
    "newest": dict(
        title=_("Newest"),
        fields=["-created"],
    ),
    "oldest": dict(
        title=_("Oldest"),
        fields=["created"],
    ),
    "version": dict(
        title=_("Version"),
        fields=["-versions.index"],
    ),
    "updated-desc": dict(
        title=_("Recently updated"),
        fields=["-updated"],
    ),
    "updated-asc": dict(
        title=_("Least recently updated"),
        fields=["updated"],
    ),
}

MARC21_SEARCH_DRAFTS = {
    "facets": ["access_status", "is_published", "file_type"],
    "sort": [
        "bestmatch",
        "newest",
        "oldest",
        "version",
    ],
}
"""User records search configuration (i.e. list of uploads)."""

MARC21_SEARCH = {
    "facets": ["access_status", "file_type"],
    "sort": [
        "bestmatch",
        "newest",
        "oldest",
        "version",
    ],
}
"""Record search configuration."""

MARC21_BASE_TEMPLATE = "invenio_records_marc21/base.html"

MARC21_REST_ENDPOINTS = {}
"""REST API for invenio-records-marc21."""

MARC21_RECORD_EXPORTERS = {
    "json": {
        "name": "JSON",
        "serializer": (
            "invenio_records_marc21.resources.serializers:" "Marc21JSONSerializer"
        ),
        "filename": "{id}.json",
    },
    "marcxml": {
        "name": "MARCXML",
        "serializer": (
            "invenio_records_marc21.resources.serializers:" "Marc21XMLSerializer"
        ),
        "filename": "{id}.xml",
    },
}
"""Marc21 Record export serializers."""

MARC21_RECORD_EXPORTER_OPTIONS = {
    "indent": 4,
    "sort_keys": True,
}
"""Marc21 Record export options."""

MARC21_UI_ENDPOINTS = {
    "record-detail": "/<pid_value>",
    "record-export": "/<pid_value>/export/<export_format>",
    "record_file_preview": "marc21/<pid_value>/preview/<path:filename>",
    "record_file_download": "marc21/<pid_value>/files/<path:filename>",
}
"""Marc21 Record ui endpoints."""

MARC21_UI_THEME_ENDPOINTS = {
    "index": "/",
    "record-search": "/search",
    "uploads-marc21": "/uploads",
    "deposit-create": "/uploads/new",
    "deposit-edit": "/uploads/<pid_value>",
}
"""Records UI for invenio-records-marc21."""

SEARCH_UI_JSTEMPLATE_RESULTS = "templates/invenio_records_marc21/search/results.html"
"""Result list template."""

MARC21_ENDPOINTS_ENABLED = True
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


#
# Persistent identifiers configuration
#
MARC21_PERSISTENT_IDENTIFIER_PROVIDERS = [
    # DataCite DOI provider
    Marc21DataCitePIDProvider(
        "datacite",
        client=providers.DataCiteClient("datacite", config_prefix="DATACITE"),
        pid_type="doi",
        serializer=Marc21DataCite43JSONSerializer(),
        label=_("DOI"),
    ),
    # DOI provider for externally managed DOIs
    providers.ExternalPIDProvider(
        "external",
        "doi",
        validators=[providers.BlockedPrefixes(config_names=["DATACITE_PREFIX"])],
        label=_("DOI"),
    ),
]
"""A list of configured persistent identifier providers.

ATTENTION: All providers (and clients) takes a name as the first parameter.
This name is stored in the database and used in the REST API in order to
identify the given provider and client.

The name is further used to configure the desired persistent identifiers (see
``MARC21_PERSISTENT_IDENTIFIER_PROVIDERS`` below)
"""


MARC21_IDENTIFIERS_SCHEMES = {
    "doi": {"label": _("DOI"), "validator": idutils.is_doi, "datacite": "DOI"},
}
"""These are used for main, alternate and related identifiers."""

MARC21_PERSISTENT_IDENTIFIERS = {
    "doi": {
        "providers": ["datacite", "external"],
        "required": True,
        "label": _("DOI"),
        "validator": idutils.is_doi,
        "normalizer": idutils.normalize_doi,
    },
}
"""The configured persistent identifiers for records.

.. code-block:: python

    "<scheme>": {
        "providers": ["<default-provider-name>", "<provider-name>", ...],
        "required": True/False,
    }
"""


MARC21_API_HEADERS = {
    "vnd+json": {
        "Content-Type": "application/json",
        "Accept": "application/vnd.inveniomarc21.v1+marcxml",
    },
}
"""The api headers for the RDM deposit app."""

MARC21_DEFAULT_FILES_ENABLED = True
"""Marc21 deposit page files enabled value on new records."""

# Configuration for the DataCiteClient used by the DataCitePIDProvider
# Configuration may come from RDM records module
DATACITE_ENABLED = False
"""Flag to enable/disable DOI registration."""


DATACITE_USERNAME = ""
"""DataCite username."""


DATACITE_PASSWORD = ""
"""DataCite password."""


DATACITE_PREFIX = ""
"""DataCite DOI prefix."""


DATACITE_TEST_MODE = True
"""DataCite test mode enabled."""


DATACITE_FORMAT = "{prefix}/{id}"
"""A string used for formatting the DOI or a callable.

If set to a string, you can used ``{prefix}`` and ``{id}`` inside the string.

You can also provide a callable instead:

.. code-block:: python

    def make_doi(prefix, record):
        return f"{prefix}/{record.pid.pid_value}"

    DATACITE_FORMAT = make_doi
"""

MARC21_RECORD_MANAGER_NEEDS = [RoleNeed("Marc21Manager")]
"""This Role has the most powerfull below of the admin. It will have create/modify/delete permissions."""

MARC21_RECORD_CURATOR_NEEDS = [RoleNeed("Marc21Curator")]
"""This Role is to modify records only, no creation, no deletion possible."""
