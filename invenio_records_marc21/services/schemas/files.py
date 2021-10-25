# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Marc21 record files schemas."""

from marshmallow import Schema, fields
from marshmallow_utils.fields import SanitizedUnicode
from marshmallow_utils.permissions import FieldPermissionsMixin


class FileSchema(Schema):
    """File schema."""

    type = fields.String()
    checksum = fields.String()
    size = fields.Integer()
    key = SanitizedUnicode()
    version_id = SanitizedUnicode()
    bucket_id = SanitizedUnicode()
    mimetype = SanitizedUnicode()
    storage_class = SanitizedUnicode()


class FilesSchema(Schema, FieldPermissionsMixin):
    """Files metadata schema."""

    enabled = fields.Bool()
    default_preview = SanitizedUnicode()
    order = fields.List(SanitizedUnicode())
