# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM service component for PIDs."""

from copy import copy

from invenio_rdm_records.services.components import PIDsComponent as BasePIDsComponent
from invenio_records_resources.services.uow import TaskOp

from ..pids.tasks import register_or_update_pid


class PIDsComponent(BasePIDsComponent):
    """Service component for PIDs."""

    def _doi_identifier_to_metadata(self, doi, data):
        metadata = data.get("metadata", {})
        fields = metadata.get("fields", {})
        other_standard_identifier = fields.get("024", [])
        matadata_doi = {
            "ind1": "7",
            "ind2": "_",
            "subfields": {"a": [doi.get("identifier")], "2": ["doi"]},
        }
        other_standard_identifier.append(matadata_doi)
        fields.update({"024": other_standard_identifier})

    def create(self, identity, data=None, record=None, errors=None):
        """This method is called on draft creation.

        It validates and add the pids to the draft.
        """
        pids = data.get("pids", {})
        self.service.pids.pid_manager.validate(pids, record, errors)

        record.pids = pids
        pids = self.service.pids.pid_manager.create_all(
            record,
            pids=pids,
            schemes=set(self.service.config.pids_required),
        )
        if "doi" in pids and data:
            self._doi_identifier_to_metadata(pids["doi"], data)
        record.pids = pids

    def publish(self, identity, draft=None, record=None):
        """Publish handler."""
        draft_pids = draft.get("pids", {})
        record_pids = copy(record.get("pids", {}))
        draft_schemes = set(draft_pids.keys())
        record_schemes = set(record_pids.keys())

        missing_required_schemes = (
            set(self.service.config.pids_required) - record_schemes - draft_schemes
        )

        self.service.pids.pid_manager.validate(draft_pids, record, raise_errors=True)

        changed_pids = {}
        for scheme in draft_schemes.intersection(record_schemes):
            record_id = record_pids[scheme]["identifier"]
            draft_id = draft_pids[scheme]["identifier"]
            if record_id != draft_id:
                changed_pids[scheme] = record_pids[scheme]

        self.service.pids.pid_manager.discard_all(changed_pids)

        pids = self.service.pids.pid_manager.create_all(
            draft,
            pids=draft_pids,
            schemes=missing_required_schemes,
        )

        self.service.pids.pid_manager.reserve_all(draft, pids)
        record.pids = pids

        for scheme in pids.keys():
            self.uow.register(TaskOp(register_or_update_pid, record["id"], scheme))
