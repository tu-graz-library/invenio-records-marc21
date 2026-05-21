# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Add OAI PIDs to existing marc21 records."""

from click import secho
from invenio_db import db
from invenio_pidstore.errors import PIDAlreadyExists
from invenio_rdm_records.services.pids.providers import OAIPIDProvider

from invenio_records_marc21.proxies import current_records_marc21
from invenio_records_marc21.records import Marc21Draft, Marc21Record

try:
    from invenio_catalogue_marc21.records import (
        Marc21CatalogueDraft,
        Marc21CatalogueRecord,
    )

    catalogue_package_installed = True
except ImportError:
    catalogue_package_installed = False


def update_pids(record):
    """Update record."""
    if record.is_deleted:
        return None, None

    try:
        provider: OAIPIDProvider = (
            current_records_marc21.records_service.config.pids_providers["oai"]["oai"]
        )
        pid = provider.create(record=record)

        secho(f"> Updated pid for OAI: {record.pid.pid_value}\n", fg="green")
        return pid, None
    except PIDAlreadyExists:
        # expected error: we update only records that don't have OAI pid yet.
        return provider.get(provider.generate_id(record)), None
    except Exception as e:
        secho(f"> Error {e!r}", fg="red")
        error = f"Pid {record.pid.pid_value} failed to update"
        return None, error


def update_record(record, pid):
    if not pid:
        return None

    provider: OAIPIDProvider = (
        current_records_marc21.records_service.config.pids_providers["oai"]["oai"]
    )
    try:
        if pid.pid_type not in record["pids"]:
            # update only records that don't have the oai PID
            record["pids"][pid.pid_type] = {
                "identifier": pid.pid_value,
                "provider": provider.name,
            }

            record.commit()
            secho(
                f"> Updated record: {record.pid.pid_value} with PID: {pid.pid_value}\n",
                fg="green",
            )
    except Exception as e:
        secho(f"> Error {e!r}", fg="red")
        error = f"Record {record.pid.pid_value} failed to update"
        return error


def is_catalogue_record(data):
    return ("$schema" in data and "catalogue" in data["$schema"]) or "catalogue" in data


def execute_upgrade():
    """Execute upgrade."""
    errors = []

    apis = {
        "records": {
            "base": Marc21Record,
        },
        "drafts": {
            "base": Marc21Draft,
        },
    }

    if catalogue_package_installed:
        apis["records"]["catalogue"] = Marc21CatalogueRecord
        apis["drafts"]["catalogue"] = Marc21CatalogueDraft

    for api_type in apis.values():
        base_cls = api_type["base"]

        for record_metadata in base_cls.model_cls.query.all():
            try:
                data = record_metadata.data
                use_catalogue_api = catalogue_package_installed and is_catalogue_record(
                    data
                )

                api_cls = api_type["catalogue"] if use_catalogue_api else base_cls

                record = api_cls(record_metadata.data, model=record_metadata)
                pid, error_pid = update_pids(record)
                error_record = update_record(record, pid)

                if error_pid:
                    errors.append(error_pid)
                if error_record:
                    errors.append(error_record)
            except Exception as e:
                # Log this unexpected behaviour but don't stop the process.
                #
                # This can happen only if API classes fail to load the record
                # which signals that there is a record which does not respect
                # the schema.
                #
                # This should be addressed separately and shouldn't block this
                # migration process.
                secho(f"> Error {e!r}: record {record_metadata.data}", fg="red")

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
