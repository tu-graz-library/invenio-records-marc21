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
from marshmallow_utils.fields import SanitizedUnicode

from ..schema import Marc21Schema

FormatDatetime = partial(BaseFormatDatetime, locale=get_locale)


class Marc21UISchema(Marc21Schema):
    """Schema for dumping extra information for the UI."""

    id = SanitizedUnicode(data_key="id", attribute="id")

    access_status = AccessStatusField(attribute="access")

    created = FormatDatetime(attribute="created", format="long")

    updated = FormatDatetime(attribute="updated", format="long")
