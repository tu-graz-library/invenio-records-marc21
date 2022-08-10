# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""


from copy import deepcopy

import pytest


@pytest.fixture(scope="function")
def marc21_metadata():
    """Record UI metadata."""
    return {
        "leader": "01198nam a2200397 c 4500",
        "fields": {
            "001": "990004519310204517",
            "005": "20220511091822.0",
            "007": "tu",
            "008": "201022|2022 ||| m ||| | eng c",
            "009": "AC11056824",
            "100": [
                {
                    "ind1": "_",
                    "ind2": "_",
                    "subfields": {
                        "a": ["Philipp"],
                    },
                }
            ],
            "245": [
                {
                    "ind1": "1",
                    "ind2": "0",
                    "subfields": {
                        "a": ["<<The>> development of high strain actuator materials"],
                        "c": ["Denis Sch\u00fctz"],
                    },
                }
            ],
            "260": [
                {
                    "ind1": "3",
                    "ind2": "0",
                    "subfields": {
                        "b": ["TU Graz"],
                    },
                }
            ],
            "362": [
                {
                    "ind1": "0",
                    "ind2": "_",
                    "subfields": {
                        "a": ["2022"],
                    },
                }
            ],
            "502": [
                {
                    "ind1": "_",
                    "ind2": "_",
                    "subfields": {
                        "a": ["Graz, Techn. Univ., Diss., 2012"],
                    },
                }
            ],
        },
    }


@pytest.fixture(scope="function")
def expect_metadata_ui_xml():
    """Record UI xml metadata."""
    return (
        '<record><leader>01198nam a2200397 c 4500</leader><controlfield tag="001">990004519310204517</controlfield>'
        '<controlfield tag="005">20220511091822.0</controlfield><controlfield tag="007">tu</controlfield><controlfield tag="008">201022|2022 ||| m ||| | eng c</controlfield><controlfield tag="009">'
        'AC11056824</controlfield><datafield tag="100" ind1=" " ind2=" "><subfield code="a">Philipp</subfield></datafield>'
        '<datafield tag="245" ind1="1" ind2="0"><subfield code="a">&lt;&lt;The&gt;&gt; development of high strain actuator materials'
        '</subfield><subfield code="c">Denis Schütz</subfield></datafield><datafield tag="260" ind1="3" ind2="0"><subfield code="b">TU Graz'
        '</subfield></datafield><datafield tag="362" ind1="0" ind2=" "><subfield code="a">2022'
        '</subfield></datafield><datafield tag="502" ind1=" " ind2=" "><subfield code="a">Graz, Techn. Univ., Diss., 2012</subfield>'
        "</datafield></record>"
    )


@pytest.fixture(scope="function")
def expect_metadata_ui():
    """Record UI metadata."""
    return {
        "main_entry_personal_name": {"personal_name": "Philipp", "relator_code": ""},
        "title_statement": {
            "title": "<<The>> development of high strain actuator materials"
        },
        "physical_description": {"extent": ""},
        "dissertation_note": {"dissertation_note": "Graz, Techn. Univ., Diss., 2012"},
        "general_note": {"general_note": ""},
        "production_publication_distribution_manufacture_and_copyright_notice": {
            "date_of_production_publication_distribution_manufacture_or_copyright_notice": ""
        },
        "language_code": {"language_code_of_text_sound_track_or_separate_title": ""},
    }


@pytest.fixture(scope="function")
def full_record(marc21_record, marc21_metadata):
    """Full record as is expected by the UI serializer."""
    marc21_record
    marc21_record["id"] = "9jkx5-hx115"
    marc21_record["pid"] = {
        "pk": 58,
        "status": "R",
        "obj_type": "rec",
        "pid_type": "marcid",
    }
    marc21_record["pids"] = {
        "doi": {
            "identifier": "10.5281/inveniordm.1234",
            "provider": "datacite",
            "client": "inveniordm",
        },
    }
    marc21_record["files"] = {"enabled": True}
    marc21_record["access"] = {
        "files": "restricted",
        "embargo": {"until": None, "active": False, "reason": None},
        "metadata": "restricted",
        "status": "restricted",
    }
    marc21_record["metadata"] = marc21_metadata
    marc21_record["versions"] = {"index": 1, "is_latest": True, "is_latest_draft": True}

    return marc21_record


@pytest.fixture(scope="function")
def list_records(full_record):
    """Fixture list of records."""
    list_records = {
        "hits": {"hits": [deepcopy(full_record), deepcopy(full_record)]},
    }
    return list_records
