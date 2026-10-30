# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""High-level API for wokring with Marc21 records, pids and search."""

from .config import (
    Marc21DraftFilesServiceConfig,
    Marc21RecordFilesServiceConfig,
    Marc21RecordServiceConfig,
)
from .permissions import Marc21RecordPermissionPolicy
from .record import (
    DuplicateRecordError,
    Marc21Metadata,
    add_file_to_record,
    check_about_duplicate,
    convert_json_to_marc21xml,
    convert_marc21xml_to_json,
    create_record,
)
from .services import (
    Marc21DraftFilesService,
    Marc21RecordFilesService,
    Marc21RecordService,
    RecordItem,
)

__all__ = (
    "Marc21Metadata",
    "add_file_to_record",
    "create_record",
    "Marc21RecordService",
    "Marc21DraftFilesService",
    "Marc21RecordFilesService",
    "Marc21RecordServiceConfig",
    "Marc21DraftFilesServiceConfig",
    "Marc21RecordFilesServiceConfig",
    "Marc21RecordPermissionPolicy",
    "RecordItem",
    "DuplicateRecordError",
    "check_about_duplicate",
    "convert_json_to_marc21xml",
    "convert_marc21xml_to_json",
)
