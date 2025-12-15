# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 utils module."""

import sys
from json import JSONDecodeError, load, loads
from pathlib import Path

from click import Context, Parameter, ParamType, secho


def build_record_unique_id(doc):
    """Build record unique identifier."""
    doc["unique_id"] = "{0}_{1}".format(doc["recid"], doc["parent_recid"])
    return doc


####
# copy pasted from repository-cli
# code slightly updated
###
def _error_msg(art: str, key: str) -> str:
    """Construct error message."""
    error_msgs = {
        "validate": f"The given json does not validate, key: '{key}' does not exists",
    }
    return error_msgs[art]


class JSON(ParamType):
    """JSON provides the ability to load a json from a string or a file."""

    name = "JSON"

    def __init__(self, validate: list[str] | None = None) -> None:
        """Construct Json ParamType."""
        self.validate = validate

    def convert(
        self,
        value: str,
        param: Parameter | None,  # noqa: ARG002
        ctx: Context | None,  # noqa: ARG002
    ) -> dict:
        """Convert the json-file to the dictionary representation."""
        try:
            if Path(value).is_file():
                with Path(value).open("r", encoding="utf8") as file_pointer:
                    obj = load(file_pointer)
            else:
                obj = loads(value)
        except JSONDecodeError as error:
            msg = "ERROR - Invalid JSON provided. Check file path or json string."
            secho(msg, fg="red")
            secho(f"  error: {error.args[0]}", fg="red")
            sys.exit()
            return {}

        if self.validate:
            for key in self.validate:
                if key not in obj:
                    secho(_error_msg("validate", key), fg="red")
                    sys.exit()

        return obj


####
# copy pasted from repository-cli END
###
