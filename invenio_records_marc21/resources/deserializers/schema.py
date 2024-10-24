# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 record response deserializers."""

from marshmallow import EXCLUDE, Schema, fields, pre_load


class Marc21Schema(Schema):
    """Marc21 schema."""

    class Meta:
        """Meta class to accept unknwon fields."""

        unknown = EXCLUDE
        additional = (
            "id",
            "pids",
            "access",
            "parent",
            "files",
        )

    metadata = fields.Method(deserialize="load_metadata")

    def load_metadata(self, value):
        """Load metadata."""
        fields = {}

        for field in value["fields"]:
            if int(field["id"]) < 10:
                fields[field["id"]] = field["subfield"]
            else:
                if field["id"] not in fields:
                    fields[field["id"]] = []

                subfields = {
                    v[0:1]: [v[2:].strip()] for v in field["subfield"].split("$$")[1:]
                }

                fields[field["id"]].append(
                    {
                        "ind1": field["ind1"],
                        "ind2": field["ind2"],
                        "subfields": subfields,
                    }
                )
        return {
            "fields": fields,
            "leader": value["leader"],
        }

    @pre_load
    def remove(self, data, **kwargs):
        """Remove."""
        if "id" in data and data["id"] is None:
            del data["id"]

        if "pids" in data and data["pids"] is None:
            del data["pids"]

        return data
