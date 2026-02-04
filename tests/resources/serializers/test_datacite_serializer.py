# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resources serializers tests."""

from invenio_records_marc21.resources.serializers import Marc21DataCite43JSONSerializer


def test_datacite43_serializer(app, full_record):
    """Test serializer to DataCite 4.3 JSON"""
    expected_data = {
        "schemaVersion": "http://datacite.org/schema/kernel-4",
        "publicationYear": "2022",
        "identifiers": [
            {"identifier": "10.5281/inveniordm.1234", "identifierType": "DOI"}
        ],
        "titles": [{"title": "<<The>> development of high strain actuator materials"}],
        "creators": {"name": "Philipp"},
        "publisher": "TU Graz",
        "types": {"resourceTypeGeneral": "Other", "resourceType": "Text"},
    }

    with app.app_context():
        serializer = Marc21DataCite43JSONSerializer()
        serialized_record = serializer.dump_obj(full_record)

    assert serialized_record == expected_data
