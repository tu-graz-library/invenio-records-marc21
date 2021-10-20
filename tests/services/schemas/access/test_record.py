# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test record AccessSchema."""


from datetime import timedelta

import arrow
import pytest
from flask_babelex import lazy_gettext as _
from invenio_rdm_records.services.schemas.access import AccessSchema
from marshmallow import ValidationError
from marshmallow.exceptions import ValidationError


def test_valid_full():
    valid_full = {
        "record": "restricted",
        "embargo": {
            "until": (arrow.utcnow().datetime + timedelta(days=2)).strftime("%Y-%m-%d"),
            "active": True,
            "reason": "Because I can!",
        },
        "files": "public",
    }
    assert valid_full == AccessSchema().load(valid_full)


@pytest.mark.parametrize("value", ["public", "restricted"])
def test_valid_metadata_protection(value):
    assert AccessSchema().validate_record_protection(value) is None


def test_invalid_metadata_protection():
    with pytest.raises(ValidationError) as e:
        AccessSchema().validate_record_protection("invalid")
    assert e.value.messages[0] == _("'record' must be either 'public' or 'restricted'")
    assert e.value.field_name == "record"


@pytest.mark.parametrize("value", ["public", "restricted"])
def test_valid_files_protection(value):
    assert AccessSchema().validate_files_protection(value) is None


def test_invalid_files_protection():
    with pytest.raises(ValidationError) as e:
        AccessSchema().validate_files_protection("invalid")
    assert e.value.messages[0] == _("'files' must be either 'public' or 'restricted'")
    assert e.value.field_name == "record"
