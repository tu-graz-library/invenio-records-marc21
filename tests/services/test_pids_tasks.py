# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""PID service tasks tests."""

from invenio_pidstore.models import PIDStatus

from invenio_records_marc21.proxies import current_records_marc21
from invenio_records_marc21.services.pids.tasks import register_or_update_pid


def test_register_pid(running_app, full_metadata, mocker, identity_simple):
    """Registers a PID."""

    def public_doi(self, metadata, url, doi):
        """Mock doi deletion."""
        pass

    mocker.patch(
        "invenio_rdm_records.services.pids.providers.datacite."
        "DataCiteRESTClient.public_doi",
        public_doi,
    )
    service = current_records_marc21.records_service
    draft = service.create(identity=identity_simple, metadata=full_metadata)
    # draft = service.pids.create(identity=identity_simple, id_=draft.id, scheme="doi")
    doi = draft["pids"]["doi"]["identifier"]

    provider = service.pids.pid_manager._get_provider("doi", "datacite")
    pid = provider.get(pid_value=doi)
    record = service.record_cls.publish(draft._record)
    record.pids = {pid.pid_type: {"identifier": pid.pid_value, "provider": "datacite"}}
    record.metadata = draft["metadata"]

    record.register()
    record.commit()
    assert pid.status == PIDStatus.NEW

    pid.reserve()
    assert pid.status == PIDStatus.RESERVED

    register_or_update_pid(recid=record["id"], scheme="doi")
    assert pid.status == PIDStatus.REGISTERED
