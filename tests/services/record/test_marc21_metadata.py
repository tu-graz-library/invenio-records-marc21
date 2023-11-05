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

    assert "<ns0:record" in metadata.xml
    assert 'xmlns="http://www.loc.gov/MARC21/slim"' in metadata.xml

    metadata.emplace_datafield(selector="245.1.0.a", value="laborum sunt ut nulla")

    assert '<ns0:datafield tag="245" ind1="1" ind2="0">' in metadata.xml
    assert '<ns0:subfield code="a">laborum sunt ut nulla</ns0:subfield>' in metadata.xml


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
    namespaces = {"ns0": "http://www.loc.gov/MARC21/slim"}

    leader = metadata.etree.find(".//ns0:leader", namespaces)
    assert leader.text == "00000nam a2200000zca4500"

    assert not metadata.etree.find(".//ns0:datafield", namespaces)

    metadata.emplace_datafield(selector="245.1.0.a", value="laborum sunt ut nulla")

    datafield = metadata.etree.find(".//ns0:datafield", namespaces)
    assert datafield
    assert not datafield.text
    assert len(metadata.etree.findall(".//ns0:datafield", namespaces)) == 1
    assert datafield.attrib == {"tag": "245", "ind1": "1", "ind2": "0"}

    subfield = metadata.etree.find(".//ns0:subfield", namespaces)
    assert subfield is not None
    assert len(datafield.findall(".//ns0:subfield", namespaces)) == 1
    assert subfield.attrib == {"code": "a"}
    assert subfield.text == "laborum sunt ut nulla"

    metadata.emplace_datafield(selector="245.1.0.b", value="laborum sunt ut nulla")

    assert len(metadata.etree.findall(".//ns0:datafield", namespaces)) == 2
    assert len(metadata.etree.findall(".//ns0:subfield", namespaces)) == 2

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
    namespaces = {"ns0": "http://www.loc.gov/MARC21/slim"}

    assert "<ns0:controlfield" not in metadata.xml
    assert not metadata.etree.find(".//ns0:controlfield", namespaces)

    metadata.emplace_controlfield(tag="123", value="laborum sunt ut nulla")

    controlfield = metadata.etree.find(".//ns0:controlfield", namespaces)
    assert controlfield is not None
    assert controlfield.text == "laborum sunt ut nulla"
    assert controlfield.attrib == {"tag": "123"}
    assert len(metadata.etree.findall(".//ns0:controlfield", namespaces)) == 1

    assert '<ns0:controlfield tag="123">laborum sunt ut nulla' in metadata.xml


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


def test_get_field(marc21_record, full_metadata):
    """Test get field."""
    namespaces = {"ns0": "http://www.loc.gov/MARC21/slim"}
    marc21_records = [
        Marc21Metadata(json=marc21_record["metadata"]),
        full_metadata,
    ]

    for record in marc21_records:
        assert record.get_value(category="001") == "990004519310204517"
        assert record.get_value(category="264", subf_code="b") == "TU Graz"
        assert record.get_value(category="264", subf_code="x") == ""
        assert (
            record.get_value(category="264", ind1=" ", ind2="1", subf_code="c")
            == "2012"
        )
        assert record.get_values(category="264") == ["TU Graz", "2012"]

        _, datafields = record.get_fields(category="971", ind1="7", ind2=" ")

        assert (
            datafields[0]
            .findall("{http://www.loc.gov/MARC21/slim}subfield[@code='a']")[0]
            .text
            == "gesperrt"
        )

        assert (
            datafields[0].findall("ns0:subfield[@code='a']", namespaces)[0].text
            == "gesperrt"
        )

        assert (
            record.exists_field(
                category="971", ind1="7", ind2=" ", subf_code="a", subf_value="gesperrt"
            )
            is True
        )
        assert (
            record.exists_field(
                category="971", ind1="7", ind2=" ", subf_code="a", subf_value="world"
            )
            is False
        )
