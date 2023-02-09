# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio-Records-Marc21 datamodel.

This guide will show you how to get started with
Invenio-Records-Marc21. It assumes that you already have knowledge of
Flask applications and Invenio modules.

It will then explain key topics and concepts of this module.

Getting started
---------------

You will learn how to create a new Marc21 records, upload a file and accosiate with the record
using the programmatic APIs of Invenio-Records-Marc21.


This is the initial configuration needed to have things running:

:py:data:`invenio_records_marc21.config`


Service operations
------------------


Initialization
~~~~~~~~~~~~~~


>>> import os
>>> db_url = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite://')
>>> from flask import Flask
>>> app = Flask('myapp')
>>> app.config.update({
...     "JSONSCHEMAS_HOST": "not-used",
...     "RECORDS_REFRESOLVER_CLS": "invenio_records.resolver.InvenioRefResolver",
...     "RECORDS_REFRESOLVER_STORE": "invenio_jsonschemas.proxies.current_refresolver_store",
...     "SQLALCHEMY_DATABASE_URI": db_url,
...     "SQLALCHEMY_TRACK_MODIFICATIONS": False,
... })

Initialize Invenio-Records-Marc21 dependencies and Invenio-Records-Marc21 itself:

>>> from invenio_db import InvenioDB
>>> ext_db = InvenioDB(app)
>>> from invenio_records import InvenioRecords
>>> ext_records = InvenioRecords(app)
>>> from invenio_access import InvenioAccess
>>> ext_access = InvenioAccess(app)
>>> from invenio_files_rest import InvenioFilesREST
>>> ext_rdm = InvenioFilesREST(app)
>>> from invenio_jsonschemas import InvenioJSONSchemas
>>> ext_json = InvenioJSONSchemas(app)
>>> from invenio_search import InvenioSearch
>>> ext_search = InvenioSearch(app)
>>> from invenio_rdm_records import InvenioRDMRecords
>>> ext_rdm = InvenioRDMRecords(app)
>>> from invenio_records_marc21 import InvenioRecordsMARC21
>>> ext = InvenioRecordsMARC21(app)

The following examples needs to run in a Flask application context, so
let's push one:

>>> app.app_context().push()


Also, for the examples to work we need to create the database and tables (note,
in this example we use an in-memory SQLite database by default):

>>> from invenio_db import db
>>> from sqlalchemy_utils.functions import create_database, database_exists, drop_database
>>> if database_exists(str(db.engine.url)):
...     drop_database(str(db.engine.url))
>>> create_database(str(db.engine.url))
>>> db.create_all()


The Invenio-Records-Marc21 module needs also a location for Files upload, if the
record contains Files.

>>> import tempfile
>>> from invenio_files_rest.models import Location
>>> location_obj = Location(
...     name="marc21-file-location", uri=tempfile.mkdtemp(), default=True
... )

>>> from invenio_db import db
>>> db.session.add(location_obj)
>>> db.session.commit()

Creation
~~~~~~~~


Let's **create** a very simple record:

>>> from invenio_records_marc21.proxies import current_records_marc21
>>> service = current_records_marc21.records_service

>>> from flask_principal import Identity
>>> from invenio_access import any_user
>>> identity = Identity(1)
>>> identity.provides.add(any_user)
>>> draft = service.create(identity=identity, data={"metadata": {"title_statement": {"title": "The title of the record"}}})


A new row has been added to the database, in the table ``marc21_drafts_metadata``:
this corresponds to the record metadata, first version (version 1).


Publish
~~~~~~~~


Let's **publish** our very simple record:

>>> from flask_principal import Identity
>>> from invenio_access import any_user
>>> identity = Identity(1)
>>> identity.provides.add(any_user)
>>> record = service.publish(identity=identity, id_=draft.id)

A new row has been added to the database, in the table ``marc21_records_metadata``:
this corresponds to the record metadata, second version (version 2). The created
Draft from before has been deleted.


Service Advanced
----------------

The Invenio-Records-Marc21 service provides advanced Record creation functionality.

.. code-block::

    def create(self, identity, data=None, metadata=Marc21Metadata(), files=False, access=None):

The Create Method of the Marc21 service  takes additional parameters:

    :data: Input data according to the data schema.
    :metadata: Input data according to the metadata schema and provided in the module `invenio_records_marc21.services.record.Marc21Metadata`.
    :files: enable/disable file support for the record.
    :access: provide additional access information.

The api does not only takes  a json like object e.q. `data`. The Records can be created with only the metadata.

Marc21Metadata
~~~~~~~~~~~~~~

>>> from invenio_records_marc21.services.record import Marc21Metadata
>>> metadata = Marc21Metadata()
>>> metadata.emplace_datafield(selector="245.1.0.", value="nulla sunt laborum")

or set a whole Marc21 xml string

>>> metadata.xml = "<record><leader>00000nam a2200000zca4500</leader></record>"

Access
~~~~~~

The access dict structure required for Invenio-Records-Marc21 records:

>>> access = {
...     "record": "public/restricted",
...     "files": "public/restricted",
...     "embargo": {
...         "active": False/True,
...         "until": "YYYY-MM-DD",
...         "reason": "Reason",
...    }
... }

Now let us put this all together
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


>>> from invenio_records_marc21.proxies import current_records_marc21
>>> service = current_records_marc21.records_service

>>> access = {
...     "record": "public",
...     "files": "public",
...     "embargo": {
...         "active": False,
...    }
... }
>>> from invenio_records_marc21.services.record import Marc21Metadata
>>> from flask_principal import Identity
>>> from invenio_access import any_user
>>> identity = Identity(1)
>>> identity.provides.add(any_user)
>>> metadata = Marc21Metadata()
>>> metadata.xml = "<record><leader>00000nam a2200000zca4500</leader></record>"
>>> draft = service.create(identity=identity, metadata=metadata, access=access)
>>> record = service.publish(identity=identity, id_=draft.id)

See :doc:`api` for extensive API documentation.

"""

from __future__ import absolute_import, print_function

from .ext import InvenioRecordsMARC21
from .proxies import current_records_marc21
from .records import MarcDraftProvider
from .services import (
    DuplicateRecordError,
    Marc21Metadata,
    Marc21RecordService,
    add_file_to_record,
    check_about_duplicate,
    convert_json_to_marc21xml,
    convert_marc21xml_to_json,
    create_record,
)

__version__ = "0.9.2"

__all__ = (
    "__version__",
    "InvenioRecordsMARC21",
    "current_records_marc21",
    "Marc21Metadata",
    "add_file_to_record",
    "create_record",
    "MarcDraftProvider",
    "DuplicateRecordError",
    "check_about_duplicate",
    "convert_json_to_marc21xml",
    "convert_marc21xml_to_json",
    "Marc21RecordService",
)
