# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2021 TU Wien.
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""RDM service component for PIDs."""

from copy import copy

from flask_principal import Identity
from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_rdm_records.services.components import PIDsComponent as BasePIDsComponent
from invenio_records_resources.services.uow import TaskOp

from ...records.api import Marc21Draft, Marc21Record
from ..pids.tasks import register_or_update_pid


class PIDsComponent(BasePIDsComponent):
    """Service component for PIDs."""

    def _add_other_standard_identifier(self, doi: dict, fields: dict) -> dict:
        """Add the other standard identifier to fields."""
        matadata_doi = {
            "ind1": "7",
            "ind2": "_",
            "subfields": {"a": [doi], "2": ["doi"]},
        }

        field = fields.get("024", [])

        if len(field) == 0:
            field.append(matadata_doi)

            fields.update({"024": field})

        return fields

    def _add_electronic_location_and_access(self, doi: dict, fields: dict) -> dict:
        """Add electronic location and access field to fields."""
        metadata_doi = {
            "ind1": "4",
            "ind2": "0",
            "subfields": {
                "u": [f"https://dx.doi.org/{doi}"],
                "z": ["kostenfrei"],
                "3": ["Volltext"],
            },
        }
        field = fields.get("856", [])
        field.append(metadata_doi)

        fields.update({"856": field})

        return fields

    def _doi_identifier_to_metadata(self, doi: dict, data: dict) -> dict:
        metadata = data.get("metadata", {})
        fields = metadata.get("fields", {})

        fields = self._add_other_standard_identifier(doi.get("identifier"), fields)
        fields = self._add_electronic_location_and_access(doi.get("identifier"), fields)

        # Only required in cases where fields might be missing from the metadata
        metadata["fields"] = fields
        return metadata

    def create(  # type: ignore[override]
        self,
        identity: Identity,  # noqa: ARG002
        data: dict,
        record: Marc21Record,
        errors: dict | None = None,
    ) -> None:
        """Create pids.

        This method is called on draft creation.
        It validates and add the pids to the draft.
        """
        pids = data.get("pids", {})
        self.service.pids.pid_manager.validate(pids, record, errors)

        record.pids = pids

    def publish(  # type: ignore[override]
        self,
        identity: Identity,  # noqa: ARG002
        draft: Marc21Draft,
        record: Marc21Record,
    ) -> None:
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

        if "doi" in pids:
            data = copy(draft.model.data)
            record.metadata = self._doi_identifier_to_metadata(pids["doi"], data)

        for scheme in pids:
            self.uow.register(TaskOp(register_or_update_pid, record["id"], scheme))

    def new_version(  # type: ignore[override]
        self,
        identity: Identity,  # noqa: ARG002
        draft: Marc21Draft,
        record: Marc21Record,
    ) -> None:
        """Handle the case of a new version.

        A new version shouldn't have the pids from previos version.
        """
        if record.pids.get("doi", {}).get("provider") == "external":
            draft.pids = {"doi": {"provider": "external", "identifier": ""}}
        else:
            draft.pids = {}


class ParentPIDsComponent(ServiceComponent):
    """Service component for record parent PIDs."""

    def create(
        self,
        identity: Identity,
        data: dict = None,
        record: Marc21Record = None,
        errors: dict = None,
    ) -> None:
        """This method is called on draft creation."""
        record.parent.pids = {}
