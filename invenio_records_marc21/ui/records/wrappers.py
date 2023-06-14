# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Records string wrapper."""

from invenio_i18n import gettext as _

PERSONAL_CODES = {
    "aut": _("Author"),
    "aud": _("Author of dialog"),
    "act": _("Actor"),
    "arc": _("Architect"),
    "bkp": _("Book producer"),
    "cre": _("Creator"),
    "cur": _("Curator"),
}


def get_personal_code(code):
    """Getter function for personal codes."""
    return PERSONAL_CODES.get(code, code)
