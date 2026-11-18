# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Resources datacite serializer tests."""

from datetime import UTC, datetime
from json import load, loads
from pathlib import Path

import decorator
import pytest
from jinja2 import Environment, FileSystemLoader

from invenio_records_marc21.records.api import Marc21Record
from invenio_records_marc21.resources.serializers import Marc21DataCite43JSONSerializer


def load_as_json(func: callable) -> any:
    """Decorate to load content of file as dictionary from a json file."""

    def wrapper(*args: dict, **__: dict) -> any:
        parent = Path(__file__).parent

        # load test data
        with Path(f"{parent}/data/base_record_test.json").open() as fp:
            record = load(fp)

        with Path(f"{parent}/data/{args[2]}.json").open() as fp:
            test = load(fp)

        record["metadata"] = test

        # load expected data
        env = Environment(
            loader=FileSystemLoader(f"{parent}/data/"),
            autoescape=False,  # noqa: S701
        )
        template = env.get_template(f"{args[3]}.json")

        replace_metadata = {
            "CURRENT_YEAR": datetime.now(UTC).year,
        }

        rendered = template.render(replace_metadata)
        expected = loads(rendered)

        return func(args[1], record, expected)

    return decorator.decorator(wrapper, func)


@pytest.mark.parametrize(
    ("test", "expected"),
    [
        ("primer_test", "primer_expected"),
        ("publ_ebook_test", "publ_ebook_expected"),
        ("publ_ebook2_test", "publ_ebook2_expected"),
        ("publ_article_test", "publ_article_expected"),
        ("record_w_issues_test", "record_w_issues_expected"),
        ("contribution_types_test", "contribution_types_expected"),
        ("contribution_types2_test", "contribution_types2_expected"),
    ],
)
@load_as_json
def test_datacite43_serializer(app, test, expected):
    """Test serializer to DataCite 4.3 JSON."""
    with app.app_context():
        record = Marc21Record.create(data=test)
        serializer = Marc21DataCite43JSONSerializer()
        serialized_record = serializer.dump_obj(record)
    assert serialized_record == expected
