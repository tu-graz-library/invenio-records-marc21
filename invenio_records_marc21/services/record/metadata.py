# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2022 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record class."""

from xml.etree.ElementTree import Element, fromstring, tostring


class QName:
    """Local Rewrite for lxml.etree.QName."""

    def __init__(self, node):
        """Constructor for QName."""
        self.node = node

    @property
    def localname(self):
        """Return localname from node with xpath."""
        return self.node.tag.split("}")[-1]

    @property
    def namespace(self):
        """Return namespace from node with xpath."""
        return self.node.tag.split("}")[0][1:]


def convert_json_to_marc21xml(record):
    """Convert marc21 json to marc21 xml."""
    visitor = JsonToXmlVisitor(record["leader"])
    visitor.visit(record["fields"])
    return visitor.get_xml_record()


class JsonToXmlVisitor:
    """JsonToXmlVisitor class."""

    def __init__(self, leader_):
        """Constructor."""
        self.record = Element("record", xmlns="http://www.loc.gov/MARC21/slim")
        leader = Element("leader")
        leader.text = leader_
        self.record.append(leader)

    def get_xml_record(self):
        """Get xml record."""
        return self.record

    def visit(self, fields):
        """Default visit method."""
        for category, items in fields.items():
            if int(category) < 10:
                self.visit_controlfield(category, items)
            else:
                self.visit_datafield(category, items)

    def visit_controlfield(self, category, value):
        """Visit controlfield."""
        controlfield = Element("controlfield", {"tag": category})
        controlfield.text = value
        self.record.append(controlfield)

    def visit_datafield(self, category, items):
        """Visit datafield."""
        for item in items:
            datafield = Element(
                "datafield",
                {"tag": category, "ind1": item["ind1"], "ind2": item["ind2"]},
            )
            for subfn, subfv in sorted(item["subfields"].items()):
                subfield = Element("subfield", {"code": subfn})
                subfield.text = " ".join(subfv)
                datafield.append(subfield)

            self.record.append(datafield)


def convert_marc21xml_to_json(record):
    """MARC21 Record class convert to json."""
    visitor = XmlToJsonVisitor()
    visitor.visit(record)
    return visitor.get_json_record()


class XmlToJsonVisitor:
    """XmlToJsonVisitor class."""

    def __init__(self):
        """Constructor."""
        self.record = {"leader": "", "fields": {}}

    def process(self, node):
        """Execute the corresponding method to the tag name."""

        def func_not_found(*args, **kwargs):
            localname = QName(node).localname
            namespace = QName(node).namespace
            raise ValueError(f"NO visitor node: '{localname}' ns: '{namespace}'")

        tag_name = QName(node).localname
        visit_func = getattr(self, f"visit_{tag_name}", func_not_found)
        result = visit_func(node)
        return result

    def visit(self, node):
        """Visit default method and entry point for the class."""
        for child in node:
            self.process(child)

    def append_string(self, tag: str, value: str):
        """Append to the field dict a single string."""
        self.record["fields"][tag] = value

    def append(self, tag: str, field: dict):
        """Append to the field tag list."""
        if tag not in self.record["fields"]:
            self.record["fields"][tag] = []

        self.record["fields"][tag].append(field)

    def get_json_record(self):
        """Get the mij representation of the marc21 xml record."""
        return self.record

    def visit_record(self, node):
        """Visit the record."""
        self.record = {"leader": "", "fields": {}}
        self.visit(node)

    def visit_leader(self, node):
        """Visit the controlfield field."""
        self.record["leader"] = node.text

    def visit_controlfield(self, node):
        """Visit the controlfield field."""
        field = node.text
        self.append_string(node.get("tag"), field)

    def visit_datafield(self, node):
        """Visit the datafield field."""
        self.subfields = {}
        self.visit(node)

        tag = node.get("tag")
        ind1 = node.get("ind1", "_").replace(" ", "_")
        ind2 = node.get("ind2", "_").replace(" ", "_")

        field = {
            "ind1": ind1,
            "ind2": ind2,
            "subfields": self.subfields,
        }
        self.append(tag, field)

    def visit_subfield(self, node):
        """Visit the subfield field."""
        subf_code = node.get("code")

        if subf_code not in self.subfields:
            self.subfields[subf_code] = []

        self.subfields[subf_code].append(node.text)


class Marc21Metadata:
    """MARC21 Record class to facilitate storage of records in MARC21 format."""

    def __init__(self, *, metadata=None, json=None):
        """Default constructor of the class."""
        self.set_default()

        if metadata:
            self.etree = metadata

        if json:
            self.json = json

    def set_default(self):
        """Set default marc21 structure."""
        self._json = {}

        leader = Element("leader")
        leader.text = "00000nam a2200000zca4500"
        self._etree = Element("record", xmlns="http://www.loc.gov/MARC21/slim")
        self._etree.append(leader)

    @property
    def etree(self):
        """Metadata etree getter method."""
        return self._etree

    @etree.setter
    def etree(self, _etree):
        """Etree setter."""
        self._etree = _etree

    @property
    def json(self):
        """Metadata json getter method."""
        self._json = {"metadata": convert_marc21xml_to_json(self._etree)}
        return self._json

    @json.setter
    def json(self, json):
        """Metadata json setter method."""
        if not isinstance(json, dict):
            raise TypeError("json must be from type dict")
        self._json = json
        self._etree = convert_json_to_marc21xml(self._json)

    @property
    def xml(self):
        """Metadata xml getter method."""
        return tostring(self._etree).decode("UTF-8")

    @xml.setter
    def xml(self, xml):
        """Metadata xml setter method."""
        if not isinstance(xml, str):
            raise TypeError("xml must be from type str")

        self._etree = fromstring(xml)

    def exists(self, to_check_category: Element, art_of_category):
        """Check if a category is already in the tree.

        Only completely equal tags will be dismissed.
        """
        to_check_category_str = tostring(to_check_category, method="xml").strip()
        for category in self._etree.findall(art_of_category):
            category_str = tostring(category, method="xml").strip()
            if to_check_category_str == category_str:
                return True

        return False

    def emplace_leader(self, value=""):
        """Change leader string in record."""
        for leader in self._etree.iter("leader"):
            leader.text = value

    def emplace_controlfield(self, tag="", value=""):
        """Add value to record for given datafield and subfield."""
        controlfield = Element("controlfield", tag=tag)
        controlfield.text = value

        if self.exists(controlfield, "controlfield"):
            return

        self._etree.append(controlfield)

    def emplace_datafield(self, selector, *, value=None, subfs=None) -> None:
        """Add value to record for given datafield and subfield.

        :params selector e.g. "100...a", "100"
        """
        tag, ind1, ind2, code = selector.split(".")

        if not ind1:
            ind1 = "_"

        if not ind2:
            ind2 = "_"

        if not code:
            code = "a"

        datafield = Element("datafield", tag=tag, ind1=ind1, ind2=ind2)
        if value:
            subfield = Element("subfield", code=code)
            subfield.text = value
            datafield.append(subfield)

        elif subfs:
            for key, val in sorted(subfs.items()):
                subfield = Element("subfield", code=key)
                subfield.text = " ".join(val)
                datafield.append(subfield)

        else:
            raise RuntimeError("Neither of value or subfs is set.")

        # double check
        if self.exists(datafield, "datafield"):
            return

        self._etree.append(datafield)
