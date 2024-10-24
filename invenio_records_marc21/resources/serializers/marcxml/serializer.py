# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record response xml serializer."""

from lxml import etree
from lxml.builder import E, ElementMaker

from ..serializer import Marc21BASESerializer


class Marc21XMLMixin:
    """Marc21 XML converter class."""

    controlfields = [
        "001",
        "003",
        "005",
        "006",
        "007",
        "008",
        "009",
    ]

    def _convert(self, key, data):
        root = etree.Element(key)
        if isinstance(data, dict):
            for k, v in data.items():
                root.append(self._convert(k, v))
        elif isinstance(data, (list, tuple)):
            for item in data:
                root.append(self._convert(key, item))
        else:
            root.text = str(data)
        return root

    def convert_record(self, data):
        """Convert marc21 record to xml."""
        E = ElementMaker()
        record = E.record()
        for key, value in data.items():
            if "metadata" in key:
                record.append(self.convert_metadata(value))
                continue
            record.append(self._convert(key, value))
        return etree.tostring(
            record,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8",
        ).decode("UTF-8")

    def convert_metadata(self, data, root=False):
        """Convert the metadata to Marc21 xml."""
        if root:
            rec = E.record()
        else:
            rec = E.metadata()

        leader = data.get("leader")
        if leader:
            rec.append(E.leader(leader))

        fields = data.get("fields", {})

        for key, value in fields.items():
            # Control fields
            if key in self.controlfields:
                controlfield = E.controlfield(value)
                controlfield.attrib["tag"] = key
                rec.append(controlfield)
            else:
                for subfields in value:
                    datafield = E.datafield()
                    datafield.attrib["tag"] = key

                    indicator1 = subfields.get("ind1", " ")
                    indicator2 = subfields.get("ind2", " ")

                    datafield.attrib["ind1"] = indicator1.replace("_", " ")
                    datafield.attrib["ind2"] = indicator2.replace("_", " ")
                    items = subfields.get("subfields", {})
                    for k in items.keys():
                        datafield.append(E.subfield(", ".join(items[k]), code=k))
                    rec.append(datafield)
        return rec


class Marc21XMLSerializer(Marc21BASESerializer, Marc21XMLMixin):
    """Marc21 XML export serializer implementation."""

    def dump_obj(self, obj):
        """Serialize a single record.

        :param record: Record instance.
        """
        return self.convert_record(super().dump_obj(obj))

    def serialize_object(self, obj):
        """Serialize a single record.

        :param record: Record instance.
        """
        return self.dump_obj(obj)

    def serialize_object_list(self, obj_list):
        """Dump the object list into a JSON string."""
        list_obj = []
        for obj in obj_list["hits"]["hits"]:
            list_obj.append(self.serialize_object(obj))

        return "\n".join(list_obj)
