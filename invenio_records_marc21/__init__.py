# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio-Records-Marc21 datamodel."""

from __future__ import absolute_import, print_function

from .ext import InvenioRecordsMARC21
from .proxies import current_records_marc21
from .records import MarcDraftProvider
from .services import (
    DuplicateRecordError,
    Marc21Metadata,
    Marc21RecordService,
    add_file_to_record,
    check_about_duplicate,
    convert_json_to_marc21xml,
    convert_marc21xml_to_json,
    create_record,
)

__version__ = "0.25.2"

__all__ = (
    "__version__",
    "InvenioRecordsMARC21",
    "current_records_marc21",
    "Marc21Metadata",
    "add_file_to_record",
    "create_record",
    "MarcDraftProvider",
    "DuplicateRecordError",
    "check_about_duplicate",
    "convert_json_to_marc21xml",
    "convert_marc21xml_to_json",
    "Marc21RecordService",
)
