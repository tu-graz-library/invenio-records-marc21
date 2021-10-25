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

from .views import index, search


#
# Registration
#
def init_theme_views(blueprint, app):
    """Blueprint for the routes and resources provided by Invenio-Records-Marc21."""
    routes = app.config.get("INVENIO_MARC21_UI_THEME_ENDPOINTS")

    blueprint.add_url_rule(routes["index"], view_func=index)
    blueprint.add_url_rule(routes["record-search"], view_func=search)

    return blueprint
