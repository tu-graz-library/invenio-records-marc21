# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

from collections import namedtuple
from datetime import timedelta

import arrow
import pytest
from invenio_access.permissions import any_user
from invenio_app.factory import create_api
from invenio_rdm_records.services.pids import PIDManager, PIDsService, providers
from invenio_records_resources.services import FileService

from invenio_records_marc21.records import Marc21Draft, Marc21Parent
from invenio_records_marc21.resources.serializers.datacite import (
    Marc21DataCite43JSONSerializer,
)
from invenio_records_marc21.services import (
    Marc21DraftFilesServiceConfig,
    Marc21RecordFilesServiceConfig,
    Marc21RecordPermissionPolicy,
    Marc21RecordService,
    Marc21RecordServiceConfig,
)

from .fake_datacite_client import FakeDataCiteClient


def _(x):
    """Identity function for string extraction."""
    return x


@pytest.fixture()
def embargoed_record():
    """Embargoed record."""
    embargoed_record = {
        "metadata": {"json": "test"},
        "access": {
            "record": "restricted",
            "files": "restricted",
            "status": "embargoed",
            "embargo": {
                "active": True,
                "until": (arrow.utcnow().datetime + timedelta(days=-365)).strftime(
                    "%Y-%m-%d"
                ),
                "reason": None,
            },
        },
        "files": {
            "enabled": False,  # Most tests don't care about files
        },
    }
    return embargoed_record


@pytest.fixture()
def marc21_record():
    """Normal record."""
    marc21_record = {
        "metadata": {"json": "test"},
        "access": {
            "files": "public",
            "status": "public",
            "record": "public",
            "embargo": {
                "active": False,
                "reason": None,
            },
        },
        "files": {"enabled": False},
    }
    return marc21_record


@pytest.fixture()
def parent(app, db):
    """A parent record."""
    return Marc21Parent.create({})


@pytest.fixture()
def example_record(app, db):
    """Example record."""
    record = Marc21Draft.create({}, metadata={"title": "Test"})
    db.session.commit()
    return record


@pytest.fixture(scope="module")
def celery_config():
    """Override pytest-invenio fixture.

    TODO: Remove this fixture if you add Celery support.
    """
    return {}


@pytest.fixture(scope="module")
def app_config(app_config, db_uri):
    """Application config fixture."""
    app_config["SQLALCHEMY_DATABASE_URI"] = db_uri

    app_config["RATELIMIT_ENABLED"] = False
    app_config[
        "RECORDS_REFRESOLVER_CLS"
    ] = "invenio_records.resolver.InvenioRefResolver"
    app_config[
        "RECORDS_REFRESOLVER_STORE"
    ] = "invenio_jsonschemas.proxies.current_refresolver_store"

    # Variable not used. We set it to silent warnings
    app_config["JSONSCHEMAS_HOST"] = "not-used"
    app_config["RDM_PERMISSION_POLICY"] = Marc21RecordPermissionPolicy
    # Enable DOI miting
    app_config["DATACITE_ENABLED"] = True
    app_config["DATACITE_USERNAME"] = "INVALID"
    app_config["DATACITE_PASSWORD"] = "INVALID"
    app_config["DATACITE_PREFIX"] = "10.123"
    app_config["INVENIO_MARC21_PERSISTENT_IDENTIFIER_PROVIDERS"] = [
        # DataCite DOI provider with fake client
        providers.DataCitePIDProvider(
            "datacite",
            client=FakeDataCiteClient("datacite", config_prefix="DATACITE"),
            pid_type="doi",
            serializer=Marc21DataCite43JSONSerializer(),
            label=_("DOI"),
        ),
        # DOI provider for externally managed DOIs
        providers.ExternalPIDProvider(
            "external",
            "doi",
            validators=[providers.BlockedPrefixes(config_names=["DATACITE_PREFIX"])],
            label=_("DOI"),
        ),
    ]

    return app_config


@pytest.fixture
def service(app):
    """Service instance."""
    config = Marc21RecordServiceConfig.build(app)

    return Marc21RecordService(
        config=config,
        files_service=FileService(Marc21RecordFilesServiceConfig()),
        draft_files_service=FileService(Marc21DraftFilesServiceConfig()),
        pids_service=PIDsService(config, PIDManager),
    )


RunningApp = namedtuple("RunningApp", ["app", "db", "service", "location"])


@pytest.fixture
def running_app(app, db, location):
    """This fixture provides an app with the typically needed db data loaded.

    All of these fixtures are often needed together, so collecting them
    under a semantic umbrella makes sense.
    """
    service = app.extensions["invenio-records-marc21"].records_service
    return RunningApp(app, db, service, location)


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return create_api
