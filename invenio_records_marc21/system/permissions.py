# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resources configuration."""

from invenio_records_permissions.policies.base import BasePermissionPolicy

from ..services.generators import Marc21RecordManagers


class TemplatePermissionPolicy(BasePermissionPolicy):
    """Template permission policy."""

    can_search = (Marc21RecordManagers(),)
    can_create = (Marc21RecordManagers(),)
    can_read = (Marc21RecordManagers(),)
    can_update = (Marc21RecordManagers(),)
    can_delete = (Marc21RecordManagers(),)
