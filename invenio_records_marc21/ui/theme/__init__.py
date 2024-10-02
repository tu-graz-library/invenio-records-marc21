# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Theme Package."""

from flask import g

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

    return blueprint
