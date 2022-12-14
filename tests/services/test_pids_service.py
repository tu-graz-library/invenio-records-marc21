# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2022 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""PID related tests for Invenio RDM Records.

This tests both the PIDsService and the RDMService behaviour related to pids.
"""

import pytest
from flask import current_app
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PIDStatus
from invenio_rdm_records.records import RDMDraft, RDMRecord
from invenio_rdm_records.services.pids.providers import (
    DataCiteClient,
    DataCitePIDProvider,
)

from invenio_records_marc21.proxies import current_records_marc21


@pytest.fixture()
def mock_public_doi(mocker):
    def public_doi(self, *args, **kwargs):
        # success
        pass

    mocker.patch(
        "invenio_rdm_records.services.pids.providers.datacite."
        "DataCiteRESTClient.public_doi",
        public_doi,
    )


@pytest.fixture()
def mock_hide_doi(mocker):
    def hide_doi(self, *args, **kwargs):
        # success
        pass

    mocker.patch(
        "invenio_rdm_records.services.pids.providers.datacite."
        "DataCiteRESTClient.hide_doi",
        hide_doi,
    )


@pytest.fixture(scope="function")
def record(location):
    """Creates an empty record."""
    draft = RDMDraft.create({})
    record = RDMRecord.publish(draft)

    return record


def test_datacite_provider_configuration(record, mocker):
    def custom_format_func(*args):
        return "10.123/custom.func"

    client = DataCiteClient("datacite")

    # check with default func
    datacite_provider = DataCitePIDProvider("datacite", client=client)
    expected_result = datacite_provider.generate_id(record)
    assert datacite_provider.create(record).pid_value == expected_result

    # check id generation from env func
    current_app.config["DATACITE_FORMAT"] = custom_format_func
    datacite_provider = DataCitePIDProvider("datacite", client=client)
    assert datacite_provider.create(record).pid_value == "10.123/custom.func"

    # check id generation from env f-string
    current_app.config["DATACITE_FORMAT"] = "{prefix}/datacite2.{id}"  # noqa
    datacite_provider = DataCitePIDProvider("datacite", client=client)
    expected_result = datacite_provider.generate_id(record)
    assert datacite_provider.create(record).pid_value == expected_result


#
# Reserve & Discard
#
def test_resolve_pid(running_app, full_metadata):
    """Resolve a PID."""

    service = current_records_marc21.records_service
    identity_simple = running_app.identity_simple
    # create the draft
    draft = service.create(identity=identity_simple, metadata=full_metadata)
    # publish the record
    record = service.publish(identity=identity_simple, id_=draft.id)
    doi = record["pids"]["doi"]["identifier"]

    # test resolution
    resolved_record = service.pids.resolve(
        identity=identity_simple, id_=doi, scheme="doi"
    )
    assert resolved_record.id == record.id
    assert resolved_record["pids"]["doi"]["identifier"] == doi


def test_resolve_non_existing_pid(running_app, full_metadata):
    """Resolve non existing a PID with error."""
    service = current_records_marc21.records_service
    identity_simple = running_app.identity_simple

    draft = service.create(identity=identity_simple, metadata=full_metadata)

    service.publish(identity=identity_simple, id_=draft.id)

    fake_doi = "10.4321/client.12345-invalid"
    with pytest.raises(PIDDoesNotExistError):
        service.pids.resolve(identity=identity_simple, id_=fake_doi, scheme="doi")


def test_reserve_pid(running_app, full_metadata):
    """Reserve a new PID."""
    service = current_records_marc21.records_service
    identity_simple = running_app.identity_simple

    draft = service.create(identity=identity_simple, metadata=full_metadata)
    # draft = service.pids.create(identity=identity_simple, id_=draft.id, scheme="doi")

    doi = draft["pids"]["doi"]["identifier"]
    provider = service.pids.pid_manager._get_provider("doi", "datacite")
    pid = provider.get(pid_value=doi)
    assert pid.status == PIDStatus.NEW


def test_discard_existing_pid(running_app, full_metadata):
    """Discard a PID without error."""
    service = current_records_marc21.records_service
    identity_simple = running_app.identity_simple

    draft = service.create(identity=identity_simple, metadata=full_metadata)

    # draft = service.pids.create(identity=identity_simple, id_=draft.id, scheme="doi")

    doi = draft["pids"]["doi"]["identifier"]
    provider = service.pids.pid_manager._get_provider("doi", "datacite")
    pid = provider.get(pid_value=doi)
    assert pid.status == PIDStatus.NEW
    draft = service.pids.discard(identity=identity_simple, id_=draft.id, scheme="doi")
    assert not draft["pids"].get("doi")
    with pytest.raises(PIDDoesNotExistError):
        pid = provider.get(pid_value=doi)


@pytest.mark.skip("Cannot be tested. Since the pids are created with a draft.")
def test_discard_non_exisisting_pid(running_app, full_metadata):
    """Discard a PID with error."""
    service = current_records_marc21.records_service
    identity_simple = running_app.identity_simple

    draft = service.create(identity=identity_simple, metadata=full_metadata)
    with pytest.raises(PIDDoesNotExistError):
        service.pids.discard(identity=identity_simple, id_=draft.id, scheme="doi")
