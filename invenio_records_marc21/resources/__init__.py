# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Invenio Marc21 module to create REST APIs."""

from .config import (
    Marc21DraftFilesResourceConfig,
    Marc21ParentRecordLinksResourceConfig,
    Marc21RecordFilesResourceConfig,
    Marc21RecordResourceConfig,
)
from .resources import Marc21ParentRecordLinksResource, Marc21RecordResource

__all__ = (
    "Marc21RecordResource",
    "Marc21DraftFilesResourceConfig",
    "Marc21RecordFilesResourceConfig",
    "Marc21RecordResourceConfig",
    "Marc21ParentRecordLinksResourceConfig",
    "Marc21ParentRecordLinksResource",
)
