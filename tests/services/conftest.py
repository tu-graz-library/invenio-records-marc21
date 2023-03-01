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
from collections import namedtuple
from os.path import dirname, join

import pytest
from flask_principal import Identity
from invenio_access.permissions import any_user, authenticated_user, system_process

from invenio_records_marc21.proxies import current_records_marc21
from invenio_records_marc21.services.record import Marc21Metadata

RunningApp = namedtuple("RunningApp", ["app", "service", "identity_simple", "location"])


@pytest.fixture
def running_app(app, identity_simple, location):
    """This fixture provides an app with the typically needed db data loaded.

    All of these fixtures are often needed together, so collecting them
    under a semantic umbrella makes sense.
    """
    service = app.extensions["invenio-records-marc21"].records_service
    return RunningApp(app, service, identity_simple, location)


@pytest.fixture(scope="module")
def identity_simple():
    """Simple identity fixture."""
    identity = Identity(1)
    identity.provides.add(any_user)
    identity.provides.add(authenticated_user)
    identity.provides.add(system_process)
    return identity


@pytest.fixture(scope="session")
def xml_metadata():
    """Input data (as coming from the view layer)."""
    metadata = Marc21Metadata()
    metadata.xml = "<record><leader>00000nam a2200000zca4500</leader><datafield tag='245' ind1='1' ind2='0'><subfield code='a'>laborum sunt ut nulla</subfield></datafield></record>"
    return metadata


@pytest.fixture(scope="session")
def xml_metadata2():
    """Input data (as coming from the view layer)."""
    metadata = Marc21Metadata()
    metadata.xml = "<record><leader>00000nam a2200000zca4500</leader><datafield tag='245' ind1='1' ind2='0'><subfield code='a'>nulla sunt laborum</subfield></datafield></record>"
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
def embargoedrecord(embargoed_record):
    """Embargoed record."""
    service = current_records_marc21.records_service

    draft = service.create(identity_simple, embargoed_record)
    record = service.publish(id_=draft.id, identity=identity_simple)
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
    metadata.xml = "<record></record>"
    return metadata
