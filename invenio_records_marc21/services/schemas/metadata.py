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


import typing

from dojson.contrib.marc21 import marc21
from dojson.contrib.marc21.utils import create_record
from marshmallow.fields import Field


def remove_order(obj):
    if isinstance(obj, dict):
        obj = {
            key: remove_order(value) for key, value in obj.items() if key != "__order__"
        }
    elif isinstance(obj, list):
        obj = [remove_order(item) for item in obj]
    return obj


class MetadataField(Field):
    """Schema for the record metadata."""

    def _deserialize(
        self,
        value: typing.Any,
        attr: typing.Optional[str],
        data: typing.Optional[typing.Mapping[str, typing.Any]],
        **kwargs
    ):
        """Deserialize value. Concrete :class:`Field` classes should implement this method.

        :param value: The value to be deserialized.
        :param attr: The attribute/key in `data` to be deserialized.
        :param data: The raw input data passed to the `Schema.load`.
        :param kwargs: Field-specific keyword arguments.
        :raise ValidationError: In case of formatting or validation failure.
        :return: The deserialized value.

        .. versionchanged:: 2.0.0
            Added ``attr`` and ``data`` parameters.

        .. versionchanged:: 3.0.0
            Added ``**kwargs`` to signature.
        """
        if "xml" in value:
            value = remove_order(marc21.do(create_record(value["xml"])))
        return value

    def _validate(self, value):
        """Perform validation on ``value``.

        Raise a :exc:`ValidationError` if validation
        does not succeed.
        """
        # TODO: validate the marc21 xml during loading the Schema
        self._validate_all(value)
