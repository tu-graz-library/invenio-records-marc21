# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-records-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Tugraz statistic record schemas."""


from marshmallow import Schema, fields


class PartialStatisticSchema(Schema):
    """Schema for a part of the record statistics.

    This fits both the statistics for "this version" as well as
    "all versions", because they have the same shape.
    """

    views = fields.Int()
    unique_views = fields.Int()
    downloads = fields.Int()
    unique_downloads = fields.Int()
    data_volume = fields.Float()


class Marc21StatisticSchema(Schema):
    """Schema for the entire record statistics."""

    this_version = fields.Nested(PartialStatisticSchema)
    all_versions = fields.Nested(PartialStatisticSchema)
