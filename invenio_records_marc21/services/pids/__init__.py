# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""PIDs module."""

from .datacite import Marc21DataCitePIDProvider
from .tasks import register_or_update_pid

__all__ = (
    "Marc21DataCitePIDProvider",
    "register_or_update_pid",
)
