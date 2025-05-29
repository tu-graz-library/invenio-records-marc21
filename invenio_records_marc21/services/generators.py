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

from flask import current_app, g
from invenio_records_permissions.generators import Generator
from invenio_search.engine import dsl


class Marc21RecordCreators(Generator):
    """Allows record owners."""

    def needs(self, identity=None, record=None, **kwargs):
        """Enabling Needs.

        The creator is only allowed to interact with the record which is created
        by the creator.
        """
        if record is None or identity is None:
            return current_app.config.get("MARC21_RECORD_CREATOR_NEEDS", [])

        if identity.id == record.parent.access.owner.owner_id:
            return current_app.config.get("MARC21_RECORD_CREATOR_NEEDS", [])

        return []

    def excludes(self, identity=None, record=None, **kwargs):
        """Preventing Needs.

        The creator is only allowed to interact with the record created by the
        creator. By returning the role if the record is not created by the
        creator is prevents the user of interacting with the record.
        """
        if record is None:
            return []

        # TODO: because of strange tests behavior
        if "identity" not in g:
            return []

        if g.identity.id == record.parent.access.owner.owner_id:
            return []

        return current_app.config.get("MARC21_RECORD_CREATOR_NEEDS", [])

    def query_filter(self, identity=None, **kwargs):
        """Allow only to see records which the creator has created."""
        users = [n.value for n in identity.provides if n.method == "id"]
        if users:
            return dsl.Q("terms", **{"parent.access.owned_by.user": users})


class Marc21RecordManagers(Generator):
    """Allows record owners."""

    def needs(self, **kwargs):
        """Enabling Needs."""
        return current_app.config.get("MARC21_RECORD_MANAGER_NEEDS", [])

    def query_filter(self, identity=None, **kwargs):
        """Allow to see any record."""
        return dsl.Q("match_all")


class Marc21RecordCurators(Generator):
    """Allows curator to modify other records."""

    def needs(self, **kwargs):
        """Enabling needs."""
        return current_app.config.get("MARC21_RECORD_CURATOR_NEEDS", [])
