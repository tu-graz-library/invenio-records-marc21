# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 field class."""

from .metadata import (
    Marc21Metadata,
    convert_json_to_marc21xml,
    convert_marc21xml_to_json,
)
from .utils import (
    DuplicateRecordError,
    add_file_to_record,
    check_about_duplicate,
    create_record,
)

__all__ = (
    "Marc21Metadata",
    "add_file_to_record",
    "create_record",
    "DuplicateRecordError",
    "check_about_duplicate",
    "convert_json_to_marc21xml",
    "convert_marc21xml_to_json",
)
