# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Tests for Resources UI marc21 serializer."""


from invenio_records_marc21.resources.serializers.ui import Marc21UIJSONSerializer
from invenio_records_marc21.resources.serializers.ui.schema import Marc21UISchema


def test_ui_json_serializer_init() -> None:
    marc = Marc21UIJSONSerializer()
    assert isinstance(marc.object_schema, Marc21UISchema)


def test_ui_json_serializer_dump_obj(full_record: dict) -> None:
    marc = Marc21UIJSONSerializer()
    obj = marc.dump_obj(full_record)

    expected = {
        "languages": [],
        "authors": [{"a": ["Philipp"], "8": []}],
        "titles": ["The development of high strain actuator materials"],
        "copyright": [],
        "description": "",
        "notes": [],
        "resource_type": "",
        "published": "",
        "publisher": "TU Graz",
        "license": {"url": "", "short": ""},
        "youtube": "",
        "isbn": None,
    }
    assert isinstance(obj["metadata"], dict)
    assert expected == obj["metadata"]


def test_ui_json_serializer_dump_list(list_records: list) -> None:
    marc = Marc21UIJSONSerializer()
    obj_list = marc.dump_list(list_records)
    for record, obj in zip(obj_list["hits"]["hits"], list_records["hits"]["hits"]):
        assert "metadata" in obj
        assert record["metadata"] == obj["metadata"]
