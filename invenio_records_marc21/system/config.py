# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Resources configuration."""

from invenio_records_resources.services.base.config import ConfiguratorMixin

from .apis import Marc21Template
from .permissions import TemplatePermissionPolicy


class Marc21TemplateServiceConfig(ConfiguratorMixin):
    """Marc21 Record resource configuration."""

    record_cls = Marc21Template
    permission_policy_cls = TemplatePermissionPolicy
