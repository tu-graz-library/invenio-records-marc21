# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Dublin Core Schema."""

from flask_resources.serializers import BaseSerializerSchema
from marshmallow import fields

from invenio_records_marc21.services.record import Marc21Metadata


class DublinCoreSchema(BaseSerializerSchema):
    """RDMRecordsSerializer."""

    contributors = fields.Method("get_contributors")
    titles = fields.Method("get_titles")
    creators = fields.Method("get_creators")
    identifiers = fields.Method("get_identifiers")
    relations = fields.Method("get_relations")
    rights = fields.Method("get_rights")
    dates = fields.Method("get_dates")
    subjects = fields.Method("get_subjects")
    descriptions = fields.Method("get_descriptions")
    publishers = fields.Method("get_publishers")
    types = fields.Method("get_types")
    sources = fields.Method("get_sources")
    languages = fields.Method("get_languages")
    locations = fields.Method("get_locations")
    formats = fields.Method("get_formats")

    def _extract(self, selectors: list[str], marc21: Marc21Metadata) -> list[str]:
        """Extract."""
        ret = []
        for selector in selectors:
            ret += marc21.get_values(*selector.split("."))
        return ret

    def get_contributors(self, marc21: Marc21Metadata) -> list:
        """Get contributors."""
        # 100, 110, 111, 700, 710, 711, 720
        selectors = ["100", "110", "111", "700", "710", "711", "720"]
        return self._extract(selectors, marc21)

    def get_titles(self, marc21: Marc21Metadata) -> list:
        """Get titles."""
        # 245, 246
        selectors = ["245", "246"]
        return self._extract(selectors, marc21)

    def get_creators(self, marc21: Marc21Metadata) -> list:
        """Get creators."""
        return []

    def get_identifiers(self, marc21: Marc21Metadata) -> list:
        """Get identifiers."""
        # 020$a, 022$a, 024$a, 856$u
        selectors = ["020...a", "022...a", "024...a", "856...u"]
        return self._extract(selectors, marc21)

    def get_relations(self, marc21: Marc21Metadata) -> list:
        """Get relations."""
        # 530, 760-787$o$t
        selectors = ["530"]
        selectors += [f"{category}...o" for category in range(760, 788)]
        return self._extract(selectors, marc21)

    def get_rights(self, marc21: Marc21Metadata) -> list:
        """Get rights."""
        # 506, 540
        selectors = ["506", "540"]
        return self._extract(selectors, marc21)

    def get_dates(self, marc21: Marc21Metadata) -> list:
        """Get dates."""
        # 008/07-10, 260$c$g
        selectors = ["260...c", "260...g"]
        dates = self._extract(selectors, marc21)
        dates += [marc21.get_value("008")[7:11]]
        return dates

    def get_subjects(self, marc21: Marc21Metadata) -> list:
        """Get subjects."""
        # 050, 060, 080, 082, 600, 610, 611, 630, 650, 653
        selectors = [
            "050",
            "060",
            "080",
            "082",
            "600",
            "610",
            "611",
            "630",
            "650",
            "653",
        ]
        return self._extract(selectors, marc21)

    def get_descriptions(self, marc21: Marc21Metadata) -> list:
        """Get descriptions."""
        # 500-599, except 506,530,540,546
        selectors = [str(i) for i in range(500, 600) if i not in [506, 530, 540, 546]]
        return self._extract(selectors, marc21)

    def get_publishers(self, marc21: Marc21Metadata) -> list:
        """Get publishers."""
        # 546, 260$a$b
        selectors = ["546", "260...a", "260...b"]
        return self._extract(selectors, marc21)

    def get_types(self, marc21: Marc21Metadata) -> list:
        """Get types."""
        # leader06, leader07, 655
        selectors = ["655"]
        types = self._extract(selectors, marc21)
        types += marc21.get_values("LDR")[6:8]
        return types

    def get_sources(self, marc21: Marc21Metadata) -> list:
        """Get soruces."""
        # 534$t, 786$o$t
        selectors = ["534...t", "786...o", "786...t"]
        return self._extract(selectors, marc21)

    def get_languages(self, marc21: Marc21Metadata) -> list:
        """Get languages."""
        # 008/35-37, 041$a$b$d$e$f$g$h$j
        selectors = [
            "041...a",
            "041...b",
            "041...d",
            "041...e",
            "041...e",
            "041...f",
            "041...g",
            "041...h",
            "041...i",
        ]
        languages = self._extract(selectors, marc21)
        languages += [marc21.get_value("008")[35:38]]
        return languages

    def get_locations(self, marc21: Marc21Metadata) -> list:
        """Get locations."""
        return []

    def get_formats(self, marc21: Marc21Metadata) -> list:
        """Get formats."""
        # 340, 856$q
        selectors = ["340", "856...q"]
        return self._extract(selectors, marc21)
