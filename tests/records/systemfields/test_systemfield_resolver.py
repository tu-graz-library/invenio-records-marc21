# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Tests for the record Pid Resolver."""

import uuid

import pytest
from invenio_pidstore.errors import (
    PIDDeletedError,
    PIDDoesNotExistError,
    PIDMissingObjectError,
    PIDRedirectedError,
)
from invenio_pidstore.models import PersistentIdentifier, PIDStatus

from invenio_records_marc21.records.systemfields import MarcResolver


def test_marc_resolver(app, db):
    """Test the class methods of PersistentIdentifier class."""

    with app.app_context():
        rec_a = uuid.uuid4()
        PersistentIdentifier.create("marcid", 1, status=PIDStatus.NEW)

        PersistentIdentifier.create(
            "marcid", 2, status=PIDStatus.NEW, object_type="rec", object_uuid=rec_a
        )
        PersistentIdentifier.create("marcid", 3, status=PIDStatus.RESERVED)
        PersistentIdentifier.create("marcid", 4, status=PIDStatus.REGISTERED)
        PersistentIdentifier.create(
            "marcid",
            5,
            status=PIDStatus.REGISTERED,
            object_type="rec",
            object_uuid=rec_a,
        )
        pid = PersistentIdentifier.create("marcid", 6, status=PIDStatus.DELETED)
        # Create redirects
        pid = PersistentIdentifier.create("marcid", 7, status=PIDStatus.REGISTERED)
        pid.redirect(PersistentIdentifier.get("marcid", "3"))

        db.session.commit()

        # Start tests
        resolver = MarcResolver(getter=lambda x: x)

        # Resolve non-existing pid
        pytest.raises(PIDDoesNotExistError, resolver.resolve, "0scgd-ps972")
        pytest.raises(PIDDoesNotExistError, resolver.resolve, "yspa2-jqz52")

        # Resolve status new
        pytest.raises(PIDMissingObjectError, resolver.resolve, "1")

        resolved = resolver.resolve("2")
        assert resolved
        ident = resolved[0]
        assert ident.pid_type == "marcid"
        assert ident.pid_value == "2"
        assert ident.pid_provider is None
        assert ident.object_uuid == rec_a

        # Resolve status reserved
        pytest.raises(PIDMissingObjectError, resolver.resolve, "3")

        # Resolve status registered
        pytest.raises(PIDMissingObjectError, resolver.resolve, "4")

        resolved = resolver.resolve("5")
        assert resolved
        ident = resolved[0]
        assert ident.pid_type == "marcid"
        assert ident.pid_value == "5"
        assert ident.pid_provider is None
        assert ident.object_uuid == rec_a

        # Resolve status deleted
        pytest.raises(PIDDeletedError, resolver.resolve, "6")

        # Resolve status redirected
        try:
            resolver.resolve("7")
            assert False
        except PIDRedirectedError as e:
            assert e.destination_pid.pid_type == "marcid"
            assert e.destination_pid.pid_value == "3"


def test_resolver_deleted_object(app, db):
    """Test the class methods of PersistentIdentifier class."""
    with app.app_context():
        rec_uuid = uuid.uuid4()
        records = {
            rec_uuid: {"title": "test"},
        }
        with db.session.begin_nested():
            pid = PersistentIdentifier.create(
                "marcid",
                "1",
                status=PIDStatus.REGISTERED,
                object_type="rec",
                object_uuid=rec_uuid,
            )

        with db.session.begin_nested():
            pid.delete()

        resolver = MarcResolver(
            pid_type="marcid", object_type="rec", getter=records.get
        )

        assert pytest.raises(PIDDeletedError, resolver.resolve, "1")


def test_resolver_not_registered_only(app, db):
    """Test the resolver returns a new and reserved PID when specified."""

    status = [PIDStatus.NEW, PIDStatus.RESERVED, PIDStatus.REGISTERED]

    with app.app_context():
        rec_a = uuid.uuid4()
        # Create pids for each status with and without object
        for idx, s in enumerate(status, 1):
            PersistentIdentifier.create("recid", idx * 2 - 1, status=s)
            PersistentIdentifier.create(
                "recid", idx * 2, status=s, object_type="rec", object_uuid=rec_a
            )

        db.session.commit()

        # Start tests
        resolver = MarcResolver(
            pid_type="recid",
            object_type="rec",
            getter=lambda x: x,
            registered_only=False,
        )

        # Resolve status new
        pytest.raises(PIDMissingObjectError, resolver.resolve, "1")
        pid, obj = resolver.resolve("2")
        assert pid and obj == rec_a

        # Resolve status reserved
        pytest.raises(PIDMissingObjectError, resolver.resolve, "3")
        pid, obj = resolver.resolve("4")
        assert pid and obj == rec_a

        # Resolve status registered
        pytest.raises(PIDMissingObjectError, resolver.resolve, "5")
        pid, obj = resolver.resolve("6")
        assert pid and obj == rec_a
