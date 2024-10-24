# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Schema for marc21 deposit records."""

from marshmallow.fields import Field

from ..schema import Marc21Schema


class MetadataDepositField(Field):
    """Metadata deposit field."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize metadata field."""
        fields_ui = []

        for category, fields in value["fields"].items():
            if isinstance(fields, str):
                obj = {
                    "id": category,
                    "ind1": " ",
                    "ind2": " ",
                    "subfield": fields,
                }
                fields_ui.append(obj)
            else:
                for field in fields:
                    subfields = " ".join(
                        f"$${k} {v[0]}" for k, v in field["subfields"].items()
                    )

                    obj = {
                        "id": category,
                        "ind1": field["ind1"].replace("_", " "),
                        "ind2": field["ind2"].replace("_", " "),
                        "subfield": subfields,
                    }

                    fields_ui.append(obj)

        return {
            "fields": fields_ui,
            "leader": value.get("leader"),
        }


class Marc21DepositSchema(Marc21Schema):
    """Marc21 deposit schema."""

    class Meta:
        """Meta class to accept unknwon fields."""

        additional = (
            "access",
            "status",
            "parent",
            "links",
            "files",
            "is_published",
            "pids",
            "versions",
        )

    metadata = MetadataDepositField(attribute="metadata")
