# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Schema for marc21 ui records."""

from functools import partial

from flask_babelex import get_locale
from invenio_rdm_records.resources.serializers.ui.fields import AccessStatusField
from marshmallow_utils.fields import FormatDate as BaseFormatDatetime
from marshmallow_utils.fields import Function, SanitizedUnicode

from ..schema import Marc21Schema
from .fields import MetadataField

FormatDatetime = partial(BaseFormatDatetime, locale=get_locale)


def record_version(obj):
    """Return record's version."""
    # TODO default should be used the field 251, but that is not yet
    # implemented in dojson
    return f"v{obj['versions']['index']}"


class Marc21UISchema(Marc21Schema):
    """Schema for dumping extra information for the UI."""

    id = SanitizedUnicode(data_key="id", attribute="id")

    class Meta:
        """Meta class to accept unknwon fields."""

        additional = (
            "access",
            "status",
            "parent",
            "links",
            "files",
        )

    access_status = AccessStatusField(attribute="access", dump_only=True)

    metadata = MetadataField(attribute="metadata")

    created = FormatDatetime(attribute="created", format="long")

    updated = FormatDatetime(attribute="updated", format="long")

    version = Function(record_version)
