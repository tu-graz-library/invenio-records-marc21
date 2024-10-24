# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Metadata field for marc21 records."""


from marshmallow.fields import Field


def field_subfields(value: list):
    """MARC21 get list of subfields from json."""
    subfields = dict(*[field.get("subfields", {}) for field in value])
    return subfields


def field_subfield(key: str, subfields: dict):
    """Find subfield in a list of subfields dicts."""
    subfield = subfields.get(key, [])
    if isinstance(subfield, list):
        subfield = ", ".join(subfield)
    return subfield if subfield else ""


class MetadataField(Field):
    """Schema for the record metadata."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialise access status."""
        fields = value.get("fields", [])
        out = {}

        if value:
            language_code = field_subfields(fields.get("041", []))
            title_statement = field_subfields(fields.get("245", []))
            manufacture_copyright = field_subfields(fields.get("264", []))
            main_entry_personal_name = field_subfields(fields.get("100", []))
            physical_description = field_subfields(fields.get("300", []))
            general_note = field_subfields(fields.get("500", []))
            dissertation_note = field_subfields(fields.get("502", []))

            out = {
                "main_entry_personal_name": {
                    "personal_name": field_subfield("a", main_entry_personal_name),
                    "relator_code": field_subfield("4", main_entry_personal_name),
                },
                "title_statement": {"title": field_subfield("a", title_statement)},
                "physical_description": {
                    "extent": field_subfield("a", physical_description)
                },
                "dissertation_note": {
                    "dissertation_note": field_subfield("a", dissertation_note)
                },
                "general_note": {"general_note": field_subfield("a", general_note)},
                "production_publication_distribution_manufacture_and_copyright_notice": {
                    "date_of_production_publication_distribution_manufacture_or_copyright_notice": field_subfield(
                        "c", manufacture_copyright
                    )
                },
                "language_code": {
                    "language_code_of_text_sound_track_or_separate_title": field_subfield(
                        "a", language_code
                    )
                },
            }

        return out
