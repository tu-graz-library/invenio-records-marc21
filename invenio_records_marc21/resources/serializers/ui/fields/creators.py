# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Metadata field for marc21 records."""

from re import search

from marshmallow.fields import Field

from .metadata import Marc21Fields


class CreatorsField(Field):
    """Schema for creators."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialize creators."""
        fields = Marc21Fields(value)

        authors = fields.get_fields("100")
        authors += fields.get_fields("700")

        creators = []

        affiliations_idx = {}
        index = {"val": 1}
        affiliation_list = []

        def _apply_idx(affiliation):
            name = affiliation.get("name")
            id_value = affiliation.get("id")

            if name not in affiliations_idx:
                affiliations_idx[name] = index["val"]
                affiliation_list.append([index["val"], name, id_value])
                index["val"] += 1
            idx = affiliations_idx[name]
            return [idx, name]

        for author in authors:

            creator = {
                "person_or_org": {
                    "type": "personal",
                    "name": author.get("a")[0],
                },
            }

            if role := author.get("4"):
                creator["role"] = {"title": role[0]}

            if orcid := author.get("2"):
                creator["person_or_org"]["identifiers"] = [
                    {
                        "scheme": "orcid",
                        "identifier": orcid[0],
                    }
                ]

            if affiliation := author.get("u"):
                matches = search(r".+(\s?\(.*\))?", affiliation[0])
                if matches:
                    try:
                        ror = matches.group(1).strip()
                    except AttributeError:
                        ror = ""
                    name = affiliation[0].replace(ror, "")
                    obj = {"name": name, "id": ror}
                    creator["affiliations"] = [_apply_idx(obj)]

            creators.append(creator)
        return {
            "creators": creators,
            "affiliations": affiliation_list,
        }
