# SPDX-FileCopyrightText: 2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Marc21 deserializers tests."""

from collections.abc import Callable
from json import load
from pathlib import Path
from typing import Any

import decorator
import pytest

from invenio_records_marc21.resources.deserializers import Marc21Schema


def load_as_json(func: Callable) -> Any:  # noqa: ANN401
    """Decorate to load content of file as dictionary from a json file."""

    def wrapper(*args: dict, **__: dict) -> Any:  # noqa: ANN401
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
        ("dataset_1_test", "dataset_1_expected"),
    ],
)
@load_as_json
def test_marc21_schema(app, test, expected):
    """Test Marc21 schema."""
    with app.app_context():
        schema = Marc21Schema()
        loaded_metadata = schema.load_metadata(value=test)

    assert loaded_metadata == expected
