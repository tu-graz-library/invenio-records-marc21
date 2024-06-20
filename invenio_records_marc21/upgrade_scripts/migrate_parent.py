# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Migrate."""

from click import secho
from invenio_db import db

from invenio_records_marc21.records import Marc21Draft, Marc21Record


def update_parent(record):
    """Update parent."""
    owned_by = record.parent["access"]["owned_by"]

    if isinstance(owned_by, list) and len(owned_by) > 0:
        record.parent.access.owned_by = {
            "user": owned_by[0]["user"],
        }


def update_record(record):
    """Update record."""
    if record.is_deleted:
        return

    try:
        record.setdefault("media_files", {"enabled": False})

        update_parent(record)

        record.parent.commit()
        record.commit()

        secho(f"> Updated parent: {record.parent.pid.pid_value}", fg="green")
        secho(f"> Updated record: {record.pid.pid_value}\n", fg="green")
        return None
    except Exception as e:
        secho(f"> Error {e!r}", fg="red")
        error = f"Record {record.pid.pid_value} failed to update"
        return error


def execute_upgrade():
    """Execute upgrade."""
    errors = []

    apis = [Marc21Record, Marc21Draft]

    for api_cls in apis:
        for record_metadata in api_cls.model_cls.query.all():
            record = api_cls(record_metadata.data, model=record_metadata)
            error = update_record(record)

            if error:
                errors.append(error)

    success = not errors

    if success:
        secho("Commiting to DB", nl=True)
        db.session.commit()
        secho(
            "Data migration completed, please rebuild the search indices now.",
            fg="green",
        )

    else:
        secho("Rollback", nl=True)
        db.session.rollback()
        secho(
            "Upgrade aborted due to the following errors:",
            fg="red",
            err=True,
        )

        for error in errors:
            secho(error, fg="red", err=True)

        msg = (
            "The changes have been rolled back. "
            "Please fix the above listed errors and try the upgrade again",
        )
        secho(msg, fg="yellow", err=True)


if __name__ == "__main__":
    execute_upgrade()
