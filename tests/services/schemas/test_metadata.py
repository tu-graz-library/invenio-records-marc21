# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Test Marc21Metadata."""

from invenio_records_marc21.services.record import Marc21Metadata


def test_metadata_emplace_field():
    metadata = Marc21Metadata()
