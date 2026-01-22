# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Tests for the record PIDField."""

from invenio_records_resources.records.systemfields import PIDField
from sqlalchemy import inspect

from invenio_records_marc21.records.api import Marc21Record
from invenio_records_marc21.records.models import Marc21RecordMetadata
from invenio_records_marc21.records.systemfields import (
    MarcPIDFieldContext,
    MarcRecordProvider,
    MarcResolver,
)


def test_class_attribute_pid():
    """Test that field is returned."""
    assert isinstance(Marc21Record.pid, MarcPIDFieldContext)


def test_record_pid_creation(testapp, db):
    """Test record creation."""
    record = Marc21Record.create({})
    assert record["id"] == record.pid.pid_value
    assert record["pid"]["pk"] == record.pid.id
    assert record["pid"]["status"] == record.pid.status
    assert record["pid"]["obj_type"] == record.pid.object_type
    assert record["pid"]["pid_type"] == record.pid.pid_type
    assert record.id == record.pid.object_uuid


def test_create_no_provider(testapp, db):
    """Test creation without a provider."""

    class Record(Marc21Record):
        model_cls = Marc21RecordMetadata
        pid = PIDField()

    record = Record.create({})
    assert record.pid is None

    record.pid = MarcRecordProvider.create(object_type="rec", object_uuid=record.id).pid

    assert record["id"] == record.pid.pid_value
    assert record["pid"]["pk"] == record.pid.id
    assert record["pid"]["status"] == record.pid.status
    assert record["pid"]["obj_type"] == record.pid.object_type
    assert record["pid"]["pid_type"] == record.pid.pid_type
    assert record.id == record.pid.object_uuid


def test_create_different_key(testapp, db):
    """Test creation with different key."""

    class Record(Marc21Record):
        model_cls = Marc21RecordMetadata

        pid = PIDField(
            key="id",
            provider=MarcRecordProvider,
            context_cls=MarcPIDFieldContext,
            resolver_cls=MarcResolver,
            delete=False,
        )

    record = Record.create({})
    assert record["id"] == record.pid.pid_value
    assert record["pid"]["pid_type"] == record.pid.pid_type


def test_reading_a_pid(testapp, db):
    """Test reading from dict."""
    record = Marc21Record(
        {
            "id": "0scgd-ps972",
            "pid": {
                "pid_type": "marcid",
                "obj_type": "rec",
                "pk": 10,
                "status": "R",
            },
        }
    )
    assert record.pid is not None
    assert record["id"] == record.pid.pid_value
    assert record["pid"]["pk"] == record.pid.id
    assert record["pid"]["status"] == record.pid.status
    assert record["pid"]["obj_type"] == record.pid.object_type
    assert record["pid"]["pid_type"] == record.pid.pid_type
