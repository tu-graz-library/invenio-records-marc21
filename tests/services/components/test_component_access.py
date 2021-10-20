# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Tests for the service AccessComponent."""

from datetime import timedelta

import arrow
import pytest
from flask_principal import Identity, UserNeed

from invenio_records_marc21.proxies import current_records_marc21
from invenio_records_marc21.records import Marc21Record
from invenio_records_marc21.services.components import AccessComponent


def test_component_access_default_access(parent, identity_simple):
    marc21_record = {"metadata": {"json": {}}}
    record = Marc21Record.create(data=marc21_record, parent=parent)
    component = AccessComponent(current_records_marc21.records_service)
    component.create(identity=identity_simple, data=marc21_record, record=record)

    prot = record.access.protection
    assert prot.record == "public"
    assert prot.files == "public"

    assert len(record.parent.access.owners) > 0
    assert record.parent.access.owners[0].owner_id == identity_simple.id


def test_component_access_update_access_via_json(
    marc21_record, parent, identity_simple
):
    next_year = arrow.utcnow().datetime + timedelta(days=+365)
    restricted_access = {
        "record": "restricted",
        "files": "restricted",
        "embargo": {
            "until": next_year.strftime("%Y-%m-%d"),
            "active": True,
            "reason": "Because I can.",
        },
    }
    marc21_record["access"] = restricted_access

    record = Marc21Record.create(marc21_record, parent=parent)
    component = AccessComponent(current_records_marc21.records_service)
    component.create(identity_simple, marc21_record, record)

    prot = record.access.protection
    assert record.access.embargo is not None
    assert "embargo" in record["access"]
    assert prot.record == record["access"]["record"] == "restricted"
    assert prot.files == record["access"]["files"] == "restricted"

    new_data = marc21_record.copy()
    new_data["access"] = {
        "record": "public",
        "files": "public",
    }
    component.create(identity_simple, new_data, record)

    prot = record.access.protection
    assert not record.access.embargo
    assert "embargo" not in record["access"]
    assert prot.record == record["access"]["record"] == "public"
    assert prot.files == record["access"]["files"] == "public"
