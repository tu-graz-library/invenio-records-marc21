# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2022-2026 Graz University of Technology.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.


"""DataCite based Schema for Invenio RDM Records."""

from urllib.parse import urlparse

from flask import current_app
from marshmallow import Schema, missing
from marshmallow.fields import Constant, Method

from ....services.record import Marc21Metadata


def get_scheme_datacite(
    scheme: dict,
    config_name: str,
    default: str | None = None,
) -> str:
    """Returns the datacite equivalent of a scheme."""
    config_item = current_app.config[config_name]
    return config_item.get(scheme, {}).get("datacite", default)


class Marc21DataCite43Schema(Schema):
    """DataCite JSON 4.3 Marshmallow Schema."""

    _metadata = None

    # PIDS-FIXME: What about versioning links and related ids
    identifiers = Method("get_identifiers")
    types = Method("get_type")  # todo ->: contact Alex regarding more exact type than "Other"
    titles = Method("get_titles")
    creators = Method("get_creators")
    publisher = Method("get_publisher")
    publicationYear = Method("get_publication_year")  # noqa: N815
    schemaVersion = Constant("http://datacite.org/schema/kernel-4")  # noqa: N815
    subjects = Method("get_subject")
    contributors = Method("get_contributors")
    language = Method("get_language")
    dates = Method("get_dates")  # todo -> check with Alex whether dates are required
    alternateIdentifiers = Method("get_alternateIdentifiers")
    relatedIdentifiers = Method("get_relatedIdentifiers")
    rightsList = Method("get_rightsList")
    descriptions = Method("get_description")
    geoLocations = Method("get_geoLocations")
    relatedItems = Method("get_relatedItems")

    def _get_metadata(self, obj: dict) -> Marc21Metadata: 
        """Cache Marc21 metadata."""
        if self._metadata is None:
            self._metadata = Marc21Metadata(json=obj.metadata)
        return self._metadata

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
            "subfields",
            {},
        )

    def _get_affiliation(
        self,
        obj: dict,
        affl_name_subfield_number: str,
        affl_id_subfield_number: str,
    ) -> list[dict[str, str]] | missing:
        """Get affiliation (common for creators and contributors)."""
        affl_name = obj.get("subfields", {}).get(affl_name_subfield_number, [""])[0]
        affl_id = obj.get("subfields", {}).get(affl_id_subfield_number, [""])[0]

        if not affl_id:
            return missing

        parsed_url = urlparse(affl_id)
        affl_id_uri = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        affl_id_scheme = parsed_url.netloc.split(".")[
            0
        ].upper()  # todo that's not save tldextract would provide the required functionality

        return [
            {
                "name": affl_name,
                "affiliationIdentifier": affl_id,
                "affiliationIdentifierScheme": affl_id_scheme,
                "schemeUri": affl_id_uri,
            },
        ]

    def _get_nameIdentifiers(
        self,
        obj: dict,
        subfield_number: str,
    ) -> list[dict[str, str]] | missing:
        """Get name identifier (common for creators and contributors)."""
        identifiers = obj.get("subfields", {}).get(subfield_number, [""])
        nameIdentifiers: list[dict[str, str]] = []

        for id in (id for id in identifiers if id):
            parsed_url = urlparse(id)
            id_uri = f"{parsed_url.scheme}://{parsed_url.netloc}/"
            id_scheme = parsed_url.netloc.split(".")[
                0
            ].upper()  # todo that's not save tldextract would provide the required functionality
            nameIdentifier = {
                "nameIdentifier": id,
                "nameIdentifierScheme": id_scheme,
                "schemeUri": id_uri,
            }
            nameIdentifiers.append(nameIdentifier)

        return nameIdentifiers or missing

    def _get_contributorType(self, obj: dict, subfield_number: str) -> tuple[str, str]:
        """Get the type of contribution."""
        kind_of_contributor = {
            "aut": "Creator",
            "edt": "Editor",
            "other": "Other",
        }
        contributor_type = obj.get("subfields", {}).get(subfield_number, ["other"])[0]
        return contributor_type, kind_of_contributor.get(contributor_type, "Other")

    def _get_contributor_by_type(
        self,
        obj: dict,
        field_number: str,
        contribution_type: str,
        exclude: bool,
    ) -> list[dict[str, str]]:
        """Get list of get_contributors."""
        contributors: list[dict[str, str]] = []
        for entry in obj["metadata"]["fields"].get(field_number, [{"subfields": {}}]):
            contributor_name = entry.get("subfields", {}).get("a", [""])[0]
            contributor_type = self._get_contributorType(entry, "4")
            to_exclude = contribution_type and exclude == (
                contributor_type[0] == contribution_type
            )
            if not contributor_name:
                continue
            if to_exclude:
                continue
            contributor = {
                "name": contributor_name,
                "contributorType": contributor_type[1],
            }

            contributor_id = self._get_nameIdentifiers(entry, "2")
            if contributor_id:
                contributor["nameIdentifiers"] = contributor_id

            contributor_affl = self._get_affiliation(entry, "u", "1")
            if contributor_affl:
                contributor["affiliation"] = contributor_affl
            
            contributors.append(contributor)
        return contributors

    def _get_related_identifiers_by_field(
        self,
        obj: dict,
        field_number: str,
        subfield_number: str,
        id_type: str,
    ) -> list[dict[str, str]]:
        """Get related identifiers of a particular type."""
        relatedIdentifiers: list[dict[str, str]] = []
        for entry in obj["metadata"]["fields"].get(field_number, [{"subfields": {}}]):
            id = entry.get("subfields", {}).get(subfield_number, [""])[0]
            if not id:
                continue
            relatedIdentifiers.append(
                {
                    "relationType": "IsPublishedIn",
                    "relatedIdentifier": id,
                    "relatedIdentifierType": id_type,
                },
            )
        return relatedIdentifiers

    def _get_alternate_identifiers_by_field(
        self,
        obj: dict,
        field_number: str,
        subfield_number: str,
        id_type: str,
    ) -> list[dict[str, str]]:
        """Get alternate identifiers of a particular type."""
        alternateIdentifiers: list[dict[str, str]] = []
        for entry in obj["metadata"]["fields"].get(field_number, [{"subfields": {}}]):
            id = entry.get("subfields", {}).get(subfield_number, [""])[0]
            if not id:
                continue
            alternateIdentifiers.append(
                {
                    "alternateIdentifier": id,
                    "alternateIdentifierType": id_type,
                },
            )
        return alternateIdentifiers


    def get_titles(self, obj: dict) -> list[dict[str, str]] | missing:
        """Get titles."""
        titles = []
        
        title = self._get_metadata(obj).get_value("245", "1", "0", "a")
        if title:
            titles.append({"title": title})
        
        subtitle = self._get_metadata(obj).get_value("245", "1", "0", "b")
        if subtitle:
            titles.append({"title": subtitle, "titleType" : "Subtitle"})
        
        return titles or missing


    def get_creators(self, obj: dict) -> list[dict]:
        """Get creators."""
        creators = self._get_contributor_by_type(obj, "100", "", False)
        co_authors = self._get_contributor_by_type(obj, "700", "aut", False)
        return creators + co_authors

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

    def get_subject(self, obj: dict) -> list[dict[str, str]] | missing:
        """Get subjects (keywords)."""
        subjects: list[dict[str, str]] = []
        for entry in obj["metadata"]["fields"].get("653", [{"subfields": {}}]):
            subject = entry.get("subfields", {}).get("a", [""])[0]
            if subject:
                subjects.append({"subject": subject})
        return subjects or missing

    def get_contributors(self, obj: dict) -> list[dict[str, str]] | missing:
        """Get list of get_contributors."""
        return self._get_contributor_by_type(obj, "700", "aut", True) or missing

    def get_language(self, obj: dict) -> str | missing:
        """Get language."""
        language_field = self._get_subfields(obj, "041")
        language: list[str] = language_field.get("a")
        if language:
            return language[0]
        return missing

    def get_dates(self, obj: dict) -> list | missing:
        """Get list of date-dicts."""
        # todo
        return missing

    def get_alternateIdentifiers(self, obj: dict) -> list | missing:
        """Get alternate identifiers, which can be used to pass custom information to metadata."""
        # example code (wip)
        # peer_review = self._get_alternate_identifiers_by_field(obj, "500", "a", "Peer Review" )
        # return peer_review
        return missing

    def get_relatedIdentifiers(self, obj: dict) -> list | missing:
        """Get related identifiers (e.g. ISBN, ISSN, DOI)."""
        ebook_isbn = self._get_related_identifiers_by_field(obj, "020", "a", "ISBN")
        print_isbn = self._get_related_identifiers_by_field(obj, "020", "z", "ISBN")
        issn = self._get_related_identifiers_by_field(obj, "022", "a", "ISSN")
        # doi = self._get_related_identifiers_by_field(obj, "787", "o", "DOI") # todo -> align with "Zeitschriften"
        return ebook_isbn + print_isbn + issn or missing

    def get_rightsList(self, obj: dict) -> list | missing:
        """Get list of rights-dicts."""
        rights: list[dict[str, str]] = []
        for entry in obj["metadata"]["fields"].get("540", [{"subfields": {}}]):
            rights_id = entry.get("subfields", {}).get("f", [""])[0]
            rights_uri = entry.get("subfields", {}).get("u", [""])[0]
            if not (rights_id and rights_uri):
                continue
            rights.append(
                {
                    "rightsUri": rights_uri,
                    "rightsIdentifier": rights_id,
                },
            )
        return rights or missing

    def get_description(self, obj: dict) -> list[dict[str, str]] | missing:
        """Get titles list."""
        description_field = self._get_subfields(obj, "520")
        descriptions: list[str] = description_field.get("a")
        if descriptions:
            return [
                {"description": description, "descriptionType": "Abstract"}
                for description in descriptions
            ]
        return missing

    def get_geoLocations(self, obj: dict) -> list[dict[str, str]] | missing:
        """Get publication location."""
        places_field = self._get_subfields(obj, "264")
        places: list[str] = places_field.get("a")
        if places:
            return [{"geoLocationPlace": places[0]}]
        return missing

    def get_relatedItems(self, obj: dict) -> list[dict] | missing:
        """Get related items (e.g. a series the publication belongs to)."""
        relatedItems: list[dict] = []
        # series + volume
        for entry in obj["metadata"]["fields"].get("490", [{"subfields": {}}]):
            series_title = entry.get("subfields", {}).get("a", [""])[0]
            series_volume = entry.get("subfields", {}).get("v", [""])[0]
            if not (series_title and series_volume):
                continue
            relatedItems.append(
                {
                    "titles": [{"title": series_title}],
                    "volume": series_volume,
                    "relatedItemType": "Other",  # todo -> Alex: welcher Typ?
                    "relationType": "IsPublishedIn",
                },
            )
        # ISBN E-Book
        for entry in obj["metadata"]["fields"].get("020", [{"subfields": {}}]):
            isbn = entry.get("subfields", {}).get("a", [""])[0]
            type = entry.get("subfields", {}).get("q", [""])[0]
            if not (isbn and type):
                continue
            relatedItems.append(
                {
                    "relatedItemType": "Other",  # todo -> Alex: wie wird der Typ spezifiziert? Bsp. Feld "q" taucht nicht in datacite Liste auf -> hardcoded Zuordnung?
                    "relationType": "IsPublishedIn",
                    "relatedItemIdentifier": {
                        "relatedItemIdentifier": isbn,
                        "relatedItemIdentifierType": "ISBN",
                    },
                },
            )
        # ISBN Print
        for entry in obj["metadata"]["fields"].get("020", [{"subfields": {}}]):
            isbn = entry.get("subfields", {}).get("z", [""])[0]
            type = entry.get("subfields", {}).get("q", [""])[0]
            if not (isbn and type):
                continue
            relatedItems.append(
                {
                    "relatedItemType": "Book",  # todo -> Alex: wie wird der Typ spezifiziert? ...
                    "relationType": "IsPublishedIn",
                    "relatedItemIdentifier": {
                        "relatedItemIdentifier": isbn,
                        "relatedItemIdentifierType": "ISBN",
                    },
                },
            )
        # ISSN
        for entry in obj["metadata"]["fields"].get("022", [{"subfields": {}}]):
            issn = entry.get("subfields", {}).get("a", [""])[0]
            if not issn:
                continue
            relatedItems.append(
                {
                    "relatedItemType": "Other",  # todo -> Alex: wie wird der Typ spezifiziert? ....
                    "relationType": "IsPublishedIn",
                    "relatedItemIdentifier": {
                        "relatedItemIdentifier": issn,
                        "relatedItemIdentifierType": "ISSN",
                    },
                },
            )
        return relatedItems or missing
