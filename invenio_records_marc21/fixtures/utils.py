# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 fixtures utils."""

import json
from os.path import dirname, join


def load_json(filename):
    """Helper function to load json."""
    with open(join(dirname(__file__), filename), "rb") as fp:
        return json.load(fp)
