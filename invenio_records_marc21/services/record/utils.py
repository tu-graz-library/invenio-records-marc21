# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2022-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 utils."""

import time
from functools import singledispatch
from os.path import basename

from invenio_search import RecordsSearch
from invenio_search.engine import dsl
from marshmallow.exceptions import ValidationError

from .types import DOI, ACNumber, DuplicateRecordError


def add_file_to_record(
    marcid,
    file_path,
    file_service,
    identity,
):
    """Add the file to the record."""
    filename = basename(file_path)
    data = [{"key": filename}]

    with open(file_path, mode="rb") as file_pointer:
        file_service.init_files(id_=marcid, identity=identity, data=data)
        file_service.set_file_content(
            id_=marcid, file_key=filename, identity=identity, stream=file_pointer
        )
        file_service.commit_file(id_=marcid, file_key=filename, identity=identity)


def create_record(service, data, file_paths, identity, do_publish=True):
    """Create the record."""
    draft = service.create(data=data, identity=identity, files=True)

    try:
        for file_path in file_paths:
            add_file_to_record(
                marcid=draft.id,
                file_path=file_path,
                file_service=service.draft_files,
                identity=identity,
            )

        if do_publish:
            # to prevent the race condition bug.
            # see https://github.com/inveniosoftware/invenio-rdm-records/issues/809
            time.sleep(0.5)

            return service.publish(id_=draft.id, identity=identity)

    except (FileNotFoundError, ValidationError) as error:
        service.delete_draft(id_=draft.id, identity=identity)
        raise error

    return draft


@singledispatch
def check_about_duplicate(value: str, category: str = None):
    """Check if the record with the ac number is already within the database."""
    search = RecordsSearch(index="marc21records")

    if category:
        query = {f"metadata.fields.{category}": value}
    else:
        return

    search.query = dsl.Q("match", **query)
    results = search.execute()

    if len(results) > 0:
        raise DuplicateRecordError(value=value, category=category, id_=results[0]["id"])


@check_about_duplicate.register
def _(value: ACNumber):
    """Check about double ac number."""
    check_about_duplicate(str(value), value.category)


@check_about_duplicate.register
def _(value: DOI):
    check_about_duplicate(str(value), value.category)
