..
    Copyright (C) 2021-2024 Graz University of Technology.

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


Setting Up Statistics
=====================

To enable and configure the statistics feature using MARC21 records in Invenio, you need to update your `invenio.cfg` file with specific configurations that integrate MARC21 statistics with Invenio's standard statistics modules.

### Configuration Steps

1. **Import Required Configurations:**

   Before updating the configuration values, ensure that you import the necessary settings from both the `invenio_records_marc21` module and the `invenio_app_rdm` module. Add the following lines to your `invenio.cfg`:

.. code-block:: console

    from invenio_records_marc21.config import MARC21_STATS_CELERY_TASKS, MARC21_STATS_EVENTS, MARC21_STATS_AGGREGATIONS, MARC21_STATS_QUERIES
    from invenio_app_rdm.config import CELERY_BEAT_SCHEDULE, STATS_EVENTS, STATS_AGGREGATIONS, STATS_QUERIES

Update Celery Beat Schedule:

Integrate MARC21-specific scheduled tasks with Invenio's scheduler:

.. code-block:: console

    CELERY_BEAT_SCHEDULE.update(MARC21_STATS_CELERY_TASKS)


Update Events, Aggregations, and Queries:

Merge MARC21 statistics configurations with the global statistics settings:

.. code-block:: console

    STATS_EVENTS.update(MARC21_STATS_EVENTS)
    STATS_AGGREGATIONS.update(MARC21_STATS_AGGREGATIONS)
    STATS_QUERIES.update(MARC21_STATS_QUERIES)


Tests
=========

.. code-block:: console

    pipenv run ./run-tests.sh
