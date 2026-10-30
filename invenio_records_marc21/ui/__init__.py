# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
