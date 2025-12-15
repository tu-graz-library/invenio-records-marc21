# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Marc21 module to create REST APIs."""

from .config import Marc21TemplateServiceConfig
from .service import Marc21TemplateService

__all__ = (
    "Marc21TemplateService",
    "Marc21TemplateServiceConfig",
)
