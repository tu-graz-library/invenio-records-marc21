# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
    "convert_marc21xml_to_json",
    "convert_json_to_marc21xml",
)
