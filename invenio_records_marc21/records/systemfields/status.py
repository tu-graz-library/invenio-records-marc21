# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

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
