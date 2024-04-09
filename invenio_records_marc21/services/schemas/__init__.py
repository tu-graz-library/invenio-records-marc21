# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record schemas."""

from flask import current_app
from invenio_drafts_resources.services.records.schema import ParentSchema
from invenio_i18n import lazy_gettext as _
from invenio_rdm_records.services.schemas.access import AccessSchema
from invenio_rdm_records.services.schemas.files import FilesSchema
from invenio_rdm_records.services.schemas.parent.access import ParentAccessSchema
from invenio_rdm_records.services.schemas.versions import VersionsSchema
from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import ValidationError
from marshmallow.decorators import post_dump
from marshmallow.fields import Boolean, Dict, Integer, Nested, Str
from marshmallow_utils.fields import NestedAttribute, SanitizedUnicode
from marshmallow_utils.permissions import FieldPermissionsMixin

from .metadata import MetadataSchema
from .pids import PIDSchema
from .statistics import Marc21StatisticSchema


def validate_scheme(scheme):
    """Validate a PID scheme."""
    if scheme not in current_app.config["MARC21_PERSISTENT_IDENTIFIERS"]:
        raise ValidationError(_("Invalid persistent identifier scheme."))


class Marc21ParentSchema(ParentSchema):
    """Record schema."""

    field_dump_permissions = {
        "access": "manage",
    }

    access = Nested(ParentAccessSchema)


class Marc21RecordSchema(BaseRecordSchema, FieldPermissionsMixin):
    """Record schema."""

    field_load_permissions = {
        "files": "update_draft",
    }
    id = Str()

    pids = Dict(
        keys=SanitizedUnicode(validate=validate_scheme),
        values=Nested(PIDSchema),
    )

    parent = NestedAttribute(Marc21ParentSchema, dump_only=True)

    metadata = NestedAttribute(MetadataSchema)
    access = NestedAttribute(AccessSchema)
    files = NestedAttribute(FilesSchema)

    created = Str(dump_only=True)
    updated = Str(dump_only=True)
    revision = Integer(dump_only=True)

    versions = NestedAttribute(VersionsSchema, dump_only=True)

    is_published = Boolean(dump_only=True)
    status = Str(dump_only=True)

    stats = NestedAttribute(Marc21StatisticSchema, dump_only=True)

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
        if not data.get("pids"):
            data["pids"] = {}

        return data


__all__ = (
    "Marc21RecordSchema",
    "Marc21ParentSchema",
)
