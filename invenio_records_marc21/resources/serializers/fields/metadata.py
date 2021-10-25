# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Metadata field for marc21 records."""

from dojson.contrib.to_marc21 import to_marc21
from dojson.contrib.to_marc21.utils import dumps
from dojson.utils import GroupableOrderedDict
from marshmallow.fields import Field

from ..errors import Marc21XMLConvertError


class MetadataField(Field):
    """Schema for the record metadata."""

    def _remove_order(self, data):
        """Removing order key in marc21 dict."""
        if isinstance(data, dict):
            kwargs = {}
            if isinstance(data, GroupableOrderedDict):
                kwargs = {"with_order": False}
            temp = []
            for k, v in data.items(**kwargs):
                temp.append((k, self._remove_order(v)))
            return dict(temp)
        elif isinstance(data, (list, tuple)):
            return [self._remove_order(item) for item in data]
        return data

    def remove_order_key(self, data, **kwargs):
        """Remove order key in metadata dict ."""
        remove_order = self.context.get("remove_order", False)
        if data and remove_order:
            data = self._remove_order(GroupableOrderedDict(data))
        return data

    def convert_xml(self, data, **kwargs):
        """Convert json into marc21 xml."""
        marcxml = self.context.get("marcxml", False)
        if data and marcxml:
            try:
                data = dumps(to_marc21.do(data))  # .decode("UTF-8")
            except Exception as e:
                raise Marc21XMLConvertError(e)

        return data

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialise access status."""
        if value:
            record_metadata = value

            record_metadata = self.remove_order_key(record_metadata)
            record_metadata = self.convert_xml(record_metadata)

            return record_metadata
        return {}
