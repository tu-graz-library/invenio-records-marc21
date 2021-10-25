# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record schemas."""
from invenio_drafts_resources.services.records.schema import ParentSchema
from invenio_rdm_records.services.schemas.access import AccessSchema
from invenio_rdm_records.services.schemas.parent.access import ParentAccessSchema
from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow.decorators import post_dump
from marshmallow.fields import Boolean, Integer, List, Nested, Str
from marshmallow_utils.fields import NestedAttribute
from marshmallow_utils.permissions import FieldPermissionsMixin

from .files import FilesSchema
from .metadata import MetadataField
from .pids import PIDSchema
from .versions import VersionsSchema


class Marc21ParentSchema(ParentSchema):
    """Record schema."""

    field_dump_permissions = {
        "access": "manage",
    }

    access = Nested(ParentAccessSchema)


class Marc21RecordSchema(BaseRecordSchema, FieldPermissionsMixin):
    """Record schema."""

    id = Str()
    # pid
    pids = List(NestedAttribute(PIDSchema))

    parent = NestedAttribute(Marc21ParentSchema, dump_only=True)

    metadata = MetadataField(attribute="metadata")
    access = NestedAttribute(AccessSchema)
    files = NestedAttribute(FilesSchema, dump_only=True)

    created = Str(dump_only=True)
    updated = Str(dump_only=True)
    revision = Integer(dump_only=True)

    versions = NestedAttribute(VersionsSchema, dump_only=True)

    is_published = Boolean(dump_only=True)

    # Add version to record schema
    # versions = NestedAttribute(VersionsSchema, dump_only=True)

    @post_dump
    def default_nested(self, data, many, **kwargs):
        """Serialize metadata as empty dict for partial drafts.

        Cannot use marshmallow for Nested fields due to issue:
        https://github.com/marshmallow-code/marshmallow/issues/1566
        https://github.com/marshmallow-code/marshmallow/issues/41
        and more.
        """
        if not data.get("metadata"):
            data["metadata"] = {}

        return data


__all__ = (
    "Marc21RecordSchema",
    "Marc21ParentSchema",
)
