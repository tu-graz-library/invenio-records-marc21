# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Test Marc21Metadata."""

from invenio_records_marc21.services.record import Marc21Metadata


def test_metadata_emplace_field():
    metadata = Marc21Metadata()
