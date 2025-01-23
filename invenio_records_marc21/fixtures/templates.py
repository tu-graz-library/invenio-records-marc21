# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 fixtures templates."""

from ..proxies import current_records_marc21
from .utils import load_json


def create_templates(filename):
    """Create templates with the service."""
    data_to_use = load_json(filename)

    service = current_records_marc21.templates_service
    templates = []
    for data in data_to_use:
        template = service.create(data=data["values"], name=data["name"])
        templates.append(template.to_dict())
    return templates


def delete_templates(name, all, force):
    """Delete templates with the service."""
    service = current_records_marc21.templates_service
    result = service.delete(name=name, all=all, force=force)
    return result
