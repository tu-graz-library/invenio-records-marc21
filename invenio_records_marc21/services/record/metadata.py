# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record class."""

from collections.abc import Iterator
from contextlib import suppress
from dataclasses import dataclass
from typing import cast
from warnings import warn
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


def convert_marc21xml_to_json(record):
    """MARC21 Record class convert to json."""
    visitor = XmlToJsonVisitor()
    visitor.visit(record)
    return visitor.get_json_record()


class XmlToJsonVisitor:
    """XmlToJsonVisitor class."""

    def __init__(self) -> None:
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


@dataclass
class Field:
    """Base field."""

    category: str

    def __init__(self, category: str | None = None) -> None:
        """Construct."""
        self._list: list[Field] = []

        if category:
            self.category = category

    def append(self, field: "Field") -> None:
        """Append."""
        self._list.append(field)

    def dump(self) -> list:
        """Dump."""
        return [field.to_obj() for field in self._list]

    def to_obj(self) -> dict:
        """To obj."""
        return {}

    def __iter__(self) -> Iterator["Field"]:
        """Iter."""
        return iter(self._list)


@dataclass
class ControlField(Field):
    """Control field."""

    value: str

    def __str__(self) -> str:
        """Stringify."""
        return self.value

    def dump(self) -> str:  # type: ignore[override]
        """Dump."""
        return self.value


@dataclass
class DataField(Field):
    """Data field."""

    ind1: str
    ind2: str
    subfields: dict[str, list[str]]

    def __init__(
        self,
        selector: str,
        *,
        value: str | None = None,
        subfs: dict | None = None,
    ) -> None:
        """Construct datafield."""
        super().__init__()

        tag, ind1, ind2, code = selector.split(".")

        if not ind1:
            ind1 = "_"

        if not ind2:
            ind2 = "_"

        if not code:
            code = "a"

        self.category = tag
        self.ind1 = ind1
        self.ind2 = ind2
        self.subfields = {}

        if value:
            self.subfields[code] = [value]
        elif subfs:
            for key, val in sorted(
                subfs.items(),
                key=lambda x: f"zz{x}" if x[0].isnumeric() else x[0],
            ):
                self.subfields[key] = val if isinstance(val, list) else [val]
        else:
            msg = "Neither of value or subfs is set."
            raise RuntimeError(msg)

        self._list.append(self)

    def get(self, subf_code: str) -> str:
        """Get."""
        return " ".join(self.subfields.get(subf_code, []))

    def to_obj(self) -> dict:
        """To obj."""
        return {
            "ind1": self.ind1,
            "ind2": self.ind2,
            "subfields": self.subfields,
        }

    def __getitem__(self, key: str | int) -> DataField | dict:
        """Getitem."""
        warn(
            "don't use subscription on DataField. please correct the code",
            DeprecationWarning,
            2,
        )
        if isinstance(key, int):
            return self

        if isinstance(key, str) and key == "subfields":
            return self.subfields

        raise RuntimeError


@dataclass
class Marc21MetadataJson:
    """Dataclass for Marc21Metatada json structure.

    leader: "00000nam a2200000zca4500",
    fields: {
        100: [
          {
             ind1: "",
             ind2: "",
             subfields:
          }
        ]
    }
    """

    leader: str
    fields: dict[str, Field]

    def add(self, field: Field) -> None:
        """Add."""
        self.fields[field.category] = field

    def extend(self, field: Field) -> None:
        """Extend."""
        self.fields[field.category].append(field)

    def emplace(self, field: DataField) -> None:
        """Emplace."""
        # NOTE: only implemented for DataField, because it does not make sense for ControlField

        # if the tag already exists it has to be found the correct ind1/ind2
        # combination to update subfields. dict does not deep update as
        # intended
        datafields = self.fields[field.category]
        for d in cast(list[DataField], datafields):
            if d.ind1 == field.ind1 and d.ind2 == field.ind2:
                for code, value in field.subfields.items():
                    if code in d.subfields:
                        d.subfields[code].extend(value)
                    else:
                        d.subfields[code] = value

    def dump(self) -> dict:
        """Dump."""
        return {
            "leader": self.leader,
            "fields": {tag: field.dump() for tag, field in self.fields.items()},
        }


class Marc21Metadata:
    """MARC21 Record class to facilitate storage of records in MARC21 format."""

    metadata: Marc21MetadataJson

    DATAFIELD_START_CATEGORY = 10

    def __init__(self, *, json: dict | None = None) -> None:
        """Default constructor of the class."""
        self.set_default()

        if json:
            self.json = json

    def set_default(self) -> None:
        """Set default marc21 structure."""
        self.metadata = Marc21MetadataJson("00000nam a2200000zca4500", {})

    def is_control_field(self, category: str) -> bool:
        """Is control field."""
        try:
            return int(category) < self.DATAFIELD_START_CATEGORY
        except ValueError:
            return False

    @property
    def json(self) -> dict:
        """Metadata json getter method."""
        return {"metadata": self.metadata.dump()}

    @json.setter
    def json(self, _json: dict) -> None:
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

        _json = _json.get("metadata", _json)

        self.metadata.leader = _json["leader"]

        for tag, field in _json["fields"].items():
            try:
                int(tag)  # filter out AV* fields
            except ValueError:
                continue

            if self.is_control_field(tag):
                self.metadata.add(ControlField(tag, field))
            else:
                datafields = Field(tag)
                for fie in field:
                    selector = f"{tag}.{fie['ind1']}.{fie['ind2']}."
                    datafields.append(DataField(selector, subfs=fie["subfields"]))
                self.metadata.add(datafields)

    def get_field(self, selector: str, *, subf_value: str = "") -> DataField | None:
        """Get Field."""
        category, ind1, ind2, subf_code = selector.split(".")
        _, datafields = self.get_fields(category, ind1, ind2)
        out = []
        for field in datafields:
            if (
                subf_code
                and subf_value
                and field.subfields.get(subf_code, [None])[0] == subf_value
            ):
                out.append(field)
            elif subf_code and not subf_value and subf_code in field.subfields:
                out.append(field)
            elif (
                not subf_code
                and subf_value
                and [subf_value] in field.subfields.values()
            ):
                out.append(field)
            elif not subf_code and not subf_value:
                out.append(field)

        return out[0] if len(out) > 0 else None

    def get_fields(
        self,
        category: str,
        ind1: str | None = None,
        ind2: str | None = None,
    ) -> tuple[ControlField | None, list[DataField]]:
        """Return fields found by category.

        The return value could be found more precisely by defining ind1, ind2
        and subf_code.
        """
        if not category.isnumeric():
            return None, []

        controlfield: ControlField | None = None
        datafields: list[DataField] = []

        try:
            if self.is_control_field(category):
                controlfield = cast(ControlField, self.metadata.fields[category])
                return controlfield, datafields
        except KeyError:
            controlfield = None

        def fix_underline(ind: str) -> list[str | None]:
            # the problem is that the codebase introduced "_" as a replacement
            # for " " and this has to be fixed somewhere in the future
            return [ind, " " if ind == "_" else None, "_" if ind == " " else None]

        def ind_condition(d: DataField) -> bool:
            ind1_ = d.ind1 in fix_underline(ind1) if ind1 else True
            ind2_ = d.ind2 in fix_underline(ind2) if ind2 else True
            return ind1_ and ind2_

        try:
            datafields = [
                d
                for d in cast(list[DataField], self.metadata.fields[category])
                if ind_condition(d)
            ]
        except KeyError:
            datafields = []
        else:
            return controlfield, datafields

        return controlfield, datafields

    def get_value(
        self,
        category: str,
        ind1: str | None = None,
        ind2: str | None = None,
        subf_code: str | None = None,
    ) -> str:
        """Get the value of the found field."""
        controlfield, datafields = self.get_fields(category, ind1, ind2)

        if controlfield:
            return str(controlfield)

        if len(datafields) > 0:
            try:
                return " ".join(datafields[0].subfields[subf_code or ""])
            except KeyError:
                return ""

        return ""

    def get_values(
        self,
        category: str,
        ind1: str | None = None,
        ind2: str | None = None,
        subf_code: str | None = None,
    ) -> list[str]:
        """Get values of the found field."""
        controlfield, datafields = self.get_fields(category, ind1, ind2)

        values: list[str] = []

        if controlfield:
            values.append(str(controlfield))

        for datafield in datafields:
            if subf_code is None:
                values.extend(" ".join(d) for d in datafield.subfields.values())

            with suppress(KeyError):
                values.extend(datafield.subfields[subf_code or ""])

        return values

    def exists_field(
        self,
        category: str,
        ind1: str | None = None,
        ind2: str | None = None,
        subf_code: str | None = None,
        subf_value: str | None = None,
    ) -> bool:
        """Check if the field exists."""
        values = self.get_values(category, ind1, ind2, subf_code)
        return any(value == subf_value for value in values)

    def emplace_leader(self, value: str = "") -> None:
        """Change leader string in record."""
        self.metadata.leader = value

    def emplace_controlfield(self, tag: str = "", value: str = "") -> None:
        """Add value to record for given datafield and subfield."""
        if not self.is_control_field(tag):
            msg = "ERROR: controlfields are < 10"
            raise RuntimeError(msg)

        controlfield = ControlField(tag, value)
        self.metadata.add(controlfield)

    def emplace_datafield(
        self,
        selector: str,
        *,
        value: str | None = None,
        subfs: dict | None = None,
    ) -> None:
        """Emplace value to record for given datafield and subfield.

        :params selector e.g. "100...a", "100"

        This method should only be used if a field with the same indicators
        should be merged together. If a field like 500 should be added twice,
        use add_datafield.

        It could be problematic to mix emplace_datafield and add_datafield.

        On the first addition emplace_datafield and add_datafield work the same,
        the difference only becomes apparent when an identical field is added.
        """
        datafield = DataField(selector, value=value, subfs=subfs)

        if datafield.category not in self.metadata.fields:
            self.metadata.add(datafield)
        else:
            self.metadata.emplace(datafield)

    def add_datafield(
        self,
        selector: str,
        *,
        value: str | None = None,
        subfs: dict | None = None,
    ) -> None:
        """Add value to record for given datafield and subfield.

        This method can be used if two independent fields with the same
        indicator should be added to the fields list.
        """
        datafield = DataField(selector, value=value, subfs=subfs)

        if datafield.category not in self.metadata.fields:
            self.metadata.add(datafield)
        else:
            self.metadata.extend(datafield)
