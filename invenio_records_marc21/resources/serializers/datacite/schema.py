# SPDX-FileCopyrightText: 2021 CERN.
# SPDX-FileCopyrightText: 2021 Northwestern University.
# SPDX-FileCopyrightText: 2022-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""DataCite based Schema for Invenio RDM Records."""

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, Concatenate, overload

from flask import current_app
from marshmallow import Schema, missing
from marshmallow.fields import Constant, Field, Method
from marshmallow.utils import _Missing

from invenio_records_marc21.services.record import Marc21Metadata


@overload
def metadata[SelfT, **P, T](
    f: Callable[Concatenate[SelfT, Marc21Metadata, P], T],
) -> Callable[Concatenate[SelfT, dict, P], T]:
    """Metadata-decorator for the "get_..."-methods inside Marc21DataCite43Schema."""


@overload
def metadata[SelfT, A, **P, T](
    f: Callable[Concatenate[SelfT, A, Marc21Metadata, P], T],
) -> Callable[Concatenate[SelfT, A, dict, P], T]:
    """Metadata-decorator for the "serialize"-methods inside CreatorField and ContributorField."""


def metadata(f: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to fetch metadata as Marc21Metadata."""
    signature = inspect.signature(f)

    @wraps(f)
    def inner(*args: Any, **kwargs: Any) -> Any:
        bound = signature.bind(*args, **kwargs)

        obj = bound.arguments["obj"]
        bound.arguments["obj"] = Marc21Metadata(json=obj["metadata"])

        return f(*bound.args, **bound.kwargs)

    return inner


def get_scheme_datacite(
    scheme: dict,
    config_name: str,
    default: str | None = None,
) -> str:
    """Returns the datacite equivalent of a scheme."""
    config_item = current_app.config[config_name]
    return config_item.get(scheme, {}).get("datacite", default)


class PersonSchema43(Schema):
    """Creator/contributor schema for v4.3."""

    name = Method("get_name")
    nameIdentifiers = Method("get_name_identifier_orcid")  # noqa: N815
    affiliation = Method("get_affiliation_ror")
    contributorType = Method("get_contribution_type")  # noqa: N815

    def get_name(self, obj: dict) -> str | _Missing:
        """Get a persons name."""
        return obj.get("subfields", {}).get("a", [""])[0] or "N/A"

    def get_name_identifier_orcid(self, obj: dict) -> list[dict] | _Missing:
        """Assemble name identifier dict for ORCID."""
        if contributor_id := obj.get("subfields", {}).get("2", [""])[0]:
            return [
                {
                    "nameIdentifier": f"https://orcid.org/{contributor_id}",
                    "nameIdentifierScheme": "ORCID",
                    "schemeUri": "https://orcid.org/",
                },
            ]
        return missing

    def get_affiliation_ror(self, obj: dict) -> list[dict] | _Missing:
        """Assemble affiliation dict for ROR."""
        affiliation = {}

        contributor_affl = obj.get("subfields", {}).get("u", [""])[0]
        contributor_affl_id = obj.get("subfields", {}).get("1", [""])[0]

        if contributor_affl:
            affiliation["name"] = contributor_affl
        if contributor_affl_id:
            affiliation["affiliationIdentifier"] = (
                f"https://ror.org/{contributor_affl_id}"
            )
            affiliation["affiliationIdentifierScheme"] = "ROR"
            affiliation["schemeUri"] = "https://ror.org/"

        return [affiliation] if affiliation else missing

    def get_contribution_type(self, obj: dict) -> str:
        """Get contribution type."""
        kind_of_contribution = {
            "aut": "Creator",
            "edt": "Editor",
            "other": "Other",
        }

        contribution_type = obj.get("subfields", {}).get("4", [""])[0] or "other"

        return kind_of_contribution.get(contribution_type, "Other")


def load_persons_from_marc21(
    obj: Marc21Metadata,
    field_number: str,
    default_contribution: str | None = None,
    include_contribution: str | None = None,
    exclude_contribution: str | None = None,
    consider_contribution: int | None = None,
) -> list[dict]:
    """Load persons from a marc21 field considering include_/exclude_contributions."""
    loaded_persons = []

    person_fields = obj.get_fields(*field_number.split("."))

    for person in person_fields[1]:

        base_person = person.to_obj()

        contributions = [
            v.strip() for v in (person.get("4") or default_contribution or "").split()
        ]

        if consider_contribution is not None:
            contributions = [contributions[consider_contribution]]

        for contribution in contributions:

            if include_contribution and contribution != include_contribution:
                continue

            if exclude_contribution and contribution == exclude_contribution:
                continue

            base_person["subfields"]["4"] = [contribution]
            loaded_persons.append(base_person)

    return loaded_persons


class CreatorField(Field):
    """Class to extract creators from metadata."""

    @metadata
    def serialize(
        self,
        attr: str,
        obj: Marc21Metadata,
        accessor: Callable[[Any, str, Any], Any] | None,
        **kwargs,
    ) -> list:
        """Generate a list of creators."""
        creators_marc21 = load_persons_from_marc21(
            obj=obj,
            field_number="100.1.",
            default_contribution="aut",
            consider_contribution=0,  # avoid duplicates
        ) + load_persons_from_marc21(
            obj=obj,
            field_number="700.1.",
            include_contribution="aut",
        )

        # creator is mandatory: add dummy entry if creators_marc21 is empty
        if not creators_marc21:
            creators_marc21 = [{"ind1": "1", "ind2": "_", "subfields": {"a": ["N/A"]}}]

        creators = [
            PersonSchema43(exclude=("contributorType",)).dump(p)
            for p in creators_marc21
        ]

        return creators


class ContributorField(Field):
    """Class to extract contributors from metadata."""

    @metadata
    def serialize(
        self,
        attr: str,
        obj: Marc21Metadata,
        accessor: Callable[[Any, str, Any], Any] | None,
        **kwargs,
    ) -> list | _Missing:
        """Generate a list of contributors."""
        contributors_marc21 = load_persons_from_marc21(
            obj=obj,
            field_number="100.1.",
            include_contribution="edt",
        ) + load_persons_from_marc21(
            obj=obj,
            field_number="700.1.",
            default_contribution="other",
            exclude_contribution="aut",
        )

        contributors = [PersonSchema43().dump(p) for p in contributors_marc21]

        return contributors or missing


class Marc21DataCite43Schema(Schema):
    """DataCite JSON 4.3 Marshmallow Schema."""

    types = Method("get_type")
    titles = Method("get_titles")
    creators = CreatorField()
    publisher = Method("get_publisher")
    publicationYear = Method("get_publication_year")  # noqa: N815
    schemaVersion = Constant("http://datacite.org/schema/kernel-4")  # noqa: N815
    subjects = Method("get_subject")
    contributors = ContributorField()
    language = Method("get_language")
    dates = Method("get_dates")
    alternateIdentifiers = Method("get_alternate_identifiers")  # noqa: N815
    relatedIdentifiers = Method("get_related_identifiers")  # noqa: N815
    rightsList = Method("get_rights_list")  # noqa: N815
    descriptions = Method("get_description")
    geoLocations = Method("get_geo_locations")  # noqa: N815
    relatedItems = Method("get_related_items")  # noqa: N815

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

    @metadata
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

    @metadata
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

    @metadata
    def get_publisher(self, obj: Marc21Metadata) -> str:
        """Get publisher."""
        publisher_260 = obj.get_value(category="260", subf_code="b")
        if publisher_260:
            return publisher_260

        publisher_264 = obj.get_value(category="264", subf_code="b")
        if publisher_264:
            return publisher_264

        return current_app.config.get("MARC21_DATACITE_DEFAULT_PUBLISHER") or "N/A"

    @metadata
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

    @metadata
    def get_subject(self, obj: Marc21Metadata) -> list[dict[str, str]] | _Missing:
        """Get subjects (keywords)."""
        return [
            {"subject": subject}
            for subject in obj.get_values(category="653", subf_code="a")
        ] or missing

    @metadata
    def get_language(self, obj: Marc21Metadata) -> str | _Missing:
        """Get language."""
        return obj.get_value(category="041", subf_code="a") or missing

    @metadata
    def get_dates(self, obj: Marc21Metadata) -> list | _Missing:
        """Get list of date-dicts."""
        # not implemented yet
        return missing

    def get_alternate_identifiers(
        self,
        obj: dict,
    ) -> list[dict[str, str]] | _Missing:
        """Get alternate identifiers."""
        # pids
        pids = []
        for scheme, id_ in obj["pids"].items():
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

        # further identifiers from metadata
        metadata = Marc21Metadata(json=obj["metadata"])

        ebook_isbn = self._get_alternate_identifiers_by_field(
            metadata,
            field_number="020...a",
            id_type="ISBN",
        )
        print_isbn = self._get_alternate_identifiers_by_field(
            metadata,
            field_number="020...z",
            id_type="ISBN",
        )
        issn = self._get_alternate_identifiers_by_field(
            metadata,
            field_number="022...a",
            id_type="ISSN",
        )
        doi = self._get_alternate_identifiers_by_field(
            metadata,
            field_number="856.4.0.u",
            id_type="DOI",
        )

        return pids + ebook_isbn + print_isbn + issn + doi or missing

    @metadata
    def get_related_identifiers(
        self,
        obj: Marc21Metadata,
    ) -> list[dict[str, str]] | _Missing:
        """Get related identifiers."""
        # not implemented yet
        # make use of self._get_related_identifiers_by_field
        return missing

    @metadata
    def get_rights_list(self, obj: Marc21Metadata) -> list[dict[str, str]] | _Missing:
        """Get list of rights-dicts."""
        return [
            {
                "rightsUri": entry.get("u"),
                "rightsIdentifier": entry.get("f"),
            }
            for entry in obj.get_fields(category="540")[1]
        ] or missing

    @metadata
    def get_description(self, obj: Marc21Metadata) -> list[dict[str, str]] | _Missing:
        """Get description."""
        return (
            [{"description": description, "descriptionType": "Abstract"}]
            if (description := obj.get_value(category="520", subf_code="a"))
            else missing
        )

    @metadata
    def get_geo_locations(self, obj: Marc21Metadata) -> list[dict[str, str]] | _Missing:
        """Get publication location."""
        return (
            [{"geoLocationPlace": place}]
            if (place := obj.get_value(category="264", subf_code="a"))
            else missing
        )

    def get_related_items(self, obj: dict) -> list[dict] | _Missing:
        """Get related items (e.g. a series the publication belongs to)."""
        metadata = Marc21Metadata(json=obj["metadata"])

        related_items = []

        # series + volume
        series_title = metadata.get_value(
            category="490",
            ind1="0",
            ind2="",
            subf_code="a",
        )
        series_volume = metadata.get_value(
            category="490",
            ind1="0",
            ind2="",
            subf_code="v",
        )
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
        proceedings_title = metadata.get_value(
            category="773",
            ind1="0",
            ind2="8",
            subf_code="t",
        )
        proceedings_isbn = metadata.get_value(
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
