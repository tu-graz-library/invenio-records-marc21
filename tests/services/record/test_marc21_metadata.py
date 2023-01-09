# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Tests for record MetadataSchema."""

from xml.etree.ElementTree import Element

import pytest

from invenio_records_marc21.services.record import Marc21Metadata


def test_create_metadata():
    """Test constructor and emplace_datafield method."""
    metadata = Marc21Metadata()

    assert '<record xmlns="http://www.loc.gov/MARC21/slim">' in metadata.xml

    metadata.emplace_datafield(selector="245.1.0.a", value="laborum sunt ut nulla")

    assert '<datafield tag="245" ind1="1" ind2="0">' in metadata.xml
    assert '<subfield code="a">laborum sunt ut nulla</subfield>' in metadata.xml


def test_validate_metadata():
    """Test the construction and emplace_datafield method."""
    metadata = Marc21Metadata()
    expected_json = {"metadata": {"leader": "00000nam a2200000zca4500", "fields": {}}}

    assert metadata.json == expected_json

    metadata.emplace_datafield(selector="245.1.0.a", value="laborum sunt ut nulla")
    expected_json = {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {"a": ["laborum sunt ut nulla"]},
                    }
                ]
            },
        }
    }
    assert metadata.json == expected_json

    metadata.emplace_datafield(
        selector="245.1.0.", value="laborum sunt ut nulla et infinitum"
    )
    expected_json = {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {"a": ["laborum sunt ut nulla"]},
                    },
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {"a": ["laborum sunt ut nulla et infinitum"]},
                    },
                ]
            },
        }
    }

    assert metadata.json == expected_json


def test_subfield_metadata():
    """Test the construction and emplace_datafield method."""
    metadata = Marc21Metadata()

    leader = metadata.etree.find(".//leader")
    assert leader.text == "00000nam a2200000zca4500"

    assert not metadata.etree.find(".//datafield")

    metadata.emplace_datafield(selector="245.1.0.a", value="laborum sunt ut nulla")

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

    metadata.emplace_datafield(selector="245.1.0.b", value="laborum sunt ut nulla")

    assert len(metadata.etree.findall(".//datafield")) == 2
    assert len(metadata.etree.findall(".//subfield")) == 2

    expected_json = {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {"a": ["laborum sunt ut nulla"]},
                    },
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {"b": ["laborum sunt ut nulla"]},
                    },
                ]
            },
        }
    }

    assert metadata.json == expected_json


def test_controlfields_metadata():
    """Test controlfield."""
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


def test_load_metadata():
    """Test constructor."""
    etree_metadata = Element("record")
    control = Element("controlfield", tag="001")
    control.text = "990079940640203331"
    etree_metadata.append(control)

    datafield = Element("datafield", tag="245", ind1="0", ind2="0")
    title = Element("subfield", code="a")
    title.text = "International Brain-Computer Interface"
    datafield.append(title)

    subtitle = Element("subfield", code="b")
    subtitle.text = "Subtitle field"
    datafield.append(subtitle)

    etree_metadata.append(datafield)

    metadata = Marc21Metadata(metadata=etree_metadata)
    assert metadata.etree == etree_metadata


def test_xml_type():
    """Test type of xml."""
    metadata = Marc21Metadata()

    test = '<datafield tag="245" ind1="0" ind2="0"></datafield>'
    metadata.xml = test
    assert metadata.xml

    test = {}
    with pytest.raises(TypeError):
        metadata.xml = test


@pytest.mark.skip(reason="the json setter is not implemented in a correct way")
def test_json_type():
    """Test type of json."""
    metadata = Marc21Metadata()

    test = {}
    metadata.json = test
    assert "metadata" in metadata.json.keys()

    test = ""
    with pytest.raises(TypeError):
        metadata.json = test
