# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
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
                "invenio-records-marc21-landing-page": "./js/invenio_records_marc21/landing_page/index.js",
                "invenio-records-marc21-search": "./js/invenio_records_marc21/search/index.js",
                "invenio-records-marc21-user-dashboard": "./js/invenio_records_marc21/user_dashboard/index.js",
            },
            dependencies={
                "@babel/runtime": "^7.9.0",
                "marcjs": "^2.0.0",
                "i18next": "^20.3.0",
                "i18next-browser-languagedetector": "^6.1.0",
                "react-i18next": "^11.11.0",
            },
            aliases={
                "@js/invenio_records_marc21": "js/invenio_records_marc21",
                "@less/invenio_records_marc21": "./less/invenio_records_marc21",
                "@translations/invenio_records_marc21": "translations/invenio_records_marc21",
            },
        ),
    },
)
