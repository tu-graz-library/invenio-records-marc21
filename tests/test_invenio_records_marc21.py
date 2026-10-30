# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Module tests."""

from flask import Flask

from invenio_records_marc21 import InvenioRecordsMARC21


def test_version():
    """Test version import."""
    from invenio_records_marc21 import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioRecordsMARC21(app)
    assert "invenio-records-marc21" in app.extensions

    app = Flask("testapp")
    ext = InvenioRecordsMARC21()
    assert "invenio-records-marc21" not in app.extensions
    ext.init_app(app)
    assert "invenio-records-marc21" in app.extensions
