# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2022-2026 Graz University of Technology.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.


"""DataCite based Schema for Invenio RDM Records."""

from flask import current_app
from marshmallow import Schema, missing
from marshmallow.fields import Constant, Method, Nested


def get_scheme_datacite(
    scheme: dict,
    config_name: str,
    default: str | None = None,
) -> str:
    """Returns the datacite equivalent of a scheme."""
    config_item = current_app.config[config_name]
    return config_item.get(scheme, {}).get("datacite", default)


class CreatorSchema43(Schema):
    """Creator schema for v4."""

    name = Method("get_name")

    def get_name(self, obj: dict) -> str:
        """Get titles list."""
        names = obj.get("100", [{"subfields": {}}])[0]
        return names.get("subfields", {}).get("a", [""])[0]


class Marc21DataCite43Schema(Schema):
    """DataCite JSON 4.3 Marshmallow Schema."""

    # PIDS-FIXME: What about versioning links and related ids
    identifiers = Method("get_identifiers")
    types = Method("get_type")
    titles = Method("get_titles")
    creators = Nested(CreatorSchema43, attribute="metadata.fields")
    publisher = Method("get_publisher")
    publicationYear = Method("get_publication_year")  # noqa: N815
    schemaVersion = Constant("http://datacite.org/schema/kernel-4")  # noqa: N815

    def get_type(self, _: dict) -> dict[str, str]:
        """Get resource type."""
        # FIXME: The metadatafield 970 from dojson module needed
        return {
            "resourceTypeGeneral": "Other",
            "resourceType": "Text",
        }

    def _get_field(self, obj: dict, field_number: str, default: None = None) -> dict:
        """Get field from metadata."""
        fields = obj["metadata"].get("fields", {})
        return fields.get(field_number, default)

    def _get_subfields(self, obj: dict, field_number: str) -> dict:
        """Get subfields from metadata."""
        return self._get_field(obj, field_number, default=[{"subfields": {}}])[0].get(
            "subfields", {}
        )

    def get_titles(self, obj: dict) -> list[dict[str, str]]:
        """Get titles list."""
        titles_field = self._get_subfields(obj, "245")

        title_fields = titles_field.get("a", [""])
        return [{"title": title} for title in title_fields]

    def get_publisher(self, obj: dict) -> str:
        """Get publisher."""
        for field_number in ["260", "264"]:
            publisher_field = self._get_subfields(obj, field_number)
            publisher: list[str] = publisher_field.get("b")
            if publisher:
                return publisher[0]

        return current_app.config.get("MARC21_DATACITE_DEFAULT_PUBLISHER")

    def get_publication_year(self, obj: dict) -> str | None:
        """Get publication year from edtf date."""
        publication_dates = self._get_field(obj, "008", None)
        if publication_dates:
            publication_date: str = publication_dates[7:11]
            return publication_date

        # Production, Publication, Distribution, Manufacture, and Copyright Notice
        ppdmcn = self._get_subfields(obj, "264")
        if ppdmcn:
            return ppdmcn.get("c")[0]

        return None

    def get_identifiers(self, obj: dict) -> list | missing:
        """Get (main and alternate) identifiers list."""
        serialized_identifiers = []

        # pids go first so the DOI from the record is included
        pids = obj.get("pids", {})
        for scheme, id_ in pids.items():
            id_scheme = get_scheme_datacite(
                scheme,
                "MARC21_IDENTIFIERS_SCHEMES",
                default=scheme,
            )

            if id_scheme:
                serialized_identifiers.append(
                    {
                        "identifier": id_["identifier"],
                        "identifierType": id_scheme,
                    },
                )

        return serialized_identifiers or missing
