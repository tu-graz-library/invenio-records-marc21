# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record metadata field."""

import json
from os.path import dirname, join

from fastjsonschema import compile
from fastjsonschema.exceptions import JsonSchemaValueException
from marshmallow import Schema, validates_schema
from marshmallow.exceptions import ValidationError as MarshmallowValidationError


def get_schema():
    """Marc21 load json schema."""
    with open(
        join(
            dirname(__file__),
            "../../records/jsonschemas/marc21/marc21-structure-v1.0.0.json",
        ),
        "rb",
    ) as fp:
        input = fp.read()
        return json.loads(input.decode("utf-8"))


_schema = get_schema()
_schema_validator = compile(_schema)


class MetadataSchema(Schema):
    """Schema for the record metadata."""

    class Meta:
        """Meta class to accept additional fields."""

        additional = (
            "leader",
            "fields",
        )

    @validates_schema
    def validate(self, data, **kwargs):
        """Perform validation on ``data``.

        Raise a :exc:`ValidationError` if validation
        does not succeed.
        """
        try:
            _schema_validator(data)
        except JsonSchemaValueException as e:
            path = e.path[1:]
            raise MarshmallowValidationError(
                field_name=".".join(path), message=" ".join(e.message.split(" ")[1:])
            )
