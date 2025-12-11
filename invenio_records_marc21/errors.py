# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 error messages."""

from collections.abc import Callable
from functools import wraps

from click import secho
from invenio_i18n import gettext as _

ERROR_MESSAGE_WRAPPER: dict[str, list[dict[str, str]]] = {
    "ProgrammingError": [
        {
            "args": "UndefinedTable",
            "message": "DB_TABLE_NOT_FOUND",
        },
    ],
    "OperationalError": [
        {
            "args": "could not connect to server",
            "message": "SERVICES_CONNECTION_REFUSED",
        },
    ],
    "ConnectionError": [
        {
            "args": "Connection refused.",
            "message": "SERVICES_CONNECTION_REFUSED",
        },
    ],
    "PermissionDeniedError": [
        {
            "args": "",
            "message": "PERMISSIONS_ERROR",
        },
    ],
}

ERROR_MESSAGES: dict[str, str] = {
    "DB_TABLE_NOT_FOUND": _(
        "The table you are looking for does not exist.\n"
        "Maybe you missed to re-setup the services after the marc21 module was installed.\n"
        "Try to do a invenio-cli services setup -f",
    ),
    "SERVICES_CONNECTION_REFUSED": _(
        "Connection to Services refused.\n"
        "Maybe you missed to start the services.\n"
        "Try to do a invenio-cli services setup -f",
    ),
    "PERMISSIONS_ERROR": _("User has not the permissions."),
}


def log_exceptions[**P, R](f: Callable[P, R]) -> Callable[P, R]:
    """Decorate function to catch all exceptions and log to CLI."""

    @wraps(f)
    def catch_and_log(*args: P.args, **kwargs: P.kwargs) -> R:
        """Catch and log."""
        try:
            ret = f(*args, **kwargs)
        except Exception as e:
            _create_errormessage(e)

        return ret

    return catch_and_log


def _create_errormessage(e: Exception) -> None:
    """Create an error message for CLI."""
    message = ""
    errors = ERROR_MESSAGE_WRAPPER.get(type(e).__name__, [])

    for error in errors:
        args = error.get("args")
        if args is None or args in e.args[0]:
            wrap = error.get("message", "")
            message = ERROR_MESSAGES.get(wrap, "")
            break
    message = message if message else "Error:\n" + str(e)
    secho(message, fg="red")
