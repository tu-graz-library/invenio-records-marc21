# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Tests for record MetadataSchema."""

import pytest
from lxml import etree

from invenio_records_marc21.services.record import Marc21Metadata


def test_create_metadata():

    metadata = Marc21Metadata()

    assert '<record xmlns="http://www.loc.gov/MARC21/slim"' in metadata.xml
    assert 'type="Bibliographic"' in metadata.xml

    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )

    assert '<datafield tag="245" ind1="1" ind2="0">' in metadata.xml
    assert '<subfield code="a">laborum sunt ut nulla</subfield>' in metadata.xml


def test_validate_metadata():
    metadata = Marc21Metadata()

    assert metadata.is_valid_marc21_xml_string()
    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )
    assert metadata.is_valid_marc21_xml_string()

    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="", value="laborum sunt ut nulla"
    )

    assert not metadata.is_valid_marc21_xml_string()


def test_subfield_metadata():
    metadata = Marc21Metadata()

    leader = metadata.etree.find(".//leader")
    assert leader.text == "00000nam a2200000zca4500"

    assert not metadata.etree.find(".//datafield")

    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )

    datafield = metadata.etree.find(".//datafield")
    assert datafield
    assert not datafield.text
    assert len(metadata.etree.findall(".//datafield")) == 1
    assert datafield.attrib == {"tag": "245", "ind1": "1", "ind2": "0"}

    subfield = metadata.etree.find(".//subfield")
    assert subfield is not None
    assert len(datafield.findall(".//subfield")) == 1
    assert subfield.attrib == {"code": "a"}
    assert subfield.text == "laborum sunt ut nulla"

    metadata.emplace_field(
        tag="245", ind1="1", ind2="0", code="b", value="laborum sunt ut nulla"
    )

    assert len(metadata.etree.findall(".//datafield")) == 2
    assert len(metadata.etree.findall(".//subfield")) == 2

    assert metadata.is_valid_marc21_xml_string()


def test_controlfields_metadata():
    metadata = Marc21Metadata()

    assert "<controlfield" not in metadata.xml
    assert not metadata.etree.find(".//controlfield")

    metadata.emplace_controlfield(tag="123", value="laborum sunt ut nulla")

    controlfield = metadata.etree.find(".//controlfield")
    assert controlfield is not None
    assert controlfield.text == "laborum sunt ut nulla"
    assert controlfield.attrib == {"tag": "123"}
    assert len(metadata.etree.findall(".//controlfield")) == 1

    assert '<controlfield tag="123">laborum sunt ut nulla' in metadata.xml


def test_uniqueness_metadata():
    metadata = Marc21Metadata()
    metadata.emplace_unique_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )

    datafield = metadata.etree.find(".//datafield")
    assert datafield is not None
    assert not datafield.text
    assert len(metadata.etree.findall(".//datafield")) == 1
    assert datafield.attrib == {"tag": "245", "ind1": "1", "ind2": "0"}

    subfield = metadata.etree.find(".//subfield")
    assert subfield is not None
    assert len(datafield.findall(".//subfield")) == 1
    assert subfield.attrib == {"code": "a"}
    assert subfield.text == "laborum sunt ut nulla"

    metadata.emplace_unique_field(
        tag="245", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )

    datafield = metadata.etree.find(".//datafield")
    assert datafield
    assert not datafield.text
    assert len(metadata.etree.findall(".//datafield")) == 1
    assert datafield.attrib == {"tag": "245", "ind1": "1", "ind2": "0"}

    subfield = metadata.etree.find(".//subfield")
    assert subfield is not None
    assert len(datafield.findall(".//subfield")) == 1
    assert subfield.attrib == {"code": "a"}
    assert subfield.text == "laborum sunt ut nulla"

    assert metadata.is_valid_marc21_xml_string()


def test_contains_metadata():
    metadata = Marc21Metadata()

    assert not metadata.contains(
        ref_df={"tag": "245", "ind1": "1", "ind2": "0"},
        ref_sf={"code": "a", "value": "laborum sunt ut nulla"},
    )
    metadata.emplace_field(
        tag="246", ind1="1", ind2="0", code="a", value="laborum sunt ut nulla"
    )
    assert not metadata.contains(
        ref_df={"tag": "246", "ind1": "1", "ind2": "0"},
        ref_sf={"code": "b", "value": "laborum sunt ut nulla"},
    )

    assert metadata.contains(
        ref_df={"tag": "246", "ind1": "1", "ind2": "0"},
        ref_sf={"code": "a", "value": "laborum sunt ut nulla"},
    )


def test_load_metadata():
    metadata = Marc21Metadata()

    etree_metadata = etree.Element("record")
    control = etree.Element("controlfield", tag="001")
    control.text = "990079940640203331"
    etree_metadata.append(control)

    datafield = etree.Element("datafield", tag="245", ind1="0", ind2="0")
    title = etree.Element("subfield", code="a")
    title.text = "International Brain-Computer Interface"
    datafield.append(title)

    subtitle = etree.Element("subfield", code="b")
    subtitle.text = "Subtitle field"
    datafield.append(subtitle)

    etree_metadata.append(datafield)

    metadata.load(etree_metadata)
    assert metadata._etree == etree_metadata

    controlfield = metadata._etree.xpath(".//controlfield[@tag='001']")
    assert controlfield
    assert len(controlfield) == 1
    assert controlfield[0].text == "990079940640203331"

    datafield = metadata._etree.xpath(".//datafield[@tag='245' and @ind2='0' and @ind1='0']")
    assert datafield
    assert len(datafield) == 1

    title_field = datafield[0].xpath(".//subfield[@code='a']")

    assert title_field
    assert len(title_field) == 1
    assert title_field[0].text == "International Brain-Computer Interface"

    subfields = datafield[0].xpath(".//subfield[@code='b']")

    assert subfields
    assert len(subfields) == 1
    subfields[0].text = "Subtitle field"


def test_xml_type():
    metadata = Marc21Metadata()

    test = '<datafield tag="245" ind1="0" ind2="0"></datafield>'
    metadata.xml = test
    assert metadata.xml

    test = {}
    with pytest.raises(TypeError):
        metadata.xml = test


def test_json_type():
    metadata = Marc21Metadata()

    test = dict()
    metadata.json = test
    assert "metadata" in metadata.json.keys()

    test = ""
    with pytest.raises(TypeError):
        metadata.json = test
