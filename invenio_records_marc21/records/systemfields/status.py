# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Marc21 status field."""

from invenio_records.systemfields import SystemField


class Marc21Status(SystemField):
    """Marc21 record status field which checks the state."""

    def __init__(self, key=None):
        """Initialize the Status.

        It stores the `draft.draft_status` value in the record metadata.

        :param key: Attribute name to store the DraftStatus value.
        """
        super().__init__(key=key)

    def __get__(self, record, owner=None):
        """Get the persistent identifier."""
        if record is None:
            return "draft"

        is_published = getattr(record, "is_published")

        if is_published:
            return "published"

        return "draft"
