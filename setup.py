# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 datamodel"""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = [
    "invenio-records>=1.1.0",
    "invenio-app>=1.3.0,<2.0.0",
    "invenio-access>=1.4.1",
    "invenio-indexer>=1.1.0",
    "invenio_search>=1.3.1",
    "pytest-invenio>=1.4.0",
    "mock>=4.0.3",
]

# Should follow inveniosoftware/invenio versions
invenio_db_version = ">=1.0.4,<2.0.0"
invenio_search_version = ">=1.4.0,<2.0.0"

extras_require = {
    "docs": [
        "Sphinx>=3,<4",
    ],
    "elasticsearch7": [
        "invenio-search[elasticsearch7]{}".format(invenio_search_version),
    ],
    "postgresql": [
        "invenio-db[postgresql,versioning]{}".format(invenio_db_version),
    ],
    "tests": tests_require,
}

extras_require["all"] = []
for name, reqs in extras_require.items():
    if name[0] == ":" or name in ("elasticsearch7", "postgresql"):
        continue
    extras_require["all"].extend(reqs)

setup_requires = [
    "Babel>=2.8",
    "pytest-runner>=3.0.0,<5",
]

install_requires = [
    "invenio-i18n>=1.2.0",
    "dojson>=1.4.0",
    "invenio-jsonschemas>=1.1.0",
    "invenio-records>=1.4.0a4,<2.0.0",
    "invenio-records-rest>=1.4.0,<2.0.0",
    "invenio-records-ui>=1.2.0a1,<2.0.0",
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("invenio_records_marc21", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="invenio-records-marc21",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords="invenio Marc21",
    license="MIT",
    author="Graz University of Technology",
    author_email="info@tugraz.at",
    url="https://github.com/tu-graz-library/invenio-records-marc21",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "invenio_base.apps": [
            "invenio_records_marc21 = invenio_records_marc21:InvenioRecordsMARC21",
        ],
        "invenio_base.blueprints": [
            "invenio_records_marc21 = invenio_records_marc21.views:blueprint",
        ],
        "invenio_i18n.translations": [
            "messages = invenio_records_marc21",
        ],
        # TODO: Edit these entry points to fit your needs.
        # 'invenio_access.actions': [],
        # 'invenio_admin.actions': [],
        # 'invenio_assets.bundles': [],
        # 'invenio_base.api_apps': [],
        # 'invenio_base.api_blueprints': [],
        # 'invenio_base.blueprints': [],
        # 'invenio_celery.tasks': [],
        # 'invenio_db.models': [],
        # 'invenio_pidstore.minters': [],
        # 'invenio_records.jsonresolver': [],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 1 - Planning",
    ],
)
