# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resources configuration."""

from invenio_records_resources.services.base.config import ConfiguratorMixin

from .apis import Marc21Template
from .permissions import TemplatePermissionPolicy


class Marc21TemplateServiceConfig(ConfiguratorMixin):
    """Marc21 Record resource configuration."""

    record_cls = Marc21Template
    permission_policy_cls = TemplatePermissionPolicy
