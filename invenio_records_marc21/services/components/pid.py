# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 external pid component."""

from flask_principal import Identity
from invenio_drafts_resources.services.records.components import (
    PIDComponent as BasePIDComponent,
)

from ...records.api import Marc21Record


class PIDComponent(BasePIDComponent):
    """Service component for pids integration."""

    def create(
        self,
        identity: Identity,  # noqa: ARG002
        data: dict,  # noqa: ARG002
        record: Marc21Record = None,
        errors: dict | None = None,  # noqa: ARG002
    ) -> None:  # type: ignore[override]
        """Create PID when record is created.."""
        self.service.record_cls.pid.create(record)
