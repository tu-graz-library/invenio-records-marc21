# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Tests for Resources UI marc21 serializer."""


from invenio_records_marc21.resources.serializers.ui import Marc21UIJSONSerializer
from invenio_records_marc21.resources.serializers.ui.schema import Marc21UISchema


def test_ui_json_serializer_init():
    marc = Marc21UIJSONSerializer()
    assert marc._object_key == "ui"
    assert isinstance(marc.object_schema, Marc21UISchema)


def test_ui_json_serializer_dump_obj(full_record):
    marc = Marc21UIJSONSerializer()
    obj = marc.dump_obj(full_record)

    assert isinstance(obj["metadata"], dict)
    assert full_record["metadata"] == obj["metadata"]

    assert marc._object_key in obj
    obj_ui = obj[marc._object_key]
    assert "metadata" in obj_ui
    assert isinstance(obj_ui["metadata"], dict)


def test_ui_json_serializer_dump_list(list_records):
    marc = Marc21UIJSONSerializer()
    obj_list = marc.dump_list(list_records)
    for record, obj in zip(obj_list["hits"]["hits"], list_records["hits"]["hits"]):
        assert marc._object_key in obj

        assert "metadata" in obj
        assert record["metadata"] == obj["metadata"]

        obj_ui = obj[marc._object_key]
        assert "metadata" in obj_ui
        assert isinstance(obj_ui["metadata"], dict)
