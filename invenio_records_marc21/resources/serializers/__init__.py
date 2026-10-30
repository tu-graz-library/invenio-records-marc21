# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Record serializers."""

from __future__ import absolute_import, print_function

from .datacite import Marc21DataCite43JSONSerializer
from .deposit import Marc21DepositSerializer
from .dublin_core import (
    Marc21ToDublinCoreJSONSerializer,
    Marc21ToDublinCoreXMLSerializer,
)
from .errors import Marc21XMLConvertError
from .marcxml import Marc21OAIXMLSerializer, Marc21XMLSerializer
from .serializer import Marc21BASESerializer, Marc21JSONSerializer
from .ui import Marc21UIJSONSerializer

__all__ = (
    "Marc21DataCite43JSONSerializer",
    "Marc21ToDublinCoreJSONSerializer",
    "Marc21XMLConvertError",
    "Marc21BASESerializer",
    "Marc21JSONSerializer",
    "Marc21XMLSerializer",
    "Marc21UIJSONSerializer",
    "Marc21DepositSerializer",
    "Marc21ToDublinCoreXMLSerializer",
    "Marc21OAIXMLSerializer",
)
