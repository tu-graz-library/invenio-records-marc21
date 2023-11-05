# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Records user interface."""

from flask import Blueprint

from .records import init_records_views
from .theme import init_theme_views


#
# Registration
#
def create_blueprint(app):
    """Register blueprint routes on app."""
    blueprint = Blueprint(
        "invenio_records_marc21",
        __name__,
        template_folder="../templates",
        url_prefix="/publications",
    )

    blueprint = init_theme_views(blueprint, app)
    blueprint = init_records_views(blueprint, app)
    return blueprint
