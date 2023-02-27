# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record metadata component."""

from copy import copy

from invenio_records_resources.services.records.components import (
    MetadataComponent as BaseMetadataComponent,
)


class MetadataComponent(BaseMetadataComponent):
    """Service component for metadata."""

    def create(self, identity, data=None, record=None, errors=None, **kwargs):
        """Inject parsed metadata to the record."""
        record.metadata = data.get("metadata", {})

    def update(self, identity, data=None, record=None, **kwargs):
        """Inject parsed metadata to the record."""
        record.metadata = data.get("metadata", {})

    def update_draft(self, identity, data=None, record=None, **kwargs):
        """Inject parsed metadata to the record."""
        record.metadata = data.get("metadata", {})

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        record.metadata = draft.get("metadata", {})

    def edit(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.metadata = record.get("metadata", {})

    def new_version(self, identity, draft=None, record=None, **kwargs):
        """New version metadata."""
        draft.metadata = copy(record.get("metadata", {}))
