# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio-Records-Marc21 datamodel."""

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

__version__ = "0.28.0"

__all__ = (
    "DuplicateRecordError",
    "InvenioRecordsMARC21",
    "Marc21Metadata",
    "Marc21RecordService",
    "MarcDraftProvider",
    "__version__",
    "add_file_to_record",
    "check_about_duplicate",
    "convert_json_to_marc21xml",
    "convert_marc21xml_to_json",
    "create_record",
    "current_records_marc21",
)
