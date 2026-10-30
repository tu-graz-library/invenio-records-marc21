# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 record schemas."""

from marshmallow import Schema, fields


#
# PIDs
#
class PIDSchema(Schema):
    """PIDs schema."""

    identifier = fields.Str(required=True)
    provider = fields.Str(required=True)
    client = fields.Str()
