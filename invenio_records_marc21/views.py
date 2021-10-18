# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Blueprint definitions."""

from flask import Blueprint

blueprint = Blueprint("invenio_records_marc21_ext", __name__)


@blueprint.record_once
def init(state):
    """Init app."""
    app = state.app
    # Register services - cannot be done in extension because
    # Invenio-Records-Resources might not have been initialized.
    registry = app.extensions["invenio-records-resources"].registry
    ext = app.extensions["invenio-records-marc21"]
    registry.register(ext.records_service, service_id="marc21-records")
    registry.register(ext.records_service.files, service_id="marc21-files")
    registry.register(ext.records_service.draft_files, service_id="marc21-draft-files")


def create_record_bp(app):
    """Create records blueprint."""
    ext = app.extensions["invenio-records-marc21"]
    return ext.record_resource.as_blueprint()


def create_record_files_bp(app):
    """Create records files blueprint."""
    ext = app.extensions["invenio-records-marc21"]
    return ext.record_files_resource.as_blueprint()


def create_draft_files_bp(app):
    """Create draft files blueprint."""
    ext = app.extensions["invenio-records-marc21"]
    return ext.draft_files_resource.as_blueprint()


def create_parent_record_links_bp(app):
    """Create parent record links blueprint."""
    ext = app.extensions["invenio-records-marc21"]
    return ext.parent_record_links_resource.as_blueprint()
