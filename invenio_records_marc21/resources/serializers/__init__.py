# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record serializers."""

from __future__ import absolute_import, print_function

from .datacite import Marc21DataCite43JSONSerializer
from .deposit import Marc21DepositSerializer
from .dublin_core import Marc21ToDublinCoreJSONSerializer
from .errors import Marc21XMLConvertError
from .marcxml import Marc21XMLSerializer
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
)
