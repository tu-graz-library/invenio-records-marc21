# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record class."""

from contextlib import suppress
from xml.etree.ElementTree import Element


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
        self.namespace = "http://www.loc.gov/MARC21/slim"
        self.record = Element("record", xmlns=self.namespace)

        leader = Element(f"{{{self.namespace}}}leader")
        leader.text = leader_
        self.record.append(leader)

    def get_xml_record(self):
        """Get xml record."""
        return self.record

    def visit(self, fields):
        """Default visit method."""
        for category, items in fields.items():
            if category == "AVA" or category == "AVE":
                self.visit_datafield(category, items)
            elif int(category) < 10:
                self.visit_controlfield(category, items)
            else:
                self.visit_datafield(category, items)

    def visit_controlfield(self, category, value):
        """Visit controlfield."""
        controlfield = Element(f"{{{self.namespace}}}controlfield", {"tag": category})
        controlfield.text = value
        self.record.append(controlfield)

    def visit_datafield(self, category, items):
        """Visit datafield."""
        for item in items:
            ind1 = item["ind1"].replace("_", " ")
            ind2 = item["ind2"].replace("_", " ")
            datafield = Element(
                f"{{{self.namespace}}}datafield",
                {
                    "tag": category,
                    "ind1": ind1,
                    "ind2": ind2,
                },
            )
            for subfn, subfv in sorted(
                item["subfields"].items(),
                key=lambda x: f"zz{x}" if x[0].isnumeric() else x[0],
            ):
                subfield = Element(f"{{{self.namespace}}}subfield", {"code": subfn})
                subfield.text = " ".join(subfv)
                datafield.append(subfield)

            self.record.append(datafield)


class Marc21Metadata:
    """MARC21 Record class to facilitate storage of records in MARC21 format."""

    def __init__(self, *, json=None):
        """Default constructor of the class."""
        self.set_default()

        if json:
            self.json = json

    def set_default(self):
        """Set default marc21 structure."""
        self._json = {
            "leader": "00000nam a2200000zca4500",
            "fields": {},
        }

    @property
    def json(self):
        """Metadata json getter method."""
        return {"metadata": self._json}

    @json.setter
    def json(self, _json):
        """Metadata json setter method."""
        if not (
            isinstance(_json, dict)
            and "leader" in _json
            and "fields" in _json
            and isinstance(_json["fields"], dict)
        ):
            msg = (
                "Marc21Metadata should get a dictionary with at least leader and fields"
            )
            raise TypeError(msg)

        self._json = _json["metadata"] if "metadata" in _json else _json

    def get_fields(
        self,
        category: str,
        ind1: str = None,
        ind2: str = None,
        return_type: str = "xml",
    ) -> tuple[list[Element], list[Element]]:
        """Return fields found by category.

        The return value could be found more precisely by defining ind1, ind2
        and subf_code.
        """
        if not category.isnumeric():
            return ([], [])

        try:
            if int(category) < 10:
                controlfields = [self._json["fields"][category]]
            else:
                controlfields = []
        except KeyError:
            controlfields = []

        def fix_underline(ind):
            # the problem is that the codebase introduced "_" as a replacement
            # for " " and this has to be fixed somewhere in the future
            return [ind, " " if ind == "_" else None, "_" if ind == " " else None]

        def ind_condition(d):
            ind1_ = d["ind1"] in fix_underline(ind1) if ind1 else True
            ind2_ = d["ind2"] in fix_underline(ind2) if ind2 else True
            return ind1_ and ind2_

        try:
            datafields = [d for d in self._json["fields"][category] if ind_condition(d)]
        except KeyError:
            datafields = []

        return (controlfields, datafields)

    def get_value(
        self,
        category: str,
        ind1: str = None,
        ind2: str = None,
        subf_code: str = None,
    ) -> str:
        """Get the value of the found field."""
        controlfields, datafields = self.get_fields(category, ind1, ind2)

        if len(controlfields) > 0:
            return controlfields[0]

        if len(datafields) > 0:
            try:
                return " ".join(datafields[0]["subfields"][subf_code])
            except KeyError:
                return ""

        return ""

    def get_values(
        self,
        category: str,
        ind1: str = None,
        ind2: str = None,
        subf_code: str = None,
    ) -> list[str]:
        """Get values of the found field."""
        controlfields, datafields = self.get_fields(category, ind1, ind2)

        values = []

        for controlfield in controlfields:
            values.append(controlfield)

        for datafield in datafields:
            if subf_code is None:
                for value in datafield["subfields"].values():
                    values.extend(value)

            with suppress(KeyError):
                values.extend(datafield["subfields"][subf_code])

        return values

    def exists_field(
        self,
        category: str,
        ind1: str = None,
        ind2: str = None,
        subf_code: str = None,
        subf_value: str = None,
    ) -> bool:
        """Check if the field exists."""
        values = self.get_values(category, ind1, ind2, subf_code)
        return any((value == subf_value for value in values))

    def emplace_leader(self, value=""):
        """Change leader string in record."""
        self._json["leader"] = value

    def emplace_controlfield(self, tag="", value=""):
        """Add value to record for given datafield and subfield."""
        if int(tag) > 9:
            raise RuntimeError("ERROR: controlfields are < 10")

        controlfield = {tag: value}
        self._json["fields"].update(controlfield)

    def emplace_datafield(self, selector, *, value=None, subfs=None) -> None:
        """Emplace value to record for given datafield and subfield.

        :params selector e.g. "100...a", "100"

        This method should only be used if a field with the same indicators
        should be merged together. If a field like 500 should be added twice,
        use add_datafield.

        It could be problematic to mix emplace_datafield and add_datafield.

        On the first addition emplace_datafield and add_datafield work the same,
        the difference only becomes apparent when an identical field is added.
        """
        tag, ind1, ind2, code = selector.split(".")
        datafield = self._datafield(selector, value=value, subfs=subfs)

        if tag not in self._json["fields"]:
            self._json["fields"].update(datafield)
        else:
            # if the tag already exists it has to be found the correct ind1/ind2
            # combination to update subfields. dict does not deep update as
            # intended
            datafields = self._json["fields"][tag]
            for d in datafields:
                if d["ind1"] == ind1 and d["ind2"] == ind2:
                    for code, value in datafield[tag][0]["subfields"].items():
                        if code in d["subfields"]:
                            d["subfields"][code].extend(value)
                        else:
                            d["subfields"][code] = value

    def add_datafield(self, selector, *, value=None, subfs=None) -> None:
        """Add value to record for given datafield and subfield.

        This method can be used if two independent fields with the same
        indicator should be added to the fields list.
        """
        tag, _, _, _ = selector.split(".")
        datafield = self._datafield(selector, value=value, subfs=subfs)

        if tag not in self._json["fields"]:
            self._json["fields"].update(datafield)
        else:
            self._json["fields"][tag].extend(datafield[tag])

    def _datafield(self, selector, *, value=None, subfs=None) -> dict:
        """Construct datafield."""
        tag, ind1, ind2, code = selector.split(".")

        if not ind1:
            ind1 = "_"

        if not ind2:
            ind2 = "_"

        if not code:
            code = "a"

        datafield = {
            tag: [
                {
                    "ind1": ind1,
                    "ind2": ind2,
                    "subfields": {},
                }
            ],
        }

        if value:
            datafield[tag][0]["subfields"][code] = [value]
        elif subfs:
            for key, val in sorted(
                subfs.items(),
                key=lambda x: f"zz{x}" if x[0].isnumeric() else x[0],
            ):
                datafield[tag][0]["subfields"][key] = (
                    val if isinstance(val, list) else [val]
                )
        else:
            raise RuntimeError("Neither of value or subfs is set.")

        return datafield
