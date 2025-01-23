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

import click
from flask.cli import with_appcontext
from invenio_access.permissions import system_identity
from invenio_accounts.proxies import current_datastore
from invenio_db import db

from .errors import log_exceptions
from .fixtures.demo import create_fake_record
from .fixtures.tasks import create_demo_record
from .fixtures.templates import create_templates, delete_templates
from .proxies import current_records_marc21


def get_user(user_email):
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
            """Wrapper."""
            click.secho(before, fg="blue")
            try:
                func(**kwargs)
            except RuntimeError as error:
                click.secho(str(error), fg="red")
            else:
                click.secho(after, fg="green")

        return wrapper

    return decorator


@click.group()
def marc21():
    """InvenioMarc21 records commands."""


@marc21.command("rebuild-index")
@with_appcontext
@wrap_messages(
    before="Reindexing records and drafts...",
    after="Reindexed records!",
)
def rebuild_index():
    """Reindex all drafts, records."""
    rec_service = current_records_marc21.records_service
    rec_service.rebuild_index(identity=system_identity)


@marc21.command("demo")
@with_appcontext
@click.option(
    "-u",
    "--user-email",
    default="user@demo.org",
    show_default=True,
    help="User e-mail of an existing user.",
)
@click.option(
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
def demo(user_email, n_records):
    """Create number of fake records for demo purposes."""
    user = get_user(user_email)

    for _ in range(n_records):
        fake_data = create_fake_record()
        create_file = True  # TODO: make that random
        create_demo_record.delay(
            user.id, fake_data, publish=True, create_file=create_file
        )


@marc21.group()
def templates():
    """InvenioMarc21 templates commands."""


@templates.command("create")
@click.option(
    "--input-file",
    "-f",
    required=True,
    show_default=True,
    type=str,
    help="Relative path to file",
)
@with_appcontext
@log_exceptions
@wrap_messages(
    before="Creating template/s..",
    after="Successfully created Template/s!",
)
def create(input_file):
    """Create Templates for Marc21 Deposit app."""
    create_templates(input_file)


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
@wrap_messages(
    before="Deleting template/s...",
    after="Successfully deleted Template!",
)
def delete(name, all, force):
    """Delete Templates for Marc21 Deposit app."""
    delete_templates(name, all, force)
