# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record class."""

from io import StringIO
from os import linesep
from os.path import dirname, join

from dojson.contrib.marc21 import marc21
from dojson.contrib.marc21.utils import create_record
from lxml import etree
from lxml.builder import ElementMaker


class Marc21Metadata(object):
    """MARC21 Record class to facilitate storage of records in MARC21 format."""

    def __init__(self):
        """Default constructor of the class."""
        self._xml = ""
        self._json = {}
        self._etree = etree.Element(
            "record", xmlns="http://www.loc.gov/MARC21/slim", type="Bibliographic"
        )
        leader = etree.Element("leader")
        leader.text = "00000nam a2200000zca4500"
        self._etree.append(leader)

    @property
    def json(self):
        """Metadata json getter method."""
        record = create_record(self._etree)
        self._json = {"metadata": marc21.do(record)}
        return self._json

    @property
    def etree(self):
        """Metadata etree getter method."""
        return self._etree

    @json.setter
    def json(self, json: dict):
        """Metadata json setter method."""
        if not isinstance(json, dict):
            raise TypeError("json must be from type dict")
        self._json = json

    @property
    def xml(self):
        """Metadata xml getter method."""
        self._to_string()
        return self._xml

    @xml.setter
    def xml(self, xml: str):
        """Metadata xml setter method."""
        if not isinstance(xml, str):
            raise TypeError("xml must be from type str")

        tree = self._to_xml_tree_from_string(xml)
        self._etree = tree
        self._xml = xml

    def load(self, xml: etree):
        """Load metadata from etree."""
        self._etree = xml

    def _to_xml_tree_from_string(self, xml: str):
        """Xml string to internal representation method."""
        tree = etree.parse(StringIO(xml))
        return tree

    def _to_string(self, tagsep: str = linesep, indent: int = 4) -> str:
        """Get a pretty-printed XML string of the record."""
        self._xml = etree.tostring(self._etree, pretty_print=True).decode("UTF-8")

    def contains(self, ref_df: dict, ref_sf: dict):
        """Return True if record contains reference datafield, which contains reference subfield.

        @param ref_df dict: datafield element specific information, containing keys [tag,ind1,ind2]
        @param ref_sf dict: subfield element specific information, containing keys [code,value]
        @return bool: true if a datafield with the subfield are found
        """
        element = self._etree.xpath(
            ".//datafield[@ind1='{ind1}' and @ind2='{ind2}' and @tag='{tag}']//subfield[@code='{code}']".format(
                **ref_df, code=ref_sf["code"]
            )
        )
        return element and len(element) > 0 and element[0].text == ref_sf["value"]

    def emplace_leader(
        self,
        value: str = "",
    ):
        """Change leader string in record."""
        for leader in self._etree.iter("leader"):
            leader.text = value

    def emplace_controlfield(
        self,
        tag: str = "",
        value: str = "",
    ):
        """Add value to record for given datafield and subfield."""
        controlfield = etree.Element("controlfield", tag=tag)
        controlfield.text = value
        self._etree.append(controlfield)

    def emplace_field(
        self,
        tag: str = "",
        ind1: str = " ",
        ind2: str = " ",
        code: str = "",
        value: str = "",
    ) -> None:
        """Add value to record for given datafield and subfield."""
        datafield = etree.Element(
            "datafield", tag=tag, ind1=ind1, ind2=ind2
        )
        subfield = etree.Element("subfield", code=code)
        subfield.text = value
        datafield.append(subfield)
        self._etree.append(datafield)

    def emplace_unique_field(
        self,
        tag: str = "",
        ind1: str = " ",
        ind2: str = " ",
        code: str = "",
        value: str = "",
    ):
        """Add value to record if it doesn't already contain it."""
        datafield = self._etree.xpath(
            f".//datafield[@ind1='{ind1}' and @ind2='{ind2}' and @tag='{tag}']"
        )
        if not datafield:
            datafield = etree.Element(
                "datafield", tag=tag, ind1=ind1, ind2=ind2
            )  # DataField(tag, ind1, ind2)
        else:
            datafield = datafield[0]
        subfield = self._etree.xpath(f".//subfield[@code='{code}']")
        if not subfield:
            subfield = etree.Element("subfield", code=code)
            subfield.text = value
            datafield.append(subfield)
            self._etree.append(datafield)

    def is_valid_marc21_xml_string(self) -> bool:
        """Validate the record against a Marc21XML Schema."""
        with open(
            join(dirname(__file__), "schema", "MARC21slim.xsd"), "r", encoding="utf-8"
        ) as fp:
            marc21xml_schema = etree.XMLSchema(etree.parse(fp))
            marc21xml = etree.parse(StringIO(self.xml))
            return marc21xml_schema.validate(marc21xml)
