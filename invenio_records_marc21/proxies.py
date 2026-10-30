# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Helper proxy to the state object."""

from typing import TYPE_CHECKING, cast

from flask import current_app
from werkzeug.local import LocalProxy

if TYPE_CHECKING:
    from .ext import InvenioRecordsMARC21

current_records_marc21: InvenioRecordsMARC21 = cast(
    "InvenioRecordsMARC21",
    LocalProxy(
        lambda: current_app.extensions["invenio-records-marc21"],
    ),
)
"""Helper proxy to get the current records marc21 extension."""
