# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Resource type field."""

from enum import Enum


class ResourceTypeEnum(Enum):
    """Enum defining resource type."""

    HSMASTER = "HS-MASTER"

    HSDISS = "HS-DISS"
