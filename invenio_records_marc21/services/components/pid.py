# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 external pid component."""

from flask_principal import Identity
from invenio_drafts_resources.services.records.components import (
    PIDComponent as BasePIDComponent,
)

from ...records.api import Marc21Record


class PIDComponent(BasePIDComponent):
    """Service component for pids integration."""

    def create(  # type: ignore[override]
        self,
        identity: Identity,  # noqa: ARG002
        data: dict,  # noqa: ARG002
        record: Marc21Record = None,
        errors: dict | None = None,  # noqa: ARG002
    ) -> None:
        """Create PID when record is created.."""
        self.service.record_cls.pid.create(record)
