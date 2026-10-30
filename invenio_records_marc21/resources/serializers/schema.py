# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Schemas for marc21 records serializers."""

from marshmallow import Schema
from marshmallow_utils.fields import SanitizedUnicode


class Marc21Schema(Schema):
    """Schema for dumping extra information for the marc21 record."""

    id = SanitizedUnicode(data_key="id", attribute="id")

    class Meta:
        """Meta class to accept unknwon fields."""

        additional = (
            "metadata",
            "created",
            "updated",
            "links",
            "files",
            "versions",
            "stats",
        )
