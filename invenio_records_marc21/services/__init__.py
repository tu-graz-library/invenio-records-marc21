# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
