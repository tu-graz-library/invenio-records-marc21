# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Tests for Resources marc21 serializer."""

import json

from invenio_records_marc21.resources.serializers import (
    Marc21JSONSerializer,
    Marc21XMLSerializer,
)
from invenio_records_marc21.resources.serializers.schema import Marc21Schema


def _test_key_in_serialized_obj(obj, keys, exept_keys):
    for key in keys:
        assert key in obj
    for no_key in exept_keys:
        assert no_key not in obj


def test_marcxml_serializer_init():
    marc = Marc21XMLSerializer()
    assert isinstance(marc.object_schema, Marc21Schema)


def test_marcxml_serializer_serialize_object(full_record):
    marc = Marc21XMLSerializer()
    test_keys = ["metadata", "id", "files"]
    exept_keys = ["pid", "access"]
    obj = marc.serialize_object(full_record)
    assert isinstance(obj, str)
    _test_key_in_serialized_obj(obj, test_keys, exept_keys)
    assert obj.startswith("<?xml version='1.0' encoding='UTF-8'?>")


def test_marcxml_serializer_serialize_object_list(list_records):
    test_keys = ["metadata", "id", "files"]
    exept_keys = ["pid", "access"]
    marc = Marc21XMLSerializer()
    obj_list = marc.serialize_object_list(list_records)
    assert isinstance(obj_list, str)
    test_obj = obj_list.split(":record>\n\n")
    for obj in test_obj:
        assert isinstance(obj, str)
        _test_key_in_serialized_obj(obj, test_keys, exept_keys)
        assert obj.startswith("<?xml version='1.0' encoding='UTF-8'?>")


def test_json_serializer_init():
    marc = Marc21JSONSerializer()
    assert isinstance(marc.object_schema, Marc21Schema)


def test_json_serializer_serialize_object(full_record):
    test_keys = ["metadata", "id", "files"]
    exept_keys = ["pid", "access"]
    marc = Marc21JSONSerializer()
    obj = marc.serialize_object(full_record)
    assert isinstance(obj, str)
    _test_key_in_serialized_obj(obj, test_keys, exept_keys)


def test_json_serializer_serialize_object_list(list_records):
    test_keys = ["metadata", "id", "files"]
    exept_keys = ["pid", "access"]
    marc = Marc21JSONSerializer()
    obj_list = marc.serialize_object_list(list_records)
    assert isinstance(obj_list, str)
    test_obj = json.loads(obj_list)
    for obj in test_obj["hits"]["hits"]:
        _test_key_in_serialized_obj(obj, test_keys, exept_keys)
