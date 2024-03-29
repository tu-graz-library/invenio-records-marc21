# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Test utilities.

NOTE: To get pytest's nice assertions this file had to be prefixed with
`test_` .
"""

import pytest
from marshmallow import ValidationError


def assert_raises_messages(lambda_expression, expected_messages):
    with pytest.raises(ValidationError) as e:
        lambda_expression()

    messages = e.value.normalized_messages()
    assert expected_messages == messages
