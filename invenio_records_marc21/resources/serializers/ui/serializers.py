# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 UI record response serializers."""


from copy import deepcopy
from datetime import datetime

from lxml import etree

from ..schema import Marc21Schema
from ..serializer import Marc21BASESerializer, Marc21XMLMixin
from .schema import Marc21UISchema


def embargo_date(fields):
    """Embargo date."""
    if "971" not in fields:
        return None

    embargo_date = None
    for field in fields["971"]:
        if "a" in field["subfields"] and field["subfields"]["a"][0] == "gesperrt":
            marc_time = field["subfields"]["c"][0].split(" ")
            try:
                embargo_date = datetime.strptime(marc_time[0], "%d.%m.%Y").strftime(
                    "%Y-%m-%d"
                )
            except ValueError:
                embargo_date = None

    return embargo_date


class Marc21UIBASESerializer(Marc21BASESerializer):
    """UI Base serializer implementation."""

    def __init__(self, object_schema_cls=Marc21UISchema, object_key="ui", **options):
        """Marc21 UI Base Constructor.

        :param object_key: str key dump ui specific information
        """
        super().__init__(object_schema_cls=object_schema_cls, **options)
        self._object_key = object_key

    def dump_obj(self, obj):
        """Dump the object into a JSON string."""
        to_dump_obj = deepcopy(obj)
        if obj["access"]["embargo"]["active"]:
            embargo_until = embargo_date(obj["metadata"]["fields"])

            if embargo_until:
                to_dump_obj["access"]["embargo"]["until"] = embargo_until
        obj[self._object_key] = self.object_schema.dump(to_dump_obj)
        return obj


class Marc21UIJSONSerializer(Marc21UIBASESerializer):
    """UI JSON serializer implementation."""


class Marc21UIXMLSerializer(Marc21UIBASESerializer, Marc21XMLMixin):
    """UI Marc21 xml serializer implementation."""

    def __init__(self, object_schema_cls=Marc21Schema, object_key="ui", **options):
        """Marc21 UI XML Constructor.

        :param object_schema_cls: object schema serializing the Marc21 record. (default: `Marc21Schema`)
        :param object_key: str key dump ui specific information
        """
        super().__init__(
            object_schema_cls=object_schema_cls, object_key=object_key, **options
        )

    def dump_obj(self, obj):
        """Dump the object into a JSON string."""
        obj[self._object_key] = self.object_schema.dump(deepcopy(obj))

        # For edit a marc21 record in the deposit react app we need
        # the metadata field also as a marcxml string
        metadata = self.convert_metadata(obj[self._object_key]["metadata"], root=True)

        metadata = etree.tostring(
            metadata,
            pretty_print=False,
            xml_declaration=False,
            encoding="UTF-8",
        ).decode("UTF-8")

        obj[self._object_key]["metadata"] = metadata
        obj["metadata"] = deepcopy(obj[self._object_key]["metadata"])
        return obj
