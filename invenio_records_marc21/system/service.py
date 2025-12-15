# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Marc21 Record Resource."""

from dataclasses import dataclass

from flask_principal import Identity
from invenio_records_resources.services import RecordService


@dataclass
class Marc21Template:
    """Marc21 Template dataclass."""


#
# Template service
#
class Marc21TemplateService(RecordService):
    """Marc21 template resource."""

    def get_templates(
        self,
        identity: Identity,
    ) -> list[Marc21Template]:
        """Get templates for a new record."""
        # TODO:
        # return templates according to the roles in the identity
        # over the scan or search function of RecordService
