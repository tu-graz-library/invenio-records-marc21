# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021-2025 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from flask import Flask
from flask_principal import ActionNeed
from invenio_access.models import ActionRoles
from invenio_access.permissions import superuser_access
from invenio_accounts.models import Role
from invenio_db import InvenioDB
from invenio_files_rest import InvenioFilesREST
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_records import InvenioRecords
from invenio_search import InvenioSearch

from invenio_records_marc21 import InvenioRecordsMARC21


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture for use with pytest-invenio."""

    def _create_app(**config):
        app_ = Flask(
            __name__,
            instance_path=instance_path,
        )
        app_.config.update(config)

        InvenioDB(app_)
        InvenioSearch(app_)
        InvenioFilesREST(app_)
        InvenioRecordsMARC21(app_)
        return app_

    return _create_app


@pytest.fixture(scope="module")
def testapp(base_app, location):
    """Application with just a database.

    Pytest-Invenio also initialises ES with the app fixture.
    """
    InvenioRecords(base_app)
    InvenioJSONSchemas(base_app)
    yield base_app


@pytest.fixture(scope="module")
def appaccess(base_app, database):
    """Create App  systemfields."""
    InvenioRecords(base_app)
    InvenioJSONSchemas(base_app)
    yield base_app


@pytest.fixture(scope="function")
def superuser_role_need(db):
    """Store 1 role with 'superuser-access' ActionNeed.

    WHY: This is needed because expansion of ActionNeed is
         done on the basis of a User/Role being associated with that Need.
         If no User/Role is associated with that Need (in the DB), the
         permission is expanded to an empty list.
    """
    role = Role(name="superuser-access")
    db.session.add(role)

    action_role = ActionRoles.create(action=superuser_access, role=role)
    db.session.add(action_role)

    db.session.commit()

    return action_role.need


@pytest.fixture(scope="function")
def superuser_identity(admin, superuser_role_need):
    """Superuser identity fixture."""
    identity = admin.identity
    identity.provides.add(superuser_role_need)
    return identity


@pytest.fixture(scope="function")
def administration_need(db):
    """Store 1 role with 'superuser-access' ActionNeed.

    WHY: This is needed because expansion of ActionNeed is
         done on the basis of a User/Role being associated with that Need.
         If no User/Role is associated with that Need (in the DB), the
         permission is expanded to an empty list.
    """
    role = Role(name="administration")
    db.session.add(role)

    action_role = ActionRoles.create(action=ActionNeed("administration"), role=role)
    db.session.add(action_role)

    db.session.commit()

    return action_role.need


@pytest.fixture()
def admin(UserFixture, app, db, administration_need):
    """Admin user for requests."""
    u = UserFixture(
        email="admin@inveniosoftware.org",
        password="admin",
    )
    u.create(app, db)

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(u.user, "administration")

    datastore.add_role_to_user(u.user, role)
    db.session.commit()
    return u
