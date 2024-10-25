# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions generators for Invenio Marc21 Records."""

from flask import current_app
from invenio_records_permissions.generators import Generator


class Marc21RecordCreators(Generator):
    """Allows record owners."""

    def needs(self, **kwargs):
        """Enabling Needs."""
        return current_app.config.get("MARC21_RECORD_CREATOR_NEEDS", [])


class Marc21RecordManagers(Generator):
    """Allows record owners."""

    def needs(self, **kwargs):
        """Enabling Needs."""
        return current_app.config.get("MARC21_RECORD_MANAGER_NEEDS", [])


class Marc21RecordCurators(Generator):
    """Allows curator to modify other records."""

    def needs(self, **kwargs):
        """Enabling needs."""
        return current_app.config.get("MARC21_RECORD_CURATOR_NEEDS", [])
