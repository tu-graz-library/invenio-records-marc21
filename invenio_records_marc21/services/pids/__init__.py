# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""PIDs module."""

from .datacite import Marc21DataCitePIDProvider
from .tasks import register_or_update_pid

__all__ = (
    "Marc21DataCitePIDProvider",
    "register_or_update_pid",
)
