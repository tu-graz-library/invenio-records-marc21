# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Tests for the record Pid Providers."""

import uuid

import pytest
from invenio_pidstore.models import PIDStatus

from invenio_records_marc21.records.systemfields import (
    MarcDraftProvider,
    MarcRecordProvider,
)


def test_record_provider(app, db):
    """Test MarcRecordProvider."""
    with app.app_context():
        provider = MarcRecordProvider.create()
        assert provider.pid
        assert provider.pid.pid_type == "marcid"
        assert provider.pid.pid_value
        assert provider.pid.pid_provider is None
        assert provider.pid.status == PIDStatus.RESERVED
        assert provider.pid.object_type is None
        assert provider.pid.object_uuid is None

        # Assign to object immediately
        rec_uuid = uuid.uuid4()
        provider = MarcRecordProvider.create(object_type="rec", object_uuid=rec_uuid)
        assert provider.pid
        assert provider.pid.pid_type == "marcid"
        assert provider.pid.pid_value
        assert provider.pid.pid_provider is None
        assert provider.pid.status == PIDStatus.REGISTERED
        assert provider.pid.object_type == "rec"
        assert provider.pid.object_uuid == rec_uuid


def test_draft_provider(app, db):
    """Test MarcDraftProvider."""
    with app.app_context():
        provider = MarcDraftProvider.create()
        assert provider.pid
        assert provider.pid.pid_type == "marcid"
        assert provider.pid.pid_value
        assert provider.pid.pid_provider is None
        assert provider.pid.status == PIDStatus.RESERVED
        assert provider.pid.object_type is None
        assert provider.pid.object_uuid is None

        # Assign to object immediately
        rec_uuid = uuid.uuid4()
        provider = MarcDraftProvider.create(object_type="rec", object_uuid=rec_uuid)
        assert provider.pid
        assert provider.pid.pid_type == "marcid"
        assert provider.pid.pid_value
        assert provider.pid.pid_provider is None
        assert provider.pid.status == PIDStatus.NEW
        assert provider.pid.object_type == "rec"
        assert provider.pid.object_uuid == rec_uuid


def test_invalid_pid_value(app, db):
    with app.app_context():
        with pytest.raises(AssertionError):
            MarcRecordProvider.create(pid_value="3")
