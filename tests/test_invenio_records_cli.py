# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module cli tests."""


from datetime import timedelta

import arrow
import pytest

from invenio_records_marc21.cli import marc21
from invenio_records_marc21.fixtures.demo import (
    create_fake_record,
    fake_access_right,
    fake_feature_date,
)


def test_fake_access_right():
    """Test random access right for demo."""
    access = fake_access_right()
    assert access in ["public", "restricted", "embargoed"]


def test_fake_feature_date():
    """Test create future date for demo."""
    assert isinstance(fake_feature_date(), str)
    date = fake_feature_date(days=30)
    start_date = arrow.utcnow().datetime
    assert isinstance(date, str)
    date_arrow = arrow.get(date)
    assert date_arrow >= arrow.get(start_date.date() + timedelta(days=1))
    assert date_arrow < arrow.get(start_date.date() + timedelta(days=30))


def test_fake_demo_record_creation(running_app, adminuser_identity, search_clear):
    """Test create fake full record with marc21 service."""
    app = running_app.app

    with app.app_context():
        record = create_fake_record()
        assert isinstance(record, dict)


def test_cli_create_demo_record(running_app, cli_runner, adminuser, search_clear):
    """Test cli marc21 demo record."""
    args = [
        "demo",
        "-u",
        adminuser.email,
        "-n",
        "1",
    ]
    result = cli_runner(marc21, *args)
    assert result.exit_code == 0
    assert result.output == "Creating demo records...\nCreated records!\n"


def test_cli_create_demo_metadata(running_app, cli_runner, adminuser, search_clear):
    """Test cli marc21 demo metadata."""
    args = [
        "demo",
        "-u",
        adminuser.email,
        "-n",
        "1",
    ]
    result = cli_runner(marc21, *args)
    assert result.exit_code == 0
    assert result.output == "Creating demo records...\nCreated records!\n"
