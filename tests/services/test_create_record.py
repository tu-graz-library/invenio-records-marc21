# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 records service tests."""

from datetime import timedelta

import arrow
import pytest


def _assert_fields_exists(fields, data):
    for key in fields:
        assert key in data


def _assert_fields(fields, values, expected):
    for key in fields:
        assert values[key] == expected[key]


@pytest.fixture()
def marc21():
    """marc21 record."""
    return {"metadata": {"fields": {}, "leader": ""}}


def test_create_with_service(running_app, service, marc21):
    adminuser_identity = running_app.adminuser_identity

    draft = service.create(data=marc21, identity=adminuser_identity, access=None)

    root_fields = [
        "id",
        "versions",
        "links",
        "is_published",
        "parent",
        "revision_id",
        "created",
        "updated",
        "metadata",
    ]
    expected = {"metadata": {"fields": {}, "leader": ""}}
    _assert_fields_exists(root_fields, draft.data)
    # TODO: the doi 024 field exists
    # _assert_fields(["metadata"], draft.data, expected)
    assert not draft["is_published"]

    record = service.publish(id_=draft.id, identity=adminuser_identity)

    assert record
    _assert_fields_exists(root_fields, record.data)
    # TODO: the doi 024 field exists
    # _assert_fields(["metadata"], record.data, expected)
    assert record["is_published"]


@pytest.fixture()
def empty_data():
    """marc21 record."""
    return {"metadata": {"fields": {}, "leader": ""}}


@pytest.mark.parametrize(
    "access",
    [
        {
            "input": {
                "record": "public",
            },
            "expect": {
                "access": {
                    "record": "public",
                    "files": "public",
                    "embargo": {
                        "active": False,
                        "reason": None,
                    },
                    "status": "metadata-only",
                },
            },
        },
        {
            "input": {
                "record": "restricted",
                "files": "restricted",
            },
            "expect": {
                "access": {
                    "files": "restricted",
                    "record": "restricted",
                    "embargo": {
                        "active": False,
                        "reason": None,
                    },
                    "status": "restricted",
                },
            },
        },
        {
            "input": {
                "record": "restricted",
                "embargo": {
                    "until": (arrow.utcnow().datetime + timedelta(days=2)).strftime(
                        "%Y-%m-%d"
                    ),
                    "active": True,
                    "reason": "Because I can!",
                },
            },
            "expect": {
                "access": {
                    "files": "restricted",
                    "record": "restricted",
                    "embargo": {
                        "until": (arrow.utcnow().datetime + timedelta(days=2)).strftime(
                            "%Y-%m-%d"
                        ),
                        "active": True,
                        "reason": "Because I can!",
                    },
                    "status": "embargoed",
                },
            },
        },
    ],
)
def test_create_with_access(running_app, service, empty_data, access):
    adminuser_identity = running_app.adminuser_identity

    draft = service.create(
        identity=adminuser_identity, data=empty_data, access=access["input"]
    )
    record = service.publish(id_=draft.id, identity=adminuser_identity)
    _assert_fields(
        ["access"],
        record.data,
        access["expect"],
    )
