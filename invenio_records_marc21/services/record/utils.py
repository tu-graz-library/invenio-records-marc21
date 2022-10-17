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
