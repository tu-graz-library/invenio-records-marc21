# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2022 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Metadata field for marc21 records."""
import re
from dataclasses import dataclass
from typing import Dict, List

from marshmallow.fields import Field


class Marc21Controlfield:
    """Marc21Controlfield."""

    def __init__(self, value):
        """Constructor."""
        self.value = value


@dataclass
class Marc21Datafield:
    """Marc21Datafield."""

    ind1: str
    ind2: str
    subfields: Dict[str, List[str]]

    def get(self, subfield_notation: str) -> List[str]:
        """Get subfield value by subfield notation."""
        return self.subfields[subfield_notation]

    def __contains__(self, subfield_notation):
        """Contains subfield_notation."""
        return subfield_notation in self.subfields


class Marc21Fields:
    """Marc21Fields."""

    def __init__(self, fields):
        """Constructor."""
        self.fields = {
            field_number: [
                Marc21Datafield(**field)
                if isinstance(field, dict)
                else Marc21Controlfield(field)
                for field in fs
            ]
            for field_number, fs in fields.items()
        }

    def __contains__(self, field_number):
        """Check if a field_number exists in the field list."""
        return field_number in self.fields

    def get_fields(
        self,
        field_number: str,
        ind1: str = None,
        ind2: str = None,
        subfield_notation: str = None,
    ) -> List[Marc21Datafield]:
        """Get field by and combination of parameter values."""
        fields = self.fields.get(field_number, [])

        if not fields:
            return fields

        if not ind1 and not ind2:
            return fields

        fields = [
            field for field in fields if field.ind1 == ind1 and field.ind2 == ind2
        ]

        if not subfield_notation:
            return fields

        return [field for field in fields if subfield_notation in field]

    def get_values(
        self,
        field_number: str,
        ind1: str = None,
        ind2: str = None,
        subfield_notation: str = None,
    ) -> List[str]:
        """Get value of field by and combination of parameter values."""
        fields = self.get_fields(field_number, ind1, ind2, subfield_notation)

        if not fields:
            return []

        if not subfield_notation:
            return fields

        values = []
        for field in fields:
            values += field.get(subfield_notation)

        return values

    def get_subfields(
        self,
        field_number: str,
        ind1: str = None,
        ind2: str = None,
        subfield_notations: List[str] = None,
    ) -> List[Dict[str, List[str]]]:
        """Get subfields."""
        mostly_important_subfield_notation = (
            subfield_notations[0] if subfield_notations else None
        )
        fields = self.get_fields(
            field_number, ind1, ind2, mostly_important_subfield_notation
        )

        if not fields:
            return []

        if not subfield_notations:
            return fields

        out = []
        for field in fields:
            obj = {subfield_notation: [] for subfield_notation in subfield_notations}
            for subfield_notation in subfield_notations:
                if subfield_notation in field:
                    obj[subfield_notation] += field.get(subfield_notation)
            out.append(obj)

        return out


class MetadataField(Field):
    """Schema for the record metadata."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialise access status."""
        fields = Marc21Fields(value.get("fields", {}))
        out = {}

        if not fields:
            return out

        return {
            "languages": fields.get_values("041", subfield_notation="a"),
            "authors": self.get_authors(fields),
            "titles": self.get_titles(fields),
            "copyright": fields.get_values("264"),
            "description": self.get_description(fields),
            "notes": fields.get_values("500"),
            "resource_type": self.get_resource_type(fields),
        }

    def get_authors(self, fields):
        """Get authors."""
        authors = []

        if "100" in fields:
            authors += fields.get_subfields("100", subfield_notations=["a", "8"])

        if "700" in fields:
            authors += fields.get_subfields("700", subfield_notations=["a", "8"])

        return authors

    def get_titles(self, fields):
        """Get title."""
        titles = fields.get_values("245", subfield_notation="a")
        return [re.sub(r"[<>]", "", title) for title in titles]

    def get_description(self, fields):
        """Get descriptions."""
        descriptions = fields.get_subfields("300", subfield_notations=["a", "b"])

        out = []
        for desc in descriptions:
            for _, val in desc.items():
                out.append(", ".join(val))

        return ", ".join(out)

    def get_resource_type(self, fields):
        """Get resource type."""
        resource_type = fields.get_values("970", "2", "_", subfield_notation="d")

        if resource_type:
            return resource_type[0]

        return ""
