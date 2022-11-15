# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

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
        )
