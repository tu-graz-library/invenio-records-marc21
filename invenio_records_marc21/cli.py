# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Command-line tools for demo module."""


from collections.abc import Callable
from functools import wraps

from click import group, option, secho
from flask.cli import with_appcontext
from invenio_access.permissions import system_identity
from invenio_accounts.models import User
from invenio_accounts.proxies import current_datastore
from invenio_db import db

from .errors import log_exceptions
from .fixtures.demo import create_fake_record
from .fixtures.tasks import create_demo_record
from .proxies import current_records_marc21
from .utils import JSON


def get_user(user_email: str) -> User:
    """Get user."""
    with db.session.no_autoflush:
        user = current_datastore.get_user_by_email(user_email)

    if not user:
        msg = f"NO user found for email: {user_email}"
        raise RuntimeError(msg)

    return user


def wrap_messages(before: str, after: str) -> Callable:
    """Wrap messages with entry and exit message."""

    def decorator[T](func: Callable[..., T]) -> Callable:
        @wraps(func)
        def wrapper(**kwargs: dict) -> None:
            """Wrapp."""
            secho(before, fg="blue")
            try:
                func(**kwargs)
            except RuntimeError as error:
                secho(str(error), fg="red")
            else:
                secho(after, fg="green")

        return wrapper

    return decorator


@group()
def marc21() -> None:
    """InvenioMarc21 records commands."""


@marc21.command("rebuild-index")
@with_appcontext
@wrap_messages(
    before="Reindexing records and drafts...",
    after="Reindexed records!",
)
def rebuild_index() -> None:
    """Reindex all drafts, records."""
    rec_service = current_records_marc21.records_service
    rec_service.rebuild_index(identity=system_identity)


@marc21.command("demo")
@with_appcontext
@option(
    "-u",
    "--user-email",
    default="user@demo.org",
    show_default=True,
    help="User e-mail of an existing user.",
)
@option(
    "--number",
    "-n",
    "n_records",
    default=10,
    show_default=True,
    type=int,
    help="Number of records will be created.",
)
@with_appcontext
@log_exceptions
@wrap_messages(
    before="Creating demo records...",
    after="Created records!",
)
def demo(user_email: str, n_records: int) -> None:
    """Create number of fake records for demo purposes."""
    user = get_user(user_email)

    for _ in range(n_records):
        fake_data = create_fake_record()
        create_file = True  # TODO: make that random
        create_demo_record.delay(
            user.id,
            fake_data,
            publish=True,
            create_file=create_file,
        )


@marc21.group()
def templates() -> None:
    """InvenioMarc21 templates commands."""


@templates.command("create")
@option(
    "--input-data",
    required=True,
    show_default=True,
    type=JSON(),
    help="Relative path to json file",
)
@with_appcontext
@log_exceptions
@wrap_messages(
    before="Creating template/s..",
    after="Successfully created Template/s!",
)
def create(input_data: dict) -> None:
    """Create Templates for Marc21 Deposit app.

    \b
    json should look like:
    \b
    {
      "NAME": {
        "fields": {
          041": [
            {
              "ind1": "_",
              "ind2": "_",
              "subfields": {
                "a": ["eng"]
              }
            }
          ]
        }
      }
    }
    """
    service = current_records_marc21.templates_service

    for data in input_data:
        service.create(identity=system_identity, data=data)


@templates.command("delete")
@option(
    "--pid",
    required=False,
    type=str,
    help="Template pid.",
)
@with_appcontext
@log_exceptions
@wrap_messages(
    before="Deleting template...",
    after="Successfully deleted Template!",
)
def delete(pid: str) -> None:
    """Delete Templates for Marc21 Deposit app."""
    service = current_records_marc21.templates_service
    return service.delete(identity=system_identity, id_=pid)
