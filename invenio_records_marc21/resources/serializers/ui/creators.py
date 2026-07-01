# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Metadata field for marc21 records."""

from re import search
from typing import cast

from marshmallow.fields import Field

from ....services.record.metadata import DataField, Marc21Metadata


class CreatorsField(Field):
    """Schema for creators."""

    def _serialize(
        self,
        value: dict,
        attr: str | None,  # noqa: ARG002
        obj: dict,
        **kwargs: dict,  # noqa: ARG002
    ) -> dict:
        """Serialize creators."""
        metadata = Marc21Metadata(json=value)

        _, authors_100 = metadata.get_fields("100")
        _, authors_700 = metadata.get_fields("700")

        authors: list[DataField] = [*authors_100, *authors_700]

        creators = []

        affiliations_idx = {}
        index = {"val": 1}
        affiliation_list = []

        def _apply_idx(affiliation: dict) -> tuple[int, str]:
            name: str = cast(str, affiliation.get("name"))
            id_value = affiliation.get("id")

            if name not in affiliations_idx:
                affiliations_idx[name] = index["val"]
                affiliation_list.append([index["val"], name, id_value])
                index["val"] += 1
            idx = affiliations_idx[name]
            return idx, name

        for author in authors:

            creator: dict = {
                "person_or_org": {
                    "type": "personal",
                    "name": author.get("a"),
                },
            }

            if role := author.get("4"):
                creator["role"] = {"title": role}

            if orcid := author.get("2"):
                creator["person_or_org"]["identifiers"] = [
                    {
                        "scheme": "orcid",
                        "identifier": orcid,
                    },
                ]

            if affiliation := author.get("u"):
                matches = search(r".+(\s?\(.*\))?", affiliation)
                if matches:
                    try:
                        ror = matches.group(1).strip()
                    except AttributeError:
                        ror = ""
                    name = affiliation.replace(ror, "")
                    obj = {"name": name, "id": ror}
                    creator["affiliations"] = [_apply_idx(obj)]

            creators.append(creator)
        return {
            "creators": creators,
            "affiliations": affiliation_list,
        }
