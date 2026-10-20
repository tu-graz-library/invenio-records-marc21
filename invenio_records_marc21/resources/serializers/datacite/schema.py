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
from marshmallow import Schema, missing, pre_dump
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

    _pids = None

    types = Method("get_type")
    titles = Method("get_titles")
    creators = Method("get_creators")
    publisher = Method("get_publisher")
    publicationYear = Method("get_publication_year")  # noqa: N815
    schemaVersion = Constant("http://datacite.org/schema/kernel-4")  # noqa: N815
    subjects = Method("get_subject")
    contributors = Method("get_contributors")
    language = Method("get_language")
    dates = Method("get_dates")
    alternateIdentifiers = Method("get_alternate_identifiers")  # noqa: N815
    relatedIdentifiers = Method("get_related_identifiers")  # noqa: N815
    rightsList = Method("get_rights_list")  # noqa: N815
    descriptions = Method("get_description")
    geoLocations = Method("get_geo_locations")  # noqa: N815
    relatedItems = Method("get_related_items")  # noqa: N815

    @pre_dump
    def _pre_format_metadata(
        self,
        obj: dict,
        *,
        many: bool,
        **_kwargs: object,
    ) -> Marc21Metadata:
        self._pids = obj.get("pids", {})
        return Marc21Metadata(json=obj["metadata"])

    def _get_contributor_by_type(
        self,
        obj: Marc21Metadata,
        field_number: str,
        allowed_contribution_types: list[str],
    ) -> list[dict[str, str | list]]:
        """Get list of get_contributors."""
        kind_of_contributor = {
            "aut": "Creator",
            "edt": "Editor",
            "other": "Other",
        }

        contributors: list[dict[str, str | list[dict[str, str]]]] = []

        contributor_fields = obj.get_fields(*field_number.split("."))
        for entry in contributor_fields[1]:
            contributor_name = entry.get("a")
            contributor_type = entry.get("4") or "empty"

            if not contributor_name:
                continue

            if contributor_type and contributor_type not in allowed_contribution_types:
                continue

            contributor = {
                "name": contributor_name,
                "contributorType": kind_of_contributor.get(contributor_type, "Other"),
            }

            # ORCID
            contributor_id = entry.get("2")
            if contributor_id:
                contributor["nameIdentifiers"] = [
                    {
                        "nameIdentifier": f"https://orcid.org/{contributor_id}",
                        "nameIdentifierScheme": "ORCID",
                        "schemeUri": "https://orcid.org/",
                    },
                ]

            # ROR
            affiliation = {}

            contributor_affl = entry.get("u")
            contributor_affl_id = entry.get("1")

            if contributor_affl:
                affiliation["name"] = contributor_affl
            if contributor_affl_id:
                affiliation["affiliationIdentifier"] = (
                    f"https://ror.org/{contributor_affl_id}"
                )
                affiliation["affiliationIdentifierScheme"] = "ROR"
                affiliation["schemeUri"] = "https://ror.org/"
            if affiliation:
                contributor["affiliation"] = [affiliation]

            contributors.append(contributor)
        return contributors

    def _get_related_identifiers_by_field(
        self,
        obj: Marc21Metadata,
        field_number: str,
        id_type: str,
    ) -> list[dict[str, str]]:
        """Get related identifiers of a particular type."""
        return [
            {
                "relationType": "IsPublishedIn",
                "relatedIdentifier": identifier,
                "relatedIdentifierType": id_type,
            }
            for identifier in obj.get_values(*field_number.split("."))
        ]

    def _get_alternate_identifiers_by_field(
        self,
        obj: Marc21Metadata,
        field_number: str,
        id_type: str,
    ) -> list[dict[str, str]]:
        """Get alternate identifiers of a particular type."""
        return [
            {
                "alternateIdentifier": identifier,
                "alternateIdentifierType": id_type,
            }
            for identifier in obj.get_values(*field_number.split("."))
        ]

    def get_type(self, obj: Marc21Metadata) -> dict[str, str]:
        """Get resource type."""
        map_970d_to_datacite = {
            # from https://wiki.obvsg.at/Katalogisierungshandbuch/Kategorienuebersicht970FE
            # to https://datacite-metadata-schema.readthedocs.io/en/4.7/properties/resourcetype/#a-resourcetypegeneral
            "HS-BACHELOR": "Other",  # (Restliche Hochschulgschriften)
            "HS-DIPL": "Other",  # (Diplomarbeiten (vor Bologna))
            "HS-DISS": "Dissertation",  # (Doktoratsstudien)
            "HS-HABIL": "Other",  # (Habil.-Schriften)
            "HS-MASTER": "Other",  # (Master-Arbeiten (nach Bologna))
            "NAK": "Other",  # (Nachlasskatalogisierung)
            "OA-ARTICLE": "JournalArticle",  # (Aufsatz in einer Zeitschrift)
            "OA-BOOKPART": "BookChapter",  # (Aufsatz in einem Sammelwerk)
            "OA-MONOGRAPH": "Book",  # (Buch)
            # from TU Graz Verlag
            "Monografie": "Book",
            "Konferenzbeitrag": "ConferencePaper",
            "Masterthesis": "Other",
            "Dissertation": "Dissertation",
        }

        type_007 = obj.get_value(category="007")
        type_970 = obj.get_value(category="970", ind1="2", ind2="", subf_code="d")

        if type_970:
            return {
                "resourceTypeGeneral": (map_970d_to_datacite.get(type_970, "Other")),
                "resourceType": "Text",
            }
        if type_007 and type_007 == "cr#|||||||||||":
            return {
                "resourceTypeGeneral": "Book",
                "resourceType": "Text",
            }
        return {
            "resourceTypeGeneral": "Other",
            "resourceType": "Text",
        }

    def get_titles(self, obj: Marc21Metadata) -> list[dict[str, str]]:
        """Get titles."""
        titles: list[dict[str, str]] = []

        field_numbers = ["245.1.0", "245.0.0"]

        for field in field_numbers:

            title = obj.get_value(*field.split("."), subf_code="a")
            if title:
                titles.append({"title": title})

            subtitle = obj.get_value(*field.split("."), subf_code="b")
            if subtitle:
                titles.append({"title": subtitle, "titleType": "Subtitle"})

            if titles:
                return titles

        return [{"title": "N/A"}]

    def get_creators(self, obj: Marc21Metadata) -> list[dict]:
        """Get creators."""
        creators = self._get_contributor_by_type(
            obj,
            field_number="100.1.",
            allowed_contribution_types=["aut", "empty"],
        ) + self._get_contributor_by_type(
            obj,
            field_number="700.1.",
            allowed_contribution_types=["aut"],
        )

        # keep it lean: creators do not expect contributorType
        for creator in creators:
            creator.pop("contributorType", None)

        return creators or [{"name": "N/A"}]

    def get_publisher(self, obj: Marc21Metadata) -> str:
        """Get publisher."""
        publisher_260 = obj.get_value(category="260", subf_code="b")
        if publisher_260:
            return publisher_260

        publisher_264 = obj.get_value(category="264", subf_code="b")
        if publisher_264:
            return publisher_264

        return current_app.config.get("MARC21_DATACITE_DEFAULT_PUBLISHER") or "N/A"

    def get_publication_year(self, obj: Marc21Metadata) -> str:
        """Get publication year from edtf date."""
        publication_dates = obj.get_value(category="008")
        publication_year: str = publication_dates[7:11] if publication_dates else ""
        if len(publication_year) == 4 and publication_year.isdigit():
            return publication_year

        # Production, Publication, Distribution, Manufacture, and Copyright Notice
        ppdmcn = obj.get_value(category="264", ind1="", ind2="1", subf_code="c")
        if ppdmcn:
            return ppdmcn

        return "N/A"

    def get_subject(self, obj: Marc21Metadata) -> list[dict[str, str]] | missing:
        """Get subjects (keywords)."""
        return [
            {"subject": subject}
            for subject in obj.get_values(category="653", subf_code="a")
        ] or missing

    def get_contributors(self, obj: Marc21Metadata) -> list[dict[str, str]] | missing:
        """Get list of get_contributors."""
        return (
            self._get_contributor_by_type(
                obj,
                field_number="700.1.",
                allowed_contribution_types=["edt", "empty"],
            )
            or missing
        )

    def get_language(self, obj: Marc21Metadata) -> str | missing:
        """Get language."""
        return obj.get_value(category="041", subf_code="a") or missing

    def get_dates(self, _obj: Marc21Metadata) -> list | missing:
        """Get list of date-dicts."""
        # not implemented yet
        return missing

    def get_alternate_identifiers(
        self,
        obj: Marc21Metadata,
    ) -> list[dict[str, str]] | missing:
        """Get alternate identifiers."""
        # pids
        pids = []
        for scheme, id_ in self._pids.items():
            id_scheme = get_scheme_datacite(
                scheme,
                "MARC21_IDENTIFIERS_SCHEMES",
                default=scheme,
            )

            if id_scheme:
                pids.append(
                    {
                        "alternateIdentifier": id_["identifier"],
                        "alternateIdentifierType": id_scheme,
                    },
                )

        # further identifiers
        ebook_isbn = self._get_alternate_identifiers_by_field(
            obj,
            field_number="020...a",
            id_type="ISBN",
        )
        print_isbn = self._get_alternate_identifiers_by_field(
            obj,
            field_number="020...z",
            id_type="ISBN",
        )
        issn = self._get_alternate_identifiers_by_field(
            obj,
            field_number="022...a",
            id_type="ISSN",
        )
        doi = self._get_alternate_identifiers_by_field(
            obj,
            field_number="856.4.0.u",
            id_type="DOI",
        )

        return pids + ebook_isbn + print_isbn + issn + doi or missing

    def get_related_identifiers(
        self,
        _obj: Marc21Metadata,
    ) -> list[dict[str, str]] | missing:
        """Get related identifiers."""
        # not implemented yet
        # make use of self._get_related_identifiers_by_field
        return missing

    def get_rights_list(self, obj: Marc21Metadata) -> list[dict[str, str]] | missing:
        """Get list of rights-dicts."""
        return [
            {
                "rightsUri": entry.get("u"),
                "rightsIdentifier": entry.get("f"),
            }
            for entry in obj.get_fields(category="540")[1]
        ] or missing

    def get_description(self, obj: Marc21Metadata) -> list[dict[str, str]] | missing:
        """Get description."""
        return (
            [{"description": description, "descriptionType": "Abstract"}]
            if (description := obj.get_value(category="520", subf_code="a"))
            else missing
        )

    def get_geo_locations(self, obj: Marc21Metadata) -> list[dict[str, str]] | missing:
        """Get publication location."""
        return (
            [{"geoLocationPlace": place}]
            if (place := obj.get_value(category="264", subf_code="a"))
            else missing
        )

    def get_related_items(self, obj: Marc21Metadata) -> list[dict] | missing:
        """Get related items (e.g. a series the publication belongs to)."""
        related_items = []

        # series + volume
        series_title = obj.get_value(category="490", ind1="0", ind2="", subf_code="a")
        series_volume = obj.get_value(category="490", ind1="0", ind2="", subf_code="v")
        if series_title and series_volume:
            related_items.append(
                {
                    "titles": [{"title": series_title}],
                    "volume": series_volume,
                    "relatedItemType": self.get_type(obj)["resourceTypeGeneral"],
                    "relationType": "IsPublishedIn",
                },
            )

        # proceedings
        proceedings_title = obj.get_value(
            category="773",
            ind1="0",
            ind2="8",
            subf_code="t",
        )
        proceedings_isbn = obj.get_value(
            category="773",
            ind1="0",
            ind2="8",
            subf_code="z",
        )
        if proceedings_title and proceedings_isbn:
            related_items.append(
                {
                    "titles": [{"title": proceedings_title}],
                    "relatedItemType": "ConferenceProceeding",
                    "relationType": "IsPublishedIn",
                },
            )

        return related_items or missing
