# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schemas."""

import arrow
from flask_babelex import lazy_gettext as _
from marshmallow import Schema, ValidationError, validates, validates_schema
from marshmallow_utils.fields import Integer, List, SanitizedUnicode
from marshmallow_utils.fields.nestedattr import NestedAttribute

from ...components import AccessStatusEnum
from .embargo import EmbargoSchema


class Agent(Schema):
    """An agent schema."""

    user = Integer(required=True)


class AccessSchema(Schema):
    """Access schema."""

    metadata = SanitizedUnicode(required=True)
    files = SanitizedUnicode(required=True)
    embargo = NestedAttribute(EmbargoSchema)
    status = SanitizedUnicode(dump_only=False)
    owned_by = List(fields.Nested(Agent))

    def validate_protection_value(self, value, field_name):
        """Check that the protection value is valid."""
        if value not in AccessStatusEnum.list():
            raise ValidationError(
                _("'{}' must be either '{}', '{}' or '{}'").format(
                    field_name,
                    *AccessStatusEnum.list(),
                ),
                "record",
            )

    @validates("metadata")
    def validate_record_protection(self, value):
        """Validate the record protection value."""
        self.validate_protection_value(value, "record")

    @validates("files")
    def validate_files_protection(self, value):
        """Validate the files protection value."""
        self.validate_protection_value(value, "files")
