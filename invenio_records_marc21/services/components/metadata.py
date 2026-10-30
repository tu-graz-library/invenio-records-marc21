# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 record metadata component."""

from copy import copy

from flask_principal import Identity
from invenio_records_resources.services.records.components import (
    MetadataComponent as BaseMetadataComponent,
)

from ...records.api import Marc21Draft, Marc21Record


class MetadataComponent(BaseMetadataComponent):
    """Service component for metadata."""

    def create(  # type: ignore[override]
        self,
        _: Identity,
        data: dict,
        record: Marc21Record,
        **__: dict,
    ) -> None:
        """Inject parsed metadata to the record."""
        record.metadata = data.get("metadata", {})

    def update(  # type: ignore[override]
        self,
        _: Identity,
        data: dict,
        record: Marc21Record,
        **__: dict,
    ) -> None:
        """Inject parsed metadata to the record."""
        record.metadata = data.get("metadata", {})

    def update_draft(  # type: ignore[override]
        self,
        _: Identity,
        data: dict,
        record: Marc21Record,
        **__: dict,
    ) -> None:
        """Inject parsed metadata to the record."""
        record.metadata = data.get("metadata", {})

    def publish(  # type: ignore[override]
        self,
        _: Identity,
        draft: Marc21Draft,
        record: Marc21Record,
        **__: dict,
    ) -> None:
        """Update draft metadata."""
        record.metadata = draft.get("metadata", {})

    def edit(  # type: ignore[override]
        self,
        _: Identity,
        draft: Marc21Draft,
        record: Marc21Record,
        **__: dict,
    ) -> None:
        """Update draft metadata."""
        draft.metadata = record.get("metadata", {})

    def new_version(  # type: ignore[override]
        self,
        _: Identity,
        draft: Marc21Draft,
        record: Marc21Record,
        **__: dict,
    ) -> None:
        """New version metadata."""
        draft.metadata = copy(record.get("metadata", {}))
