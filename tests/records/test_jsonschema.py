# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""JSONSchema tests."""

import json
from os.path import dirname, join

import pytest
from jsonschema.exceptions import ValidationError

from invenio_records_marc21.records import Marc21Record as Record


#
# Assertion helpers
#
def validates(data):
    """Assertion function used to validate according to the schema."""
    data["$schema"] = "local://marc21/marc21-v1.0.0.json"
    Record(data).validate()
    return True


def validates_meta(data):
    """Validate metadata fields."""
    return validates({"metadata": data})


def fails(data):
    """Assert that validation fails."""
    pytest.raises(ValidationError, validates, data)
    return True


def fails_meta(data):
    """Assert that validation fails for metadata."""
    pytest.raises(ValidationError, validates_meta, data)
    return True


#
# Fixtures
#


def _load_json(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        return json.load(fp)


#
# Tests internal/external identifiers
#
def test_id(appctx):
    """Test id."""
    assert validates({"id": "12345-abcd"})
    assert fails({"id": 1})


@pytest.mark.parametrize("prop", ["pid"])
def test_pid(appctx, prop):
    """Test pid."""
    pid = {
        "pk": 1,
        "status": "R",
    }
    assert validates({prop: pid})

    # Valid status
    for s in ["N", "K", "R", "M", "D"]:
        pid["status"] = s
        assert validates({prop: pid})

    # Invalid status
    pid["status"] = "INVALID"
    assert fails({prop: pid})

    # Extra propert
    pid["invalid"] = "1"
    assert fails({prop: pid})


def test_pids(appctx):
    """Test external pids."""
    assert validates(
        {
            "pids": {
                "doi": {
                    "identifier": "10.12345",
                    "provider": "datacite",
                    "client": "test",
                }
            }
        }
    )
    assert validates(
        {
            "pids": {
                "doi": {
                    "identifier": "10.12345",
                    "provider": "datacite",
                    "client": "test",
                },
                "oai": {"identifier": "oai:10.12345", "provider": "local"},
            }
        }
    )
    # Extra property
    assert fails(
        {
            "pids": {
                "oai": {
                    "identifier": "oai:10.12345",
                    "provider": "local",
                    "invalid": "test",
                }
            }
        }
    )
    # Not a string
    assert fails({"pids": {"oai": {"identifier": 1, "provider": "local"}}})


#
# Tests metadata
#
def test_metadata(appctx):
    """Test empty metadata."""
    assert validates({"metadata": {"fields": [], "leader": ""}})
