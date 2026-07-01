# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Metadata field for marc21 records."""

import re

from invenio_i18n import gettext as _
from marshmallow.fields import Field

from ....records.fields.resourcetype import ResourceTypeEnum
from ....services.record.metadata import Marc21Metadata


class MetadataField(Field):
    """Schema for the record metadata."""

    def _serialize(self, value: dict, attr: str, obj: dict, **__: dict) -> dict:
        """Serialise access status."""
        metadata = Marc21Metadata(json=value)

        return {
            "languages": metadata.get_values("041", subf_code="a"),
            "authors": self.get_authors(metadata),
            "titles": self.get_titles(metadata),
            "copyright": metadata.get_values("264"),
            "description": self.get_description(metadata),
            "notes": metadata.get_values("500"),
            "resource_type": self.get_resource_type(metadata),
            "published": self.get_published_month(metadata),
            "publisher": self.get_publisher(metadata),
            "license": self.get_license(metadata),
            "youtube": self.get_youtube(metadata),
            "isbn": self.get_isbn(metadata),
            "terms_of_use": self.get_terms_of_use(metadata),
            "included_in": self.get_included_in(metadata),
            "version": self.get_version_of_record(metadata),
        }

    def get_authors(self, metadata: Marc21Metadata) -> list[dict]:
        """Get authors."""
        authors = []

        _, author = metadata.get_fields("100")
        authors += [a.subfields for a in author]

        _, author = metadata.get_fields("700")
        authors += [a.subfields for a in author]

        return authors

    def get_titles(self, metadata: Marc21Metadata) -> list[str]:
        """Get title.

        The normal separator between the main title and the additional
        title is ':'.

        There are special cases where the 245 subfield 'b' has a '='
        in front. If this happens the separator between 'a' and 'b'
        should not be ':' because there is already the '=' as a
        separator.
        """
        titles = metadata.get_values("245", subf_code="a")
        additional_titles = metadata.get_values("245", subf_code="b")

        if len(additional_titles) > 0 and additional_titles[0][0] != "=":
            titles += [":"]

        titles += additional_titles

        return [re.sub(r"[<>]", "", title) for title in titles]

    def get_published_month(self, metadata: Marc21Metadata) -> str:
        """Get published month."""
        values = metadata.get_values("260", subf_code="c")
        if len(values) > 0:
            return "".join(values)
        values = metadata.get_values("264", subf_code="c")
        if len(values) > 0:
            return "".join(values)
        return ""

    def get_publisher(self, metadata: Marc21Metadata) -> str:
        """Get publisher."""
        values = metadata.get_values("260", subf_code="b")
        if len(values) > 0:
            return "".join(values)
        values = metadata.get_values("264", subf_code="b")
        if len(values) > 0:
            return "".join(values)
        return ""

    def get_license(self, metadata: Marc21Metadata) -> dict[str, str]:
        """Get license."""
        shorts = metadata.get_values("540", subf_code="f")
        urls = metadata.get_values("540", subf_code="u")

        short = shorts[0] if shorts else ""
        url = urls[0] if urls else ""
        return {"url": url, "short": short}

    def get_youtube(self, metadata: Marc21Metadata) -> str:
        """Get youtube."""
        _, fields = metadata.get_fields("856")

        if len(fields) == 0:
            return ""

        for field in fields:
            if field.get("a") == "youtube":
                return field.get("u")

        return ""

    def get_publisher_doi(self, metadata: Marc21Metadata) -> str:
        """Get youtube."""
        _, fields = metadata.get_fields("856")

        if len(fields) == 0:
            return ""

        for field in fields:
            if field.get("a") == "publisher":
                return field.get("u")

        return ""

    def get_description(self, metadata: Marc21Metadata) -> str:
        """Get descriptions."""
        _, descriptions = metadata.get_fields("300")

        out = []
        for desc in descriptions:
            out += [", ".join(val) for val in desc.subfields.values()]

        return ", ".join(out)

    def get_resource_type(self, metadata: Marc21Metadata) -> str:
        """Get resource type."""
        resource_type = metadata.get_values("970", ind1="2", subf_code="d")
        resource_types = {
            ResourceTypeEnum.HSMASTER.value: _("Masterthesis"),
            ResourceTypeEnum.HSDISS.value: _("Dissertation"),
        }

        if not resource_type:
            return ""

        return resource_types.get(resource_type[0], resource_type[0])

    def get_isbn(self, metadata: Marc21Metadata) -> str:
        """Get isbn."""
        # print(f"MetadataField.get_isbn metadata: {metadata}")
