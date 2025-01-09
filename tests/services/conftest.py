# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""
import json

# from os.path import dirname, join
from pathlib import Path

import pytest

from invenio_records_marc21.proxies import current_records_marc21
from invenio_records_marc21.services.record import Marc21Metadata


@pytest.fixture(scope="session")
def json_metadata():
    """Input data (as coming from the view layer)."""
    return {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {"a": ["laborum sunt ut nulla"]},
                    }
                ]
            },
        }
    }


@pytest.fixture(scope="session")
def json_metadata2():
    """Input data (as coming from the view layer)."""
    return {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {"a": ["nulla sunt laborum"]},
                    }
                ]
            },
        }
    }


@pytest.fixture()
def embargoedrecord(embargoed_record, adminuser_identity):
    """Embargoed record."""
    service = current_records_marc21.records_service

    draft = service.create(adminuser_identity, embargoed_record)
    record = service.publish(id_=draft.id, identity=adminuser_identity)
    return record


@pytest.fixture()
def full_metadata():
    """Metadata full record marc21 json."""
    # json_string = _load_file()
    metadata = Marc21Metadata()
    with Path(Path(__file__).parent / "test-metadata.json").open("r") as fp:
        metadata.json = json.load(fp)["metadata"]
    return metadata


@pytest.fixture()
def full_metadata_expected():
    """Metadata full record expected."""
    with Path(Path(__file__).parent / "test-metadata.json").open("r") as fp:
        return json.load(fp)
