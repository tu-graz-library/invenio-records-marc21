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

from json import load
from pathlib import Path

from ..proxies import current_records_marc21


def create_templates(filename: Path) -> list[dict]:
    """Create templates with the service."""
    with Path(Path(__file__).parent / filename).open("rb") as fp:
        data_to_use = load(fp)

    service = current_records_marc21.templates_service
    templates = []
    for data in data_to_use:
        template = service.create(data=data["values"], name=data["name"])
        templates.append(template.to_dict())
    return templates


def delete_templates(name: str, all: bool, force: bool):
    """Delete templates with the service."""
    service = current_records_marc21.templates_service
    result = service.delete(name=name, all=all, force=force)
    return result
