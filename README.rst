..
    Copyright (C) 2021 Graz University of Technology.

    Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

========================
 Invenio-Records-Marc21
========================

.. image:: https://img.shields.io/github/license/tu-graz-library/invenio-records-marc21.svg
        :target: https://github.com/tu-graz-library/invenio-records-marc21/blob/master/LICENSE

.. image:: https://github.com/tu-graz-library/invenio-records-marc21/workflows/CI/badge.svg
        :target: https://github.com/tu-graz-library/invenio-records-marc21/actions

.. image:: https://img.shields.io/coveralls/tu-graz-library/invenio-records-marc21.svg
        :target: https://coveralls.io/r/tu-graz-library/invenio-records-marc21

.. image:: https://img.shields.io/pypi/v/invenio-records-marc21.svg
        :target: https://pypi.org/pypi/invenio-records-marc21

Marc21 datamodel

Further documentation is available on
https://invenio-records-marc21.readthedocs.io/


Development
===========

Install
-------

Choose a version of elasticsearch and a DB, then run:

.. code-block:: console

    pipenv run pip install -e .[all]
    pipenv run pip install invenio-search[elasticsearch7]
    pipenv run pip install invenio-db[postgresql,versioning]


Service
=========

** Create Marc21 Record**

Tests
=========

.. code-block:: console

    pipenv run ./run-tests.sh

Features
========

This package serves as a MARC21 datamodel for the repository. Following features
are already implemented:

  - [ ] create a record

    - [ ] over rest API
    - [ ] over GUI

  - [ ] modify a record

    - [ ] over rest API
    - [ ] over GUI

  - [ ] inherit from the global permission system and customize it if necessary

    - [ ] create a curator for marc21 records over the normal interface for it
    - [ ] inherit ownership of records
    - [ ] lock records / make read only

  - [ ] landing page

    - [ ] export record as json

  - [ ] search about a record

    - [ ] create a search page only for marc21 records
    - [ ] make records findable also in the common search (search over all
      standards used in the repository)

  - [ ] add records to a community
  - [ ] validate records
  - [ ] add a DOI

    - [ ] with a special DOI schema (e.g. PREFIX/oer-NUMBER)

  - [ ] provide the records to the OAI-PMH server


Examples where this packages is already used:

  - <https://github.com/tu-graz-library/invenio-alma>
