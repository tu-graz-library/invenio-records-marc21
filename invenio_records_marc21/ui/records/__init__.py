# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Records user interface."""

from invenio_pidstore.errors import PIDDeletedError, PIDDoesNotExistError
from invenio_records_resources.services.errors import PermissionDeniedError

from .errors import (
    not_found_error,
    record_permission_denied_error,
    record_tombstone_error,
)
from .filters import personal_name, physical_description, pid_url, sanitize_title
from .records import (
    record_detail,
    record_export,
    record_file_download,
    record_file_preview,
)
from .searchapp import search_app_context


#
# Registration
#
def init_records_views(blueprint, app):
    """Register blueprint routes on app."""
    routes = app.config.get("MARC21_UI_ENDPOINTS")

    # Record URL rules
    blueprint.add_url_rule(
        routes["record-detail"],
        view_func=record_detail,
    )

    blueprint.add_url_rule(
        routes["record-export"],
        view_func=record_export,
    )

    blueprint.add_url_rule(routes["record_file_preview"], view_func=record_file_preview)

    blueprint.add_url_rule(
        routes["record_file_download"], view_func=record_file_download
    )

    # Register error handlers
    blueprint.register_error_handler(PIDDeletedError, record_tombstone_error)
    blueprint.register_error_handler(PIDDoesNotExistError, not_found_error)
    blueprint.register_error_handler(KeyError, not_found_error)
    blueprint.register_error_handler(
        PermissionDeniedError, record_permission_denied_error
    )

    # Register template filters
    blueprint.add_app_template_filter(pid_url)
    blueprint.add_app_template_filter(sanitize_title)
    blueprint.add_app_template_filter(personal_name)
    blueprint.add_app_template_filter(physical_description)

    # Register context processor
    blueprint.app_context_processor(search_app_context)

    return blueprint
