# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Theme Package."""


from flask_babelex import lazy_gettext as _
from flask_menu import current_menu

from .config import search_app_context
from .views import deposit_create, deposit_edit, index, search


#
# Registration
#
def init_theme_views(blueprint, app):
    """Blueprint for the routes and resources provided by Invenio-Records-Marc21."""
    routes = app.config.get("INVENIO_MARC21_UI_THEME_ENDPOINTS")

    blueprint.add_url_rule(routes["index"], view_func=index)
    blueprint.add_url_rule(routes["record-search"], view_func=search)
    blueprint.add_url_rule(routes["deposit-create"], view_func=deposit_create)
    blueprint.add_url_rule(routes["deposit-edit"], view_func=deposit_edit)

    blueprint.app_context_processor(search_app_context)

    return blueprint
