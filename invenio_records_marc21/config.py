# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Default configuration."""

from __future__ import absolute_import, print_function

import idutils
from celery.schedules import crontab, timedelta
from flask_principal import RoleNeed
from invenio_i18n import lazy_gettext as _
from invenio_rdm_records.services import facets as rdm_facets
from invenio_rdm_records.services.pids import providers
from invenio_stats.aggregations import StatAggregator
from invenio_stats.contrib.event_builders import build_file_unique_id
from invenio_stats.processors import EventsIndexer, anonymize_user, flag_robots
from invenio_stats.queries import TermsQuery

from .resources.serializers.datacite import Marc21DataCite43JSONSerializer
from .services import facets
from .services.pids import Marc21DataCitePIDProvider
from .utils import build_record_unique_id

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
    "resource_type": {
        "facet": facets.resource_type,
        "ui": {
            "field": "metadata.resource_type",
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
    "mostviewed": dict(
        title=_("Most viewed"), fields=["-stats.all_versions.unique_views"]
    ),
    "mostdownloaded": dict(
        title=_("Most downloaded"), fields=["-stats.all_versions.unique_downloads"]
    ),
}

MARC21_SEARCH_DRAFTS = {
    "facets": [
        "resource_type",
        "access_status",
        "is_published",
    ],
    "sort": [
        "bestmatch",
        "newest",
        "oldest",
        "version",
    ],
}
"""User records search configuration (i.e. list of uploads)."""

MARC21_SEARCH = {
    "facets": [
        "resource_type",
        "access_status",
    ],
    "sort": [
        "bestmatch",
        "newest",
        "oldest",
        "version",
        "mostviewed",
        "mostdownloaded",
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
        "params": {"options": {"indent": 4, "sort_keys": True}},
        "filename": "{id}.json",
    },
    "marcxml": {
        "name": "MARCXML",
        "serializer": (
            "invenio_records_marc21.resources.serializers:" "Marc21XMLSerializer"
        ),
        "params": {},
        "filename": "{id}.xml",
    },
}
"""Marc21 Record export serializers."""

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
        "Accept": "application/vnd.inveniomarc21.v1+json",
    },
    "octet-stream": {"Content-Type": "application/octet-stream"},
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

MARC21_RECORD_CREATOR_NEEDS = [RoleNeed("Marc21Creator")]
"""This Role is here to create and modify records, no publish allowed."""


# Statistics configuration

MARC21_STATS_CELERY_TASKS = {
    # indexing of statistics events & aggregations
    "marc21-stats-process-events": {
        "task": "invenio_stats.tasks.process_events",
        "args": [("marc21-record-view", "marc21-file-download")],
        "schedule": crontab(
            minute="20,50",
        ),  # Every hour at minute 20 and 50
    },
    "marc21-stats-aggregate-events": {
        "task": "invenio_stats.tasks.aggregate_events",
        "args": [
            (
                "marc21-record-view-agg",
                "marc21-file-download-agg",
            )
        ],
        "schedule": crontab(minute="5"),  # Every hour at minute 5
    },
    "marc21-reindex-stats": {
        "task": "invenio_records_marc21.services.tasks.marc21_reindex_stats",
        "args": [
            (
                "stats-marc21-record-view",
                "stats-marc21-file-download",
            )
        ],
        "schedule": crontab(minute="10"),
    },
}

# Invenio-Stats
# =============
# See https://invenio-stats.readthedocs.io/en/latest/configuration.html

MARC21_STATS_EVENTS = {
    "marc21-file-download": {
        "templates": "invenio_records_marc21.records.statistics.templates.events.marc21_file_download",
        "event_builders": [
            "invenio_rdm_records.resources.stats.file_download_event_builder",
            "invenio_rdm_records.resources.stats.check_if_via_api",
        ],
        "cls": EventsIndexer,
        "params": {
            "preprocessors": [flag_robots, anonymize_user, build_file_unique_id]
        },
    },
    "marc21-record-view": {
        "templates": "invenio_records_marc21.records.statistics.templates.events.marc21_record_view",
        "event_builders": [
            "invenio_rdm_records.resources.stats.record_view_event_builder",
            "invenio_rdm_records.resources.stats.check_if_via_api",
            "invenio_rdm_records.resources.stats.drop_if_via_api",
        ],
        "cls": EventsIndexer,
        "params": {
            "preprocessors": [flag_robots, anonymize_user, build_record_unique_id],
        },
    },
}

MARC21_STATS_AGGREGATIONS = {
    "marc21-file-download-agg": {
        "templates": "invenio_records_marc21.records.statistics.templates.aggregations.aggr_marc21_file_download",
        "cls": StatAggregator,
        "params": {
            "event": "marc21-file-download",
            "field": "unique_id",
            "interval": "day",
            "index_interval": "month",
            "copy_fields": {
                "file_id": "file_id",
                "file_key": "file_key",
                "bucket_id": "bucket_id",
                "recid": "recid",
                "parent_recid": "parent_recid",
            },
            "metric_fields": {
                "unique_count": (
                    "cardinality",
                    "unique_session_id",
                    {"precision_threshold": 1000},
                ),
                "volume": ("sum", "size", {}),
            },
        },
    },
    "marc21-record-view-agg": {
        "templates": "invenio_records_marc21.records.statistics.templates.aggregations.aggr_marc21_record_view",
        "cls": StatAggregator,
        "params": {
            "event": "marc21-record-view",
            "field": "unique_id",
            "interval": "day",
            "index_interval": "month",
            "copy_fields": {
                "recid": "recid",
                "parent_recid": "parent_recid",
                "via_api": "via_api",
            },
            "metric_fields": {
                "unique_count": (
                    "cardinality",
                    "unique_session_id",
                    {"precision_threshold": 1000},
                ),
            },
            "query_modifiers": [lambda query, **_: query.filter("term", via_api=False)],
        },
    },
}

MARC21_STATS_QUERIES = {
    "marc21-record-view": {
        "cls": TermsQuery,
        "permission_factory": None,
        "params": {
            "index": "stats-marc21-record-view",
            "doc_type": "marc21-record-view-day-aggregation",
            "copy_fields": {
                "recid": "recid",
                "parent_recid": "parent_recid",
            },
            "query_modifiers": [],
            "required_filters": {
                "recid": "recid",
            },
            "metric_fields": {
                "views": ("sum", "count", {}),
                "unique_views": ("sum", "unique_count", {}),
            },
        },
    },
    "marc21-record-view-all-versions": {
        "cls": TermsQuery,
        "permission_factory": None,
        "params": {
            "index": "stats-marc21-record-view",
            "doc_type": "marc21-record-view-day-aggregation",
            "copy_fields": {
                "parent_recid": "parent_recid",
            },
            "query_modifiers": [],
            "required_filters": {
                "parent_recid": "parent_recid",
            },
            "metric_fields": {
                "views": ("sum", "count", {}),
                "unique_views": ("sum", "unique_count", {}),
            },
        },
    },
    "marc21-record-download": {
        "cls": TermsQuery,
        "permission_factory": None,
        "params": {
            "index": "stats-marc21-file-download",
            "doc_type": "marc21-file-download-day-aggregation",
            "copy_fields": {
                "recid": "recid",
                "parent_recid": "parent_recid",
            },
            "query_modifiers": [],
            "required_filters": {
                "recid": "recid",
            },
            "metric_fields": {
                "downloads": ("sum", "count", {}),
                "unique_downloads": ("sum", "unique_count", {}),
                "data_volume": ("sum", "volume", {}),
            },
        },
    },
    "marc21-record-download-all-versions": {
        "cls": TermsQuery,
        "permission_factory": None,
        "params": {
            "index": "stats-marc21-file-download",
            "doc_type": "marc21-file-download-day-aggregation",
            "copy_fields": {
                "parent_recid": "parent_recid",
            },
            "query_modifiers": [],
            "required_filters": {
                "parent_recid": "parent_recid",
            },
            "metric_fields": {
                "downloads": ("sum", "count", {}),
                "unique_downloads": ("sum", "unique_count", {}),
                "data_volume": ("sum", "volume", {}),
            },
        },
    },
}
