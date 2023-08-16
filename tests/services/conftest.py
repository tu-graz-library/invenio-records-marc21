# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""
import json
from os.path import dirname, join

import pytest

from invenio_records_marc21.proxies import current_records_marc21
from invenio_records_marc21.services.record import Marc21Metadata


@pytest.fixture(scope="session")
def xml_metadata():
    """Input data (as coming from the view layer)."""
    metadata = Marc21Metadata()
    metadata.xml = """<record xmlns="http://www.loc.gov/MARC21/slim"><leader>00000nam a2200000zca4500</leader><datafield tag='245' ind1='1' ind2='0'><subfield code='a'>laborum sunt ut nulla</subfield></datafield></record>"""
    return metadata


@pytest.fixture(scope="session")
def xml_metadata2():
    """Input data (as coming from the view layer)."""
    metadata = Marc21Metadata()
    metadata.xml = """<record xmlns="http://www.loc.gov/MARC21/slim"><leader>00000nam a2200000zca4500</leader><datafield tag='245' ind1='1' ind2='0'><subfield code='a'>nulla sunt laborum</subfield></datafield></record>"""
    return metadata


@pytest.fixture(scope="session")
def json_metadata():
    """Input data (as coming from the view layer)."""
    metadata = {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {
                "245": [
                    {
                        "subfields": {"a": ["laborum sunt ut nulla"]},
                        "ind1": "1",
                        "ind2": "0",
                    }
                ]
            },
        }
    }
    return metadata


@pytest.fixture(scope="session")
def json_metadata2():
    """Input data (as coming from the view layer)."""
    metadata = {
        "metadata": {
            "leader": "00000nam a2200000zca4500",
            "fields": {
                "245": [
                    {
                        "subfields": {"a": ["nulla sunt laborum"]},
                        "ind1": "1",
                        "ind2": "0",
                    }
                ]
            },
        }
    }
    return metadata


@pytest.fixture()
def embargoedrecord(embargoed_record, adminuser_identity):
    """Embargoed record."""
    service = current_records_marc21.records_service

    draft = service.create(adminuser_identity, embargoed_record)
    record = service.publish(id_=draft.id, identity=adminuser_identity)
    return record


def _load_file(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        return fp.read()


@pytest.fixture()
def full_metadata():
    """Metadata full record marc21 xml."""
    metadata = Marc21Metadata()
    metadata.xml = _load_file("test-metadata.xml").decode("UTF-8")
    return metadata


@pytest.fixture()
def full_metadata_expected():
    """Metadata full record marc21 json expected."""
    json_string = _load_file("test-metadata.json")
    return json.loads(json_string.decode("UTF-8"))


@pytest.fixture()
def min_metadata():
    """Metadata empty record marc21 xml."""
    metadata = Marc21Metadata()
    metadata.xml = """<record xmlns="http://www.loc.gov/MARC21/slim"></record>"""
    return metadata
