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
from invenio_rdm_records.services import RDMRecordService
from invenio_records_resources.services.files.service import FileService
from invenio_records_resources.services.records.results import RecordItem

from .config import Marc21DraftFilesServiceConfig, Marc21RecordFilesServiceConfig
from .errors import EmbargoNotLiftedError
from .record import Marc21Metadata


class Marc21RecordService(RDMRecordService):
    """Marc21 record service class."""

    def _create_data(self, identity, data, metadata, files=False, access=None):
        """Create a data json.

        :param identity: Identity of user creating the record.
        :type identity: `flask_principal.identity`
        :param data: Input data according to the data schema.
        :type data: dict
        :param metadata: Input data according to the metadata schema.
        :type metadata: `services.record.Marc21Metadata`
        :param files: enable/disable file support for the record.
        :type files: bool
        :param dict access: provide access additional information
        :return: marc21 record dict
        :rtype: dict
        """
        if data is None:
            data = metadata.json
        if not "files" in data:
            data["files"] = {"enabled": files}
        if "access" not in data:
            default_access = {
                "access": {
                    "record": "public",
                    "files": "public",
                },
            }
            if access is not None:
                default_access["access"].update(access)
            data.update(default_access)
        return data

    def create(
        self,
        identity,
        data=None,
        metadata=Marc21Metadata(),
        files=False,
        access=None,
        uow=None,
    ) -> RecordItem:
        """Create a draft record.

        :param identity: Identity of user creating the record.
        :type identity: `flask_principal.identity`
        :param data: Input data according to the data schema.
        :type data: dict
        :param metadata: Input data according to the metadata schema.
        :type metadata: `services.record.Marc21Metadata`
        :param files: enable/disable file support for the record.
        :type files: bool
        :param dict access: provide access additional information
        :return: marc21 record item
        :rtype: `invenio_records_resources.services.records.results.RecordItem`
        """
        data = self._create_data(identity, data, metadata, files, access)
        return super().create(identity=identity, data=data)

    def update_draft(
        self,
        identity,
        id_,
        data=None,
        metadata=Marc21Metadata(),
        revision_id=None,
        access=None,
        uow=None,
    ):
        """Update a draft record.

        :param identity: Identity of user creating the record.
        :type identity: `flask_principal.identity`
        :param data: Input data according to the data schema.
        :type data: dict
        :param metadata: Input data according to the metadata schema.
        :type metadata: `services.record.Marc21Metadata`
        :param files: enable/disable file support for the record.
        :type files: bool
        :param dict access: provide access additional information
        :return: marc21 record item
        :rtype: `invenio_records_resources.services.records.results.RecordItem`
        """
        data = self._create_data(identity, data, metadata, access=access)
        return super().update_draft(
            identity=identity, id_=id_, data=data, revision_id=revision_id
        )

    def _lift_embargo_from(self, record):
        """Lifts embargo from record or draft."""
        if not record.access.lift_embargo():
            raise EmbargoNotLiftedError(record["id"])
        record.access.protection.record = "public"
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
