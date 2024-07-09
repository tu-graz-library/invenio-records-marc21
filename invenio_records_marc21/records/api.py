# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Api."""

from __future__ import absolute_import, print_function

from invenio_drafts_resources.records import Draft, Record
from invenio_drafts_resources.records.api import ParentRecord as BaseParentRecord
from invenio_drafts_resources.records.systemfields import ParentField
from invenio_pidstore.models import PIDStatus
from invenio_rdm_records.records.systemfields import (
    HasDraftCheckField,
    ParentRecordAccessField,
    RecordAccessField,
    RecordDeletionStatusField,
)
from invenio_records.dumpers import SearchDumper
from invenio_records.systemfields import ConstantField, DictField, ModelField
from invenio_records_resources.records.api import FileRecord as BaseFileRecord
from invenio_records_resources.records.systemfields import (
    FilesField,
    IndexField,
    PIDField,
    PIDStatusCheckField,
)

from . import models
from .dumpers import Marc21StatisticsDumperExt
from .systemfields import (
    Marc21RecordStatisticsField,
    Marc21Status,
    MarcDraftProvider,
    MarcPIDFieldContext,
    MarcRecordProvider,
    MarcResolver,
)


#
# Parent record API
#
class Marc21Parent(BaseParentRecord):
    """Parent record."""

    versions_model_cls = models.VersionsState
    model_cls = models.ParentMetadata

    schema = ConstantField("$schema", "local://marc21/parent-v2.0.0.json")

    pid = PIDField(
        key="id",
        provider=MarcDraftProvider,
        context_cls=MarcPIDFieldContext,
        resolver_cls=MarcResolver,
        delete=False,
    )
    access = ParentRecordAccessField()


class DraftFile(BaseFileRecord):
    """Marc21 file associated with a marc21 draft model."""

    model_cls = models.DraftFile
    record_cls = None  # defined below


class CommonFieldsMixin:
    """Common fields for Marc21 records."""

    dumper = SearchDumper(
        extensions=[
            Marc21StatisticsDumperExt("stats"),
        ]
    )


class Marc21Draft(Draft, CommonFieldsMixin):
    """Marc21 draft API."""

    model_cls = models.DraftMetadata
    versions_model_cls = models.VersionsState
    parent_record_cls = Marc21Parent

    schema = ConstantField("$schema", "local://marc21/marc21-v2.0.0.json")

    index = IndexField(
        "marc21records-drafts-marc21-v2.0.0", search_alias="marc21records"
    )

    parent = ParentField(Marc21Parent, create=True, soft_delete=False, hard_delete=True)

    pid = PIDField(
        key="id",
        provider=MarcDraftProvider,
        context_cls=MarcPIDFieldContext,
        resolver_cls=MarcResolver,
        delete=False,
    )

    files = FilesField(
        store=False,
        file_cls=DraftFile,
        delete=False,
    )
    access = RecordAccessField()
    has_draft = HasDraftCheckField()

    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED, dump=True)
    status = Marc21Status()

    bucket_id = ModelField(dump=False)

    bucket = ModelField(dump=False)

    pids = DictField("pids")


DraftFile.record_cls = Marc21Draft


class RecordFile(BaseFileRecord):
    """Marc21 record file API."""

    model_cls = models.RecordFile
    record_cls = None  # defined below


class Marc21Record(Record, CommonFieldsMixin):
    """Define API for Marc21 create and manipulate."""

    model_cls = models.RecordMetadata
    versions_model_cls = models.VersionsState
    parent_record_cls = Marc21Parent

    schema = ConstantField("$schema", "local://marc21/marc21-v2.0.0.json")

    index = IndexField(
        "marc21records-marc21-marc21-v2.0.0", search_alias="marc21records-marc21"
    )

    parent = ParentField(Marc21Parent, create=True, soft_delete=False, hard_delete=True)

    pid = PIDField(
        key="id",
        provider=MarcRecordProvider,
        context_cls=MarcPIDFieldContext,
        resolver_cls=MarcResolver,
        delete=False,
    )

    files = FilesField(
        store=False,
        file_cls=RecordFile,
        create=False,
        delete=False,
    )

    access = RecordAccessField()
    has_draft = HasDraftCheckField(Marc21Draft)

    bucket_id = ModelField(dump=False)

    bucket = ModelField(dump=False)

    is_published = PIDStatusCheckField(status=PIDStatus.REGISTERED, dump=True)
    status = Marc21Status()

    pids = DictField("pids")

    deletion_status = RecordDeletionStatusField()

    stats = Marc21RecordStatisticsField()


RecordFile.record_cls = Marc21Record
