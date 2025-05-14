..
    Copyright (C) 2021 Graz University of Technology.

    Invenio-Records-Marc21 is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======

Version v0.25.0 (release 2025-05-14)

- wip: move documentation to README
- ui: add new upload button
- chore: fix indentation


Version v0.24.1 (release 2025-04-30)

- fix: jsonschema user


Version v0.24.0 (release 2025-04-29)

- fix(tests): add configuration
- setup: add python3.13 support
- revert: remove of convert_marc21xml_to_json
- fix(links): for doi only doi
- rdm: compatibility
- metadata: add new method
- feat: make links configurable


Version v0.23.0 (release 2025-01-24)

- cli: password is per default hided
- setup: only for dev tags, will be removed
- refactor: cli demo,templates -> fixtures
- fix: LegacyAPIWarning
- tests: remove invenio-admin usage
- fix: datacite serialization
- refactor: change internal representation to json


Version v0.22.2 (release 2024-10-31)

- fix: fields could be missing
- ui: add elements to details
- fix(deposit): page render and save a empty record


Version v0.22.1 (release 2024-10-26)

- fix: creator only allowed to interact with owned records


Version v0.22.0 (release 2024-10-26)

- ui: add separator ti author detail
- setup: move to python 3.12
- fix: empty values shouldn't be displayed
- ui: published could be in 260 too
- permission: add role creator
- change: allow ' ' as not set indicator
- remove marcxml transport layer
- ui: add affiliation
- fix: multiple 700 not send to client
- fix: apply header change from rdm-records
- fix: the following / prevents rspack from building
- setup: migrate to finalize_app
- upgrade: add script to upgrade parent
- feat: files serializer use marc21 accept header
- style: improve codequality
- feat: resource type to search facets
- feat: index static metadata fields


Version v0.21.2 (release 2024-06-13)

- feat: active dashoard menu item
- fix: typo on attribute name


Version v0.21.1 (release 2024-05-19)

- translations: update wording
- bugfix: search records user dashboard


Version v0.21.0 (release 2024-05-06)

- modification: change permission for managing record access
- modifciation: documentation for statistic
- modification: landing page record title
- modification: init statistic for a record


Version v0.20.0 (release 2024-03-08)

- deps: remove upper limit of rdm-records
- modification: pretty export records
- fix(deposit): react remove deprecated dependency


Version v0.19.1 (release 2024-02-19)

- fix: embargo date could contain strings


Version v0.19.0 (release 2024-02-19)

- landingpage: embargo date from marc21 metadata


Version v0.18.0 (release 2024-02-14)

- fix: dashboard-visibility not working
- modification(search): : Apply Same Style to Publication Search Bar
- setup: increase upper limits
- black: fix v24.2.0
- fix: frontent serializer following whitespace


Version v0.17.3 (release 2024-01-11)

- fix: indexer needs queue name


Version v0.17.2 (release 2024-01-07)

- setup: add support for python3.10 and 3.11
- fix: controlfield not correct build for marcxml
- fix: ind1 could be undefined
- ui: move react-records-marc21 code here
- fix: rebuild-index not working
- fix: missing special for AVE
- bugfix: add schema to record


Version v0.17.1 (release 2023-12-01)

- alembic: add missing deletion_status


Version v0.17.0 (release 2023-11-09)

- ui: change dependency to invenio_rdm_records
- bugfix: files links list
- bugfix: add missing permissions
- CI: disable python 3.10
- tests: remove sqlalchemy NoResultFound
- tests: modification to testset and codestyle
- modification: permission policy records and files
- modification: create marc21 v2 schema and mappings
- global: change path to publications
- tests: add parameters to run-tests
- ui: redesign edit button
- records: add deletion_status
- services: make components customizable
- cli: change parameters
- resources: add dublin core serializer
- build:  limit draft resource version
- testset: modification files in record
- modification: import structure
- modification: unit of work
- modification: parent schema
- tests: fix test
- modification: records service config
- modifcation: use invenio-i18n translations module
- modification: create demo records
- modification: serializer structure
- build: bump version
- modification: marc21 v1 mapping
- modification: result item on dashboard
- modification: search mapping
- modification: user dashboard translations
- modification: translations in config module
- modification: empty search result
- translations: resource type translations
- modification: resource type translate
- modification: code style
- modification: gitignore
- translations: i18next update
- modification: result item translations
- modification: dashboard layout
- modification: user dashboard search
- fix: subfield may not exist
- landing-page: add additional titles
- translations: update
- modification: user dashboard search application
- modification: search components
- modification: configuration search application
- modification: api search options
- modification: clean code


Version v0.16.1 (release 2023-09-14)

- fix: doi modal


Version v0.16.0 (release 2023-09-14)

- landing_page: conditional wrap show doi
- modification: translations
- translation: update
- refactoring: variable naming
- landing_page: increase space above title
- landing-page: change created at to published
- landing_page: use improved export
- bugfix: import landing page


Version v0.15.0 (release 2023-09-12)

- fix: create_record dangling draft
- modification: gitignore
- modification: translations update
- modification: templates structured
- modification: add comments
- modifications: marc21 service permissions


Version v0.14.2 (release 2023-06-16)

- fix: namespace handling was wrong


Version v0.14.1 (release 2023-06-07)

- fix: remove whitespace and close div tag


Version v0.14.0 (release 2023-06-07)

- modification: alembic scripts
- modification: remove prefix in configuration variables


Version v0.13.2 (release 2023-06-05)

- bugfix: draft get file content


Version v0.13.1 (release 2023-06-01)

- bugfix: load default roles needed


Version v0.13.0 (release 2023-05-25)

- setup: remove compatibility check with python3.8
- metadata: add methods to get fields and values


Version v0.12.7 (release 2023-05-12)

- metadata: subfs, character before numbers


Version v0.12.6 (release 2023-05-11)

- pids: remove 2 subfields


Version v0.12.5 (release 2023-05-11)

- fix: metadata export needs a space


Version v0.12.4 (release 2023-05-10)

- doi: apply marc21 request changes
- tests: cleaned tests, remove unused statements
- metadata: add 856 field after doi creation
- modification: templates load from roles


Version v0.12.3 (release 2023-04-28)

- fix: distinguish between str and list


Version v0.12.2 (release 2023-04-25)

- bugfix: previewer allow to access files


Version v0.12.1 (release 2023-04-20)




Version v0.11.0 (release 2023-03-06)

- permissions: re-add SystemProcess to can_manage
- fix: to keep flask-babelex
- permissions: enlarge permission system
- modification: update marc21 record permissions
- modification: remove duplicate code
- modification: add pids to new version
- bugfix: create new version
- modification: dashboard records edit


Version v0.10.0 (release 2023-02-13)

- fix: category could be AVA
- modification: add fix me in the future
- modification: create dashboard entry for marc21


Version v0.9.2 (release 2023-02-09)

- fix: sort xml subfields generation
- fix: the value in subfs is a list
- fix: unify order of et.Element attributes


Version v0.9.1 (release 2023-01-23)

- fix: wrong alias for drafts and records
- modification: record status in deposit


Version v0.9.0 (release 2023-01-11)

- metadata: use id property instead
- fixes:
- global: pass through exports
- modification: add multiple files to record
- metadata: add param do_publish
- metadata: add exists method
- ui: update react-records-marc21
- services: add exception for common search
- services: add types
- codestyle: deposit form
- modification: deposit form style
- tests: testset update
- modification: put doi into the metadata
- modification: create identifier with draft
- bugfix: files enabled
- fix: correct CHANGES.rst


Version v0.8.4 (release 2022-11-17)

- fix:
- api: add duplicate check function
- fix
- metadata: implement convert_json_to_marc21xml
- metadata: add default values to selector
- api: add two functions moved from invenio-alma
- improve: add subfs parameter to emplace_datafield
- modification: add access_status field
- modification: use jast jsonschema
- codestyle: variable on top of the function definition.
- modification: service file config
- modification: api register services
- modification: create draft with errors
- modification: deposit structure
- modification: deposit application


Version v0.8.3 (release 2022-11-02)

- fix
- metadata: implement convert_json_to_marc21xml
- metadata: add default values to selector
- api: add two functions moved from invenio-alma
- improve: add subfs parameter to emplace_datafield
- fix: remove import of semantic css


Version v0.8.2 (release 2022-10-14)

- fix: pypi-publish inherit secrets


Version v0.8.1 (release 2022-10-14)

- global: migrate publish to reusable workflows
- setup: fix classifier


Version v0.8.0 (release 2022-10-14)

- tests: move to resuable workflows
- tests: remove CACHE and MQ
- setup: sort imports, remove doublets
- global: migrate to opensearch2


Version v0.7.5 (release 2022-09-27)

- fix: javascript dependencies


Version v0.7.4 (release 2022-09-27)

- fix: ConfigurationMixin changed location
- global: increase version of invenio-search


Version v0.7.3 (release 2022-08-10)

- fix use 009[7:11] for publication year


Version v0.7.2 (release 2022-08-10)

- modification: datacite schema\n\n changing the field numbers
- tests: modification datacite testset
- bugfix: pids components from rdm records


Version v0.7.1 (release 2022-08-09)

- fix: the missing mappings causes an error with the empty search feature


Version v0.7.0 (release 2022-08-04)

- improve (WIP) landing page and search results


Version v0.6.0 (release 2022-08-01)

- make the jsonschema less restrictive


Version v0.5.2 (release 2022-07-29)

- use search react components provided by invenio-app-rdm
- update the search initial query state


Version v0.5.1 (release 2022-07-07)




Version 0.0.1 (released TBD)

- Initial public release.
