# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio Marc21 module to create REST APIs."""

from .config import Marc21TemplateServiceConfig
from .service import Marc21TemplateService

__all__ = (
    "Marc21TemplateService",
    "Marc21TemplateServiceConfig",
)
