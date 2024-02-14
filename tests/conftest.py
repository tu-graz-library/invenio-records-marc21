# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2024 Graz University of Technology.
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
from invenio_access.models import ActionRoles
from invenio_access.permissions import superuser_access
from invenio_accounts.models import Role
from invenio_app.factory import create_app as _create_app
from invenio_rdm_records.services.pids import PIDManager, PIDsService, providers
from invenio_records_resources.services import FileService

from invenio_records_marc21.records import Marc21Draft, Marc21Parent, Marc21Record
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
from invenio_records_marc21.services.pids import Marc21DataCitePIDProvider

from .fake_datacite_client import FakeDataCiteClient


def _(x):
    """Identity function for string extraction."""
    return x


@pytest.fixture()
def embargoed_record():
    """Embargoed record."""
    embargoed_record = {
        "metadata": {
            "fields": {
                "001": "990004519310204517",
                "005": "20200511091822.0",
                "007": "tu",
                "008": "131003|2012    |||      m    ||| 0 eng c",
                "009": "AC11056824",
                "015": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": ["OeBB"], "2": ["oeb"]},
                    }
                ],
                "035": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": ["(EXLNZ-43ACC_NETWORK)990110601970203331"]},
                    }
                ],
                "040": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "a": ["TUG"],
                            "b": ["ger"],
                            "d": ["AT-UBTUG"],
                            "e": ["rakwb"],
                        },
                    }
                ],
                "041": [{"ind1": "_", "ind2": "_", "subfields": {"a": ["eng"]}}],
                "044": [{"ind1": "_", "ind2": "_", "subfields": {"c": ["XA-AT"]}}],
                "084": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": ["53.16"], "2": ["bkl"]},
                    }
                ],
                "090": [{"ind1": "_", "ind2": "_", "subfields": {"h": ["g"]}}],
                "100": [
                    {
                        "ind1": "1",
                        "ind2": "_",
                        "subfields": {"a": ["Sch\u00fctz, Denis"], "4": ["aut"]},
                    }
                ],
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {
                            "a": [
                                "<<The>> development of high strain actuator materials"
                            ],
                            "c": ["Denis Sch\u00fctz"],
                        },
                    }
                ],
                "264": [
                    {"ind1": "3", "ind2": "0", "subfields": {"b": ["TU Graz"]}},
                    {"ind1": "_", "ind2": "1", "subfields": {"c": ["2012"]}},
                ],
                "300": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "a": ["Getr. Z\u00e4hlung"],
                            "b": ["Ill., zahlr. graph. Darst."],
                        },
                    }
                ],
                "502": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": ["Graz, Techn. Univ., Diss., 2012"]},
                    }
                ],
                "689": [
                    {"ind1": "0", "ind2": "_", "subfields": {"5": ["AT-OBV", "ONBREB"]}}
                ],
                "856": [
                    {
                        "ind1": "4",
                        "ind2": "_",
                        "subfields": {
                            "u": ["https://url-of-page.com/file/download"],
                            "x": ["TUG"],
                            "3": ["Volltext"],
                        },
                    }
                ],
                "970": [
                    {
                        "ind1": "2",
                        "ind2": "_",
                        "subfields": {"a": ["TUG"], "d": ["HS-DISS"]},
                    }
                ],
                "974": [
                    {
                        "ind1": "0",
                        "ind2": "s",
                        "subfields": {"F": ["051"], "A": ["mu||w||"]},
                    }
                ],
                "996": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "a": [
                                "Fak. f\u00fcr Techn. Chemie, Verfahrenstechn. und Biotechnologie"
                            ],
                            "9": ["local"],
                        },
                    }
                ],
                "AVA": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "0": ["990004519310204517"],
                            "8": ["2237724340004517"],
                            "a": ["43ACC_TUG"],
                            "b": ["FHB"],
                            "c": ["TUG Hochschulschriften (TUGHS)"],
                            "d": ["6000/2012 S385"],
                            "e": ["available"],
                            "f": ["1"],
                            "g": ["0"],
                            "j": ["TUGHS"],
                            "k": ["8"],
                            "p": ["1"],
                            "q": ["Hauptbibliothek"],
                        },
                    }
                ],
            },
            "leader": "01198nam a2200397 c 4500",
        },
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
        "pids": {},
        "files": {
            "enabled": False,  # Most tests don"t care about files
        },
    }
    return embargoed_record


@pytest.fixture()
def marc21_record():
    """Normal record."""
    marc21_record = {
        "metadata": {
            "fields": {
                "001": "990004519310204517",
                "005": "20200511091822.0",
                "007": "tu",
                "008": "131003|2012    |||      m    ||| 0 eng c",
                "009": "AC11056824",
                "015": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": ["OeBB"], "2": ["oeb"]},
                    }
                ],
                "035": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": ["(EXLNZ-43ACC_NETWORK)990110601970203331"]},
                    }
                ],
                "040": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "a": ["TUG"],
                            "b": ["ger"],
                            "d": ["AT-UBTUG"],
                            "e": ["rakwb"],
                        },
                    }
                ],
                "041": [{"ind1": "_", "ind2": "_", "subfields": {"a": ["eng"]}}],
                "044": [{"ind1": "_", "ind2": "_", "subfields": {"c": ["XA-AT"]}}],
                "084": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": ["53.16"], "2": ["bkl"]},
                    }
                ],
                "090": [{"ind1": "_", "ind2": "_", "subfields": {"h": ["g"]}}],
                "100": [
                    {
                        "ind1": "1",
                        "ind2": "_",
                        "subfields": {"a": ["Sch\u00fctz, Denis"], "4": ["aut"]},
                    }
                ],
                "245": [
                    {
                        "ind1": "1",
                        "ind2": "0",
                        "subfields": {
                            "a": [
                                "<<The>> development of high strain actuator materials"
                            ],
                            "c": ["Denis Sch\u00fctz"],
                        },
                    }
                ],
                "264": [
                    {"ind1": "3", "ind2": "0", "subfields": {"b": ["TU Graz"]}},
                    {"ind1": "_", "ind2": "1", "subfields": {"c": ["2012"]}},
                ],
                "300": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "a": ["Getr. Z\u00e4hlung"],
                            "b": ["Ill., zahlr. graph. Darst."],
                        },
                    }
                ],
                "502": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {"a": ["Graz, Techn. Univ., Diss., 2012"]},
                    }
                ],
                "689": [
                    {"ind1": "0", "ind2": "_", "subfields": {"5": ["AT-OBV", "ONBREB"]}}
                ],
                "856": [
                    {
                        "ind1": "4",
                        "ind2": "_",
                        "subfields": {
                            "u": ["https://url-of-page.com/file/download"],
                            "x": ["TUG"],
                            "3": ["Volltext"],
                        },
                    }
                ],
                "970": [
                    {
                        "ind1": "2",
                        "ind2": "_",
                        "subfields": {"a": ["TUG"], "d": ["HS-DISS"]},
                    }
                ],
                "971": [
                    {
                        "ind1": "7",
                        "ind2": "_",
                        "subfields": {
                            "a": ["gesperrt"],
                            "b": ["2012-02-03"],
                            "c": ["2023-03-04"],
                        },
                    },
                ],
                "974": [
                    {
                        "ind1": "0",
                        "ind2": "s",
                        "subfields": {"F": ["051"], "A": ["mu||w||"]},
                    }
                ],
                "996": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "a": [
                                "Fak. f\u00fcr Techn. Chemie, Verfahrenstechn. und Biotechnologie"
                            ],
                            "9": ["local"],
                        },
                    }
                ],
                "AVA": [
                    {
                        "ind1": "_",
                        "ind2": "_",
                        "subfields": {
                            "0": ["990004519310204517"],
                            "8": ["2237724340004517"],
                            "a": ["43ACC_TUG"],
                            "b": ["FHB"],
                            "c": ["TUG Hochschulschriften (TUGHS)"],
                            "d": ["6000/2012 S385"],
                            "e": ["available"],
                            "f": ["1"],
                            "g": ["0"],
                            "j": ["TUGHS"],
                            "k": ["8"],
                            "p": ["1"],
                            "q": ["Hauptbibliothek"],
                        },
                    }
                ],
            },
            "leader": "01198nam a2200397 c 4500",
        },
        "access": {
            "files": "public",
            "status": "public",
            "record": "public",
            "embargo": {
                "active": False,
                "reason": None,
            },
        },
        "pids": {},
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
def app_config(app_config):
    """Application config fixture."""
    app_config["DB_VERSIONING"] = False

    app_config["RATELIMIT_ENABLED"] = False
    app_config["RECORDS_REFRESOLVER_CLS"] = (
        "invenio_records.resolver.InvenioRefResolver"
    )
    app_config["RECORDS_REFRESOLVER_STORE"] = (
        "invenio_jsonschemas.proxies.current_refresolver_store"
    )

    # Variable not used. We set it to silent warnings
    app_config["JSONSCHEMAS_HOST"] = "not-used"
    app_config["MARC21_PERMISSION_POLICY"] = Marc21RecordPermissionPolicy
    # Enable DOI miting
    app_config["DATACITE_ENABLED"] = True
    app_config["DATACITE_USERNAME"] = "INVALID"
    app_config["DATACITE_PASSWORD"] = "INVALID"
    app_config["DATACITE_PREFIX"] = "10.123"
    app_config["OAISERVER_ID_PREFIX"] = "oai:repo"
    app_config["MARC21_PERSISTENT_IDENTIFIER_PROVIDERS"] = [
        # DataCite DOI provider with fake client
        Marc21DataCitePIDProvider(
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


RunningApp = namedtuple(
    "RunningApp",
    [
        "app",
        "db",
        "service",
        "location",
        "adminuser_identity",
    ],
)


@pytest.fixture()
def admin_role_need(app, db):
    """Store 1 role with manager permission."""
    admin_role = Role(name="Marc21Manager")
    db.session.add(admin_role)
    action_role = ActionRoles.create(action=superuser_access, role=admin_role)
    db.session.add(action_role)
    db.session.commit()
    return admin_role


@pytest.fixture()
def adminuser_identity(adminuser, admin_role_need):
    """Superuser identity fixture."""
    identity = adminuser.identity
    identity.provides.add(admin_role_need)

    return identity


@pytest.fixture()
def adminuser(UserFixture, app, db, admin_role_need):
    """Superuser."""
    u = UserFixture(
        email="admin@marc21.at",
        password="superuser",
    )
    u.create(app, db)

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(u.user, "Marc21Manager")

    datastore.add_role_to_user(u.user, role)
    datastore.commit()
    return u


@pytest.fixture()
def superuser_role_need(db):
    """Store 1 role with 'superuser-access' ActionNeed."""
    role = Role(name="superuser-access")
    db.session.add(role)

    action_role = ActionRoles.create(action=superuser_access, role=role)
    db.session.add(action_role)

    db.session.commit()

    return action_role.need


@pytest.fixture()
def superuser(UserFixture, app, db, superuser_role_need):
    """Superuser."""
    u = UserFixture(
        email="superuser@marc21.at",
        password="superuser",
    )
    u.create(app, db)

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(u.user, "superuser-access")

    datastore.add_role_to_user(u.user, role)
    db.session.commit()
    datastore.commit()
    return u


@pytest.fixture()
def superuser_identity(superuser, superuser_role_need):
    """Superuser identity fixture."""
    identity = superuser.identity
    identity.provides.add(superuser_role_need)
    return identity


@pytest.fixture
def running_app(app, db, location, adminuser_identity):
    """This fixture provides an app with the typically needed db data loaded.

    All of these fixtures are often needed together, so collecting them
    under a semantic umbrella makes sense.
    """
    service = app.extensions["invenio-records-marc21"].records_service
    return RunningApp(app, db, service, location, adminuser_identity)


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return _create_app


def _search_create_indexes(current_search, current_search_client):
    """Create all registered search indexes."""
    to_create = [
        Marc21Record.index._name,
        Marc21Draft.index._name,
    ]
    # list to trigger iter
    list(current_search.create(ignore_existing=True, index_list=to_create))
    current_search_client.indices.refresh()


def _search_delete_indexes(current_search):
    """Delete all registered search indexes."""
    to_delete = [
        Marc21Record.index._name,
        Marc21Draft.index._name,
    ]
    list(current_search.delete(index_list=to_delete))


# overwrite pytest_invenio.fixture to only delete record indices
# keeping vocabularies.
@pytest.fixture()
def search_clear(search):
    """Clear search indices after test finishes (function scope).

    This fixture rollback any changes performed to the indexes during a test,
    in order to leave search in a clean state for the next test.
    """
    from invenio_search import current_search, current_search_client

    yield search
    _search_delete_indexes(current_search)
    _search_create_indexes(current_search, current_search_client)


@pytest.fixture(scope="module")
def cli_runner(base_app):
    """Create a CLI runner for testing a CLI command."""

    def cli_invoke(command, *args, input=None):
        return base_app.test_cli_runner().invoke(command, args, input=input)

    return cli_invoke
