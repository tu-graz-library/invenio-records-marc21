# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Routes for record-related pages provided by Invenio-Records-Marc21."""

from functools import wraps

from flask import g
from invenio_records_resources.services.errors import PermissionDeniedError

from ...proxies import current_records_marc21


def links_config():
    """Get the record links config."""
    return current_records_marc21.record_resource.config.links_config


def draft_links_config():
    """Get the drafts links config."""
    return current_records_marc21.record_resource.config.draft_links_config


def files_service():
    """Get the record files service."""
    return current_records_marc21.records_service.files


def draft_files_service():
    """Get the record files service."""
    return current_records_marc21.records_service.draft_files


def service():
    """Get the record service."""
    return current_records_marc21.records_service


def pass_draft(f):
    """Decorator to retrieve the draft using the record service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")
        draft = service().read_draft(id_=pid_value, identity=g.identity)
        kwargs["draft"] = draft
        return f(**kwargs)

    return view


def pass_draft_files(f):
    """Decorate a view to pass a draft's files using the files service."""

    @wraps(f)
    def view(**kwargs):
        try:
            pid_value = kwargs.get("pid_value")
            files = draft_files_service().list_files(id_=pid_value, identity=g.identity)
            kwargs["draft_files"] = files

        except PermissionDeniedError:
            # this is handled here because we don't want a 404 on the landing
            # page when a user is allowed to read the metadata but not the
            # files
            kwargs["draft_files"] = None

        return f(**kwargs)

    return view
