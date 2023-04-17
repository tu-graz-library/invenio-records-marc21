# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Command-line tools for demo module."""

import json
import random
from datetime import timedelta
from os.path import dirname, join

import arrow
import click
from flask.cli import with_appcontext
from flask_principal import Identity
from invenio_access.permissions import any_user, authenticated_user, system_process
from invenio_rdm_records.records.systemfields.access.field.record import (
    AccessStatusEnum,
)

from .errors import log_exceptions
from .proxies import current_records_marc21
from .services.record import Marc21Metadata


def system_identity():
    """System identity."""
    identity = Identity(1)
    identity.provides.add(any_user)
    identity.provides.add(authenticated_user)
    identity.provides.add(system_process)
    return identity


def fake_access_right():
    """Generates a fake access_right."""
    _type = random.choice(list(AccessStatusEnum)).value
    if (
        _type == AccessStatusEnum.METADATA_ONLY.value
        or _type == AccessStatusEnum.OPEN.value
    ):
        return "public"
    return _type


def fake_feature_date(days=365):
    """Generates a fake feature_date."""
    start_date = arrow.utcnow().datetime
    random_number_of_days = random.randrange(1, days)
    _date = start_date + timedelta(days=random_number_of_days)
    return _date.strftime("%Y-%m-%d")


def _load_file(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        input = fp.read()
        return input.decode("utf-8")


def _load_json(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        return json.load(fp)


def create_fake_metadata(filename):
    """Create records for demo purposes."""
    metadata = Marc21Metadata()
    metadata.xml = _load_file(filename)
    metadata_access = fake_access_right()
    data_access = {
        "files": "public",
        "record": metadata_access,
    }
    if metadata_access == AccessStatusEnum.EMBARGOED.value:
        embargo = {
            "embargo": {
                "until": fake_feature_date(),
                "active": True,
                "reason": "Because I can!",
            }
        }
        data_access.update(embargo)
        data_access["record"] = AccessStatusEnum.RESTRICTED.value

    service = current_records_marc21.records_service
    draft = service.create(
        metadata=metadata,
        identity=system_identity(),
        access=data_access,
    )

    record = service.publish(id_=draft.id, identity=system_identity())

    return record


def create_fake_record(filename):
    """Create records for demo purposes."""
    data_to_use = _load_json(filename)
    metadata_access = fake_access_right()
    data_access = {
        "files": "public",
        "record": metadata_access,
    }

    if metadata_access == AccessStatusEnum.EMBARGOED.value:
        embargo = {
            "embargo": {
                "until": fake_feature_date(),
                "active": True,
                "reason": "Because I can!",
            }
        }
        data_access.update(embargo)
        data_access["record"] = AccessStatusEnum.RESTRICTED.value

    service = current_records_marc21.records_service

    marc21_metadata = Marc21Metadata()
    marc21_metadata.xml = data_to_use["metadata"]["xml"]
    draft = service.create(
        metadata=marc21_metadata,
        identity=system_identity(),
        access=data_access,
        files=False,
    )

    record = service.publish(id_=draft.id, identity=system_identity())

    return record


@click.group()
def marc21():
    """InvenioMarc21 records commands."""
    pass


@marc21.command("rebuild-index")
@with_appcontext
def rebuild_index():
    """Reindex all drafts, records."""
    click.secho("Reindexing records and drafts...", fg="green")

    rec_service = current_records_marc21.records_service
    rec_service.rebuild_index(identity=system_identity)

    click.secho("Reindexed records!", fg="green")


@marc21.command("demo")
@with_appcontext
@click.option(
    "--number",
    "-n",
    default=10,
    show_default=True,
    type=int,
    help="Number of records will be created.",
)
@click.option(
    "--file",
    "-f",
    default="data/fake-metadata.xml",
    show_default=True,
    type=str,
    help="Relative path to file",
)
@click.option(
    "--metadata-only",
    "-m",
    default="True",
    type=bool,
    help="Provided metadata only in file",
)
@with_appcontext
@log_exceptions
def demo(number, file, metadata_only):
    """Create number of fake records for demo purposes."""
    click.secho("Creating demo records...", fg="blue")
    for _ in range(number):
        if metadata_only:
            create_fake_metadata(file)
        else:
            create_fake_record(file)

    click.secho("Created records!", fg="green")


def create_templates(filename):
    """Create templates with the service."""
    data_to_use = _load_json(filename)

    service = current_records_marc21.templates_service
    templates = []
    for data in data_to_use:
        template = service.create(data=data["values"], name=data["name"])
        templates.append(template.to_dict())
    return templates


def delete_templates(name, all, force):
    """Delete templates with the service."""
    service = current_records_marc21.templates_service
    result = service.delete(name=name, all=all, force=force)
    return result


@marc21.group()
def templates():
    """InvenioMarc21 templates commands."""
    pass


@templates.command("create")
@click.option(
    "--file",
    "-f",
    required=True,
    show_default=True,
    type=str,
    help="Relative path to file",
)
@with_appcontext
@log_exceptions
def create(file):
    """Create Templates for Marc21 Deposit app."""
    click.secho("Creating template/s..", fg="blue")

    create_templates(file)

    click.secho("Successfully created Template/s!", fg="green")


@templates.command("delete")
@click.option(
    "--all",
    default=False,
    show_default=True,
    is_flag=True,
    help="Delete all Templates",
)
@click.option(
    "--force",
    "-f",
    default=False,
    show_default=True,
    is_flag=True,
    help="Hard/Soft delete of templates.",
)
@click.option(
    "--name",
    "-n",
    required=False,
    type=str,
    help="Template name.",
)
@with_appcontext
@log_exceptions
def delete(name, all, force):
    """Delete Templates for Marc21 Deposit app."""
    click.secho("Deleting template/s...", fg="blue")

    delete_templates(name, all, force)

    click.secho("Successfully deleted Template!", fg="green")
