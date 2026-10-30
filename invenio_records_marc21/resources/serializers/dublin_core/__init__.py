# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Dublin Core Serializer for Invenio Marc21 Records."""

from .serializer import (
    Marc21ToDublinCoreJSONSerializer,
    Marc21ToDublinCoreXMLSerializer,
)

__all__ = (
    "Marc21ToDublinCoreJSONSerializer",
    "Marc21ToDublinCoreXMLSerializer",
)
