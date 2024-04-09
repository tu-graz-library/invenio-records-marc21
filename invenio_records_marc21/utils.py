# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023-2024 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 utils module."""

import random
from random import randint

from faker import Faker

from .records.fields.resourcetype import ResourceTypeEnum


def fake_resource_type():
    """Create fake record resource type."""
    samples = []
    for resource in ResourceTypeEnum:
        samples.append(resource.value)
    random_resource = random.choice(samples)
    return random_resource


def create_fake_data():
    """Create records for demo purposes."""
    fake = Faker()

    mmsid = randint(9000000000000, 9999999999999)
    ac_number = randint(13000000, 19999999)
    local_id = randint(70000, 99999)
    ac_id = f"AC{ac_number}"
    last_name = fake.last_name()
    first_name = fake.first_name()
    person_title = fake.suffix_nonbinary()
    create_date = fake.date_time_this_decade()
    country_code = fake.country_code()

    data_to_use = {
        "files": {
            "enabled": False,
        },
        "pids": {},
        "metadata": {
            "leader": "00000nam a2200000zca4501",
            "fields": {
                "001": f"{mmsid}",
                "005": "FAKE0826022415.0",
                "007": "cr#|||||||||||",
                "008": f"230501s{create_date.strftime('%Y')}    |||     om    ||| | eng c",
                "009": f"{ac_id}",
                "035": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": [f"({country_code}-OBV){ac_id}"]},
                    },
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": [f"({country_code}-599)OBV{ac_id}"]},
                    },
                ],
                "040": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "a": [f"{country_code}-UB"],
                            "b": ["eng"],
                            "d": [f"{country_code}-UB"],
                            "e": ["rda"],
                        },
                    }
                ],
                "041": [{"ind1": "_", "ind2": "_", "subfields": {"a": ["eng"]}}],
                "100": [
                    {
                        "ind1": "1",
                        "ind2": "_",
                        "subfields": {
                            "4": [country_code],
                            "a": [f"{first_name}, {last_name}"],
                        },
                    }
                ],
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {
                            "a": [f"{fake.company()}"],
                            "c": [f"{person_title} {first_name}, {last_name}"],
                        },
                    }
                ],
                "246": [
                    {
                        "ind1": "1",
                        "ind2": "_",
                        "subfields": {
                            "a": [f"{fake.catch_phrase()}"],
                            "i": [country_code],
                        },
                    }
                ],
                "264": [
                    {
                        "ind1": "_",
                        "ind2": "1",
                        "subfields": {
                            "a": [f"{fake.city()}"],
                            "c": [f"{create_date.strftime('%B %Y')}"],
                        },
                    }
                ],
                "300": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "a": [fake.text(max_nb_chars=2000)],
                            "b": [fake.text(max_nb_chars=100)],
                        },
                    }
                ],
                "336": [{"ind1": "_", "ind2": "_", "subfields": {"b": ["txt"]}}],
                "337": [{"ind1": "_", "ind2": "_", "subfields": {"b": ["c"]}}],
                "338": [{"ind1": "_", "ind2": "_", "subfields": {"b": ["cr"]}}],
                "347": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": ["Textdatei"]},
                    }
                ],
                "502": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "c": [fake.company()],
                            "d": [f"{create_date.strftime('%Y')}"],
                        },
                    },
                ],
                "506": [
                    {
                        "ind1": "0",
                        "ind2": "_",
                        "subfields": {
                            "2": ["star"],
                            "f": ["Unrestricted online access"],
                        },
                    }
                ],
                "520": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": [fake.text(max_nb_chars=100)]},
                    },
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": [fake.text(max_nb_chars=100)]},
                    },
                ],
                "655": [
                    {
                        "ind1": "_",
                        "ind2": "7",
                        "subfields": {
                            "0": [f"({country_code}-552){fake.ssn()}"],
                            "2": ["gnd-content"],
                            "a": ["Hochschulschrift"],
                        },
                    }
                ],
                "970": [
                    {
                        "ind1": "2",
                        "ind2": "_",
                        "subfields": {"d": [f"{fake_resource_type()}"]},
                    }
                ],
                "995": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "9": ["local"],
                            "a": [f"{local_id}"],
                            "i": ["FAKEInstitution"],
                        },
                    }
                ],
            },
        },
    }

    return data_to_use


def build_record_unique_id(doc):
    """Build record unique identifier."""
    doc["unique_id"] = "{0}_{1}".format(doc["recid"], doc["parent_recid"])
    return doc
