# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2022 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "invenio-records-marc21-theme": "./less/invenio_records_marc21/theme.less",
                "invenio-records-marc21-deposit": "./js/invenio_records_marc21/deposit/index.js",
                "invenio-records-marc21-search": "./js/invenio_records_marc21/search/index.js",
                "invenio-records-marc21-landing-page": "./js/invenio_records_marc21/landing_page/index.js",
            },
            dependencies={
                "@babel/runtime": "^7.9.0",
                "react-records-marc21": "^0.2.0",
                "react-invenio-deposit": "^1.0.2",
            },
            aliases={
                "@less/invenio_records_marc21": "./less/invenio_records_marc21",
            },
        ),
    },
)
