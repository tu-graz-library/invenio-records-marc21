# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2026 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resources datacite serializer tests."""

from json import load
from pathlib import Path

import decorator
import pytest

from invenio_records_marc21.resources.serializers import Marc21DataCite43JSONSerializer


def load_as_json(func: callable) -> any:
    """Decorate to load content of file as dictionary from a json file."""

    def wrapper(*args: dict, **__: dict) -> any:
        parent = Path(__file__).parent
        with Path(f"{parent}/data/{args[2]}.json").open() as fp:
            test = load(fp)
        with Path(f"{parent}/data/{args[3]}.json").open() as fp:
            expected = load(fp)
        return func(args[1], test, expected)

    return decorator.decorator(wrapper, func)


@pytest.mark.parametrize(
    ("test", "expected"),
    [
        ("primer_test", "primer_expected"),
        ("publ_ebook_test", "publ_ebook_expected"),
        ("publ_ebook2_test", "publ_ebook2_expected"),
        ("publ_article_test", "publ_article_expected"),
        ("record_w_issues_test", "record_w_issues_expected"),
    ],
)
@load_as_json
def test_datacite43_serializer(app, test, expected):
    """Test serializer to DataCite 4.3 JSON."""
    with app.app_context():
        serializer = Marc21DataCite43JSONSerializer()
        serialized_record = serializer.dump_obj(test)

    assert serialized_record == expected
