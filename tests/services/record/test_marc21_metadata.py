# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Tests for record MetadataSchema."""

import pytest

from invenio_records_marc21.services.record import Marc21Metadata


def test_create_metadata():
    """Test constructor and emplace_datafield method."""
    metadata = Marc21Metadata()

    expected = {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {},
        },
    }

    assert metadata.json == expected

    metadata.emplace_datafield(selector="245.1.0.a", value="laborum sunt ut nulla")

    expected = {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {"a": ["laborum sunt ut nulla"]},
                    },
                ],
            },
        },
    }
    assert metadata.json == expected


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
                        "subfields": {
                            "a": [
                                "laborum sunt ut nulla",
                                "laborum sunt ut nulla et infinitum",
                            ]
                        },
                    },
                ]
            },
        }
    }
    assert metadata.json == expected_json


def test_subfield_metadata():
    """Test the construction and emplace_datafield method."""
    metadata = Marc21Metadata()

    metadata.emplace_datafield(selector="245.1.0.a", value="laborum sunt ut nulla")
    metadata.emplace_datafield(selector="245.1.0.b", value="laborum sunt ut nulla")

    expected_json = {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {
                            "a": ["laborum sunt ut nulla"],
                            "b": ["laborum sunt ut nulla"],
                        },
                    },
                ]
            },
        }
    }

    assert metadata.json == expected_json


def test_controlfields_metadata():
    """Test controlfield."""
    metadata = Marc21Metadata()

    metadata.emplace_controlfield(tag="002", value="laborum sunt ut nulla")

    expected_json = {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {"002": "laborum sunt ut nulla"},
        }
    }

    assert metadata.json == expected_json

    with pytest.raises(RuntimeError):
        metadata.emplace_controlfield(tag="123", value="laborum sunt ut nulla")


def test_json_type():
    """Test type of json."""
    with pytest.raises(TypeError):
        metadata = Marc21Metadata(json={"leader": ""})

    with pytest.raises(TypeError):
        metadata = Marc21Metadata(json={"fields": {}})

    with pytest.raises(TypeError):
        metadata = Marc21Metadata(json={"fields": ""})

    metadata = Marc21Metadata()
    with pytest.raises(TypeError):
        metadata.json = {}


def test_get_field(marc21_record, full_metadata):
    """Test get field."""
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

        assert datafields[0]["subfields"]["a"] == ["gesperrt"]

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
