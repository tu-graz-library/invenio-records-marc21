# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record metadata field."""

from functools import cache
from json import loads
from pathlib import Path
from typing import cast

from fastjsonschema import compile  # noqa: A004
from fastjsonschema.exceptions import JsonSchemaValueException
from marshmallow import Schema, validates_schema
from marshmallow.exceptions import ValidationError
from marshmallow.fields import Dict, Str

SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "records/jsonschemas/marc21/marc21-structure-v1.0.0.json"
)


@cache
def get_schema() -> dict:
    """Marc21 load json schema."""
    return cast(dict, loads(SCHEMA_PATH.read_bytes()))


_schema = get_schema()
_schema_validator = compile(_schema)


class MetadataSchema(Schema):
    """Schema for the record metadata."""

    leader = Str()
    fields = Dict()  # type: ignore[assignment]

    @validates_schema
    def validate(self, data: dict, **__: dict) -> None:
        """Perform validation on ``data``.

        Raise a :exc:`ValidationError` if validation
        does not succeed.
        """
        try:
            _schema_validator(data)
        except JsonSchemaValueException as e:
            path = e.path[1:]
            raise ValidationError(
                field_name=".".join(path),
                message=" ".join(e.message.split(" ")[1:]),
            ) from e
