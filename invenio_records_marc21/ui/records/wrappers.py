# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
