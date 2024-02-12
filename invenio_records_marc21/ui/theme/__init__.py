# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Theme Package."""

from flask import g
from flask_menu import current_menu
from invenio_i18n import lazy_gettext as _

from ...proxies import current_records_marc21
from .views import deposit_create, deposit_edit, index, search, uploads_marc21


#
# Registration
#
def current_identity_can_view() -> bool:
    """Checks whether current identity has viewing rights."""
    service = current_records_marc21.records_service
    return service.check_permission(g.identity, "view")


def init_theme_views(blueprint, app):
    """Blueprint for the routes and resources provided by Invenio-Records-Marc21."""
    routes = app.config.get("MARC21_UI_THEME_ENDPOINTS")

    blueprint.add_url_rule(routes["index"], view_func=index)

    blueprint.add_url_rule(routes["uploads-marc21"], view_func=uploads_marc21)
    blueprint.add_url_rule(routes["record-search"], view_func=search)
    blueprint.add_url_rule(routes["deposit-create"], view_func=deposit_create)
    blueprint.add_url_rule(routes["deposit-edit"], view_func=deposit_edit)

    # TODO: Fix this after inveniosoftware/invenio-base#171 has been solved
    @blueprint.before_app_first_request
    def register_marc21_dashboard():
        """Register entry for marc21 in the `flask_menu`-submenu "dashboard"."""
        user_dashboard_menu = current_menu.submenu("dashboard")
        user_dashboard_menu.submenu("Publications").register(
            "invenio_records_marc21.uploads_marc21",
            text=_("Publications"),
            order=4,
            visible_when=current_identity_can_view,
        )

    return blueprint
