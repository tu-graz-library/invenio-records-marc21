# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions generators for Invenio Marc21 Records."""
from typing import cast

from flask import current_app, g
from flask_principal import Identity
from invenio_records_permissions.generators import Generator
from invenio_search.engine import dsl

from ..records.api import Marc21Record


class Marc21RecordCreators(Generator):
    """Allows record owners."""

    def needs(  # type: ignore[override]
        self,
        identity: Identity | None = None,
        record: Marc21Record | None = None,
        **__: dict,
    ) -> list:
        """Get Needs.

        The creator is only allowed to interact with the record which is created
        by the creator.
        """
        if record is None or identity is None:
            return cast(list, current_app.config.get("MARC21_RECORD_CREATOR_NEEDS", []))

        if identity.id == record.parent.access.owner.owner_id:
            return cast(list, current_app.config.get("MARC21_RECORD_CREATOR_NEEDS", []))

        return []

    def excludes(  # type: ignore[override]
        self,
        identity: Identity | None = None,
        record: Marc21Record | None = None,
        **__: dict,
    ) -> list:
        """Preventing Needs.

        The creator is only allowed to interact with the record created by the
        creator. By returning the role if the record is not created by the
        creator is prevents the user of interacting with the record.
        """
        if record is None:
            return []
        # TODO: why is not identity used?
        # TODO: because of strange tests behavior
        if "identity" not in g:
            return []

        if g.identity.id == record.parent.access.owner.owner_id:
            return []

        return cast(list, current_app.config.get("MARC21_RECORD_CREATOR_NEEDS", []))

    def query_filter(self, identity: Identity, **__: dict) -> dsl.Query | None:  # type: ignore[override]
        """Allow only to see records which the creator has created."""
        users = [n.value for n in identity.provides if n.method == "id"]
        if users:
            return dsl.Q("terms", **{"parent.access.owned_by.user": users})

        return None


class Marc21RecordManagers(Generator):
    """Allows record owners."""

    def needs(self, **__: dict) -> list:
        """Get Needs."""
        return cast(list, current_app.config.get("MARC21_RECORD_MANAGER_NEEDS", []))

    def query_filter(self, **__: dict) -> dsl.Query:
        """Allow to see any record."""
        return dsl.Q("match_all")


class Marc21RecordCurators(Generator):
    """Allows curator to modify other records."""

    def needs(self, **__: dict) -> list:
        """Get needs."""
        return cast(list, current_app.config.get("MARC21_RECORD_CURATOR_NEEDS", []))
