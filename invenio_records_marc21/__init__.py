# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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

__version__ = "0.34.4"

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
