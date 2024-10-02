# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Flask extension for Invenio-Records-Marc21."""

from __future__ import absolute_import, print_function

from flask_menu import current_menu
from invenio_i18n import lazy_gettext as _
from invenio_rdm_records.services.pids import PIDManager, PIDsService
from invenio_records_resources.resources import FileResource
from invenio_records_resources.services import FileService

from . import config
from .resources import (
    Marc21DraftFilesResourceConfig,
    Marc21ParentRecordLinksResource,
    Marc21ParentRecordLinksResourceConfig,
    Marc21RecordFilesResourceConfig,
    Marc21RecordResource,
    Marc21RecordResourceConfig,
)
from .services import (
    Marc21DraftFilesServiceConfig,
    Marc21RecordFilesServiceConfig,
    Marc21RecordService,
    Marc21RecordServiceConfig,
)
from .system import Marc21TemplateConfig, Marc21TemplateService
from .ui.theme import current_identity_can_view


class InvenioRecordsMARC21(object):
    """Invenio-Records-Marc21 extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        self.init_resources(app)
        app.extensions["invenio-records-marc21"] = self

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        with_endpoints = app.config.get("MARC21_ENDPOINTS_ENABLED", True)
        for k in dir(config):
            if k.startswith("MARC21_") or k.startswith("DATACITE_"):
                app.config.setdefault(k, getattr(config, k))
            elif k == "SEARCH_UI_JSTEMPLATE_RESULTS":
                app.config["SEARCH_UI_JSTEMPLATE_RESULTS"] = getattr(config, k)
            elif k == "CELERY_BEAT_SCHEDULE":
                if "CELERY_BEAT_SCHEDULE" in app.config:
                    app.config["CELERY_BEAT_SCHEDULE"].update(getattr(config, k))
                else:
                    app.config.setdefault(k, getattr(config, k))
            else:
                for n in [
                    "MARC21_REST_ENDPOINTS",
                    "MARC21_UI_ENDPOINTS",
                ]:
                    if k == n and with_endpoints:
                        app.config.setdefault(n, {})
                        app.config[n].update(getattr(config, k))

    def service_configs(self, app):
        """Customized service configs."""

        class ServiceConfigs:
            record = Marc21RecordServiceConfig.build(app)
            file = Marc21RecordFilesServiceConfig.build(app)
            file_draft = Marc21DraftFilesServiceConfig.build(app)

        return ServiceConfigs

    def init_services(self, app):
        """Initialize services."""
        service_config = self.service_configs(app)

        self.records_service = Marc21RecordService(
            config=service_config.record,
            files_service=FileService(service_config.file),
            draft_files_service=FileService(service_config.file_draft),
            pids_service=PIDsService(service_config.record, PIDManager),
        )
        self.templates_service = Marc21TemplateService(
            config=Marc21TemplateConfig,
        )

    def init_resources(self, app):
        """Initialize resources."""
        self.record_resource = Marc21RecordResource(
            service=self.records_service,
            config=Marc21RecordResourceConfig,
        )

        self.record_files_resource = FileResource(
            service=self.records_service.files, config=Marc21RecordFilesResourceConfig
        )

        self.draft_files_resource = FileResource(
            service=self.records_service.draft_files,
            config=Marc21DraftFilesResourceConfig,
        )

        self.parent_record_links_resource = Marc21ParentRecordLinksResource(
            service=self.records_service, config=Marc21ParentRecordLinksResourceConfig
        )


def finalize_app(app) -> None:
    """Finalize app."""
    init(app)
    register_marc21_dashboard_tab()


def api_finalize_app(app) -> None:
    """Finalize app for api."""
    init(app)


def init(app):
    """Init app."""
    # Register services - cannot be done in extension because
    # Invenio-Records-Resources might not have been initialized.

    ext = app.extensions["invenio-records-marc21"]
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.records_service, service_id="marc21-records")
    sregistry.register(ext.records_service.files, service_id="marc21-files")
    sregistry.register(ext.records_service.draft_files, service_id="marc21-draft-files")

    iregistry = app.extensions["invenio-indexer"].registry
    iregistry.register(ext.records_service.indexer, indexer_id="marc21-records")
    iregistry.register(
        ext.records_service.draft_indexer, indexer_id="marc21-records-drafts"
    )


def register_marc21_dashboard_tab():
    """Register entry for marc21 in the `flask_menu`-submenu "dashboard"."""
    user_dashboard_menu = current_menu.submenu("dashboard")
    user_dashboard_menu.submenu("Publications").register(
        "invenio_records_marc21.uploads_marc21",
        text=_("Publications"),
        order=4,
        visible_when=current_identity_can_view,
    )
