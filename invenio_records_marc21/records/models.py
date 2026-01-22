# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Marc21 Record and Draft models."""

from invenio_db import db
from invenio_drafts_resources.records import (
    DraftMetadataBase,
    ParentRecordMixin,
    ParentRecordStateMixin,
)
from invenio_files_rest.models import Bucket
from invenio_rdm_records.records.systemfields.deletion_status import (
    RecordDeletionStatusEnum,
)
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records.models import FileRecordModelMixin
from sqlalchemy_utils.types import ChoiceType, UUIDType


class Marc21ParentMetadata(db.Model, RecordMetadataBase):
    """Metadata store for the parent record."""

    __tablename__ = "marc21_parents_metadata"


class Marc21RecordMetadata(db.Model, RecordMetadataBase, ParentRecordMixin):
    """Represent a marc21 record metadata."""

    __tablename__ = "marc21_records_metadata"
    __parent_record_model__ = Marc21ParentMetadata
    __versioned__ = {}

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)

    # The deletion status is stored in the model so that we can use it in SQL queries
    deletion_status = db.Column(
        ChoiceType(RecordDeletionStatusEnum, impl=db.String(1)),
        nullable=False,
        default=RecordDeletionStatusEnum.PUBLISHED.value,
    )


class Marc21DraftMetadata(db.Model, DraftMetadataBase, ParentRecordMixin):
    """Represent a marc21 record draft metadata."""

    __tablename__ = "marc21_drafts_metadata"
    __parent_record_model__ = Marc21ParentMetadata

    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class Marc21RecordFile(db.Model, RecordMetadataBase, FileRecordModelMixin):
    """File associated with a marc21 record."""

    __tablename__ = "marc21_records_files"
    __record_model_cls__ = Marc21RecordMetadata
    __versioned__ = {}


class Marc21DraftFile(db.Model, RecordMetadataBase, FileRecordModelMixin):
    """File associated with a marc21 draft."""

    __tablename__ = "marc21_drafts_files"
    __record_model_cls__ = Marc21DraftMetadata


class Marc21VersionsState(db.Model, ParentRecordStateMixin):
    """Store for the version state of the parent record."""

    __tablename__ = "marc21_versions_state"
    __parent_record_model__ = Marc21ParentMetadata
    __record_model__ = Marc21RecordMetadata
    __draft_model__ = Marc21DraftMetadata
