..
    Copyright (C) 2021 Graz University of Technology.

    Invenio-Records-Marc21 is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======

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
