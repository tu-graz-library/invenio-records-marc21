# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Record Service."""

from invenio_db import db
from invenio_drafts_resources.services.records import RecordService
from invenio_rdm_records.records.systemfields.access.field.record import (
    AccessStatusEnum,
)
from invenio_records_resources.services.files.service import FileService
from invenio_records_resources.services.records.results import RecordItem

from .config import (
    Marc21DraftFilesServiceConfig,
    Marc21RecordFilesServiceConfig,
    Marc21RecordServiceConfig,
)
from .errors import EmbargoNotLiftedError
from .record import Marc21Metadata


class Marc21RecordService(RecordService):
    """Marc21 record service."""

    config_name = "MARC21_RECORDS_SERVICE_CONFIG"
    default_config = Marc21RecordServiceConfig

    def _create_data(self, identity, data, metadata, access=None):
        """Create a data json.

        :param identity: Identity of user creating the record.
        :param Metadata metadata: Input data according to the metadata schema.
        :param dict access: provide access additional information
        :return data: marc21 record data
        """
        if data is None:
            data = {"metadata": {"xml": metadata.xml, "json": metadata.json}}
        if "access" not in data:
            default_access = {
                "access": {
                    "owned_by": [{"user": identity.id}],
                    "metadata": AccessStatusEnum.OPEN.value,
                    "files": AccessStatusEnum.OPEN.value,
                },
            }
            if access is not None:
                default_access["access"].update(access)
            data.update(default_access)
        return data

    def create(
        self, identity, data=None, metadata=Marc21Metadata(), access=None
    ) -> RecordItem:
        """Create a draft record.

        :param identity: Identity of user creating the record.
        :param dict data: Input data according to the data schema.
        :param Marc21Metadata metadata: Input data according to the metadata schema.
        :param links_config: Links configuration.
        :param dict access: provide access additional information
        """
        data = self._create_data(identity, data, metadata, access)
        return super().create(identity, data)

    def update_draft(
        self,
        id_,
        identity,
        data=None,
        metadata=Marc21Metadata(),
        revision_id=None,
        access=None,
    ):
        """Update a draft record.

        :param identity: Identity of user creating the record.
        :param dict data: Input data according to the data schema.
        :param Marc21Metadata metadata: Input data according to the metadata schema.
        :param links_config: Links configuration.
        :param dict access: provide access additional information
        """
        data = self._create_data(identity, data, metadata, access)
        return super().update_draft(id_, identity, data, revision_id)

    def _lift_embargo_from(self, record):
        """Lifts embargo from record or draft."""
        if not record.access.lift_embargo():
            raise EmbargoNotLiftedError(record["id"])
        record.access.protection.metadata = "public"
        record.access.protection.files = "public"

    def _is_draft_access_field_modified(self, draft, record):
        """Returns True if draft's access field was modified."""
        return draft.get("access") == record.get("access")

    def lift_embargo(self, _id, identity):
        """Lifts embargo from the record and updates draft."""
        # Get the record
        record = self.record_cls.pid.resolve(_id)

        self.require_permission(identity, "lift_embargo", record=record)

        lifted_embargo_from_draft = False
        # Check if record has already a draft
        if record.has_draft:
            draft = self.draft_cls.pid.resolve(_id, registered_only=False)

            if self._is_draft_access_field_modified(draft, record):
                # Lifts embargo from draft
                self._lift_embargo_from(draft)
                lifted_embargo_from_draft = True

        # Lifts embargo from record
        self._lift_embargo_from(record)
        # Commit and index
        record.commit()
        if record.has_draft and lifted_embargo_from_draft:
            draft.commit()
        db.session.commit()
        self.indexer.index(record)
        if record.has_draft and lifted_embargo_from_draft:
            self.indexer.index(draft)


#
# Record files
#
class Marc21RecordFilesService(FileService):
    """Marc21 record files service."""

    config_name = "MARC21_RECORDS_FILES_SERVICE_CONFIG"
    default_config = Marc21RecordFilesServiceConfig


#
# Draft files
#
class Marc21DraftFilesService(FileService):
    """Marc21 draft files service."""

    config_name = "MARC21_DRAFT_FILES_SERVICE_CONFIG"
    default_config = Marc21DraftFilesServiceConfig
