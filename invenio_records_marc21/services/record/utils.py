# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2022 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 utils."""

import time
from os.path import basename

from invenio_search import RecordsSearch
from invenio_search.engine import dsl


class DuplicateRecordError(Exception):
    """Duplicate Record Exception."""

    def __init__(self, ac_number, id_):
        """Constructor for class DuplicateRecordException."""
        msg = f"DuplicateRecordError ac_number: {ac_number} already exists id={id_} in the database"
        super().__init__(msg)


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


def create_record(service, marc21_metadata, file_path, identity):
    """Create the record."""
    draft = service.create(metadata=marc21_metadata, identity=identity, files=True)

    add_file_to_record(
        marcid=draft._record["id"],  # pylint: disable=protected-access
        file_path=file_path,
        file_service=service.draft_files,
        identity=identity,
    )

    # to prevent the race condition bug.
    # see https://github.com/inveniosoftware/invenio-rdm-records/issues/809
    time.sleep(0.5)

    return service.publish(id_=draft.id, identity=identity)


def check_about_duplicate(ac_number):
    """Check if the record with the ac number is already within the database."""
    search = RecordsSearch(index="marc21records-marc21")
    search.query = dsl.Q("match", **{"metadata.fields.009": ac_number})
    results = search.execute()

    if len(results) > 0:
        raise DuplicateRecordError(ac_number=ac_number, id_=results[0]["id"])
