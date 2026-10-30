# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 Record Resource."""

from dataclasses import dataclass

from flask_principal import Identity
from invenio_records_resources.services import RecordService


@dataclass
class Marc21Template:
    """Marc21 Template dataclass."""

    def to_dict(self) -> dict:
        """To dict."""
        return {}


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
