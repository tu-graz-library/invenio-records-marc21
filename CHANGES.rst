..
    Copyright (C) 2021 Graz University of Technology.

    Invenio-Records-Marc21 is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======

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
- release v0.8.3
- fix: remove import of semantic css
- release v0.8.2
- fix: pypi-publish inherit secrets
- release v0.8.1
- global: migrate publish to reusable workflows
- setup: fix classifier
- release v0.8.0
- tests: move to resuable workflows
- tests: remove CACHE and MQ
- setup: sort imports, remove doublets
- global: migrate to opensearch2
- release v0.7.5
- fix: javascript dependencies
- release v0.7.4
- fix: ConfigurationMixin changed location
- global: increase version of invenio-search
- release v0.7.3
- fix use 009[7:11] for publication year
- release v0.7.2
- modification: datacite schema\n\n changing the field numbers
- tests: modification datacite testset
- bugfix: pids components from rdm records
- release v0.7.1
- fix: the missing mappings causes an error with the empty search feature
- release v0.7.0
- improve (WIP) landing page and search results
- release v0.6.0
- make the jsonschema less restrictive
- release v0.5.2
- move search configuration to python config
- use search react components provided by invenio-app-rdm
- update the search initial query state
- release v0.5.1
- modification: codestyle and serializer functionality
- modification: deposit records
- modification: service function header update
- modification: serialize Marc21 xml
- bugfix: serializer schema_cls name changed
- modification: codestyle
- modification: remove deposit app
- release v0.5.0
- fix combined fixes
- bugfix docs
- global: simplified tests install
- bugfix: the directory invenio_records_marc21 has to be in testpaths
- update invenio-rdm-records dependency
- fix tests
- bugfix xpath does not exists for xml.etree.ElementTree.Element
- bugfix and remove lxml from metadata.py
- refactor Marc21Metadata
- modification: metadata errors
- modification(tests): record handling\n\nupdating metadata to new structure
- modification: error handling service
- release v0.4.1
- bugfix add babel to pypi-publish
- release v0.4.0
- remove version from side bar, temporary
- modification: merge configuration to setup.cfg
- modification: codestyle
- bugfix: dependencies resolve
- modification: codestyle
- modification(build): change module build
- release: v0.3.0
- bugfix:test-set changed structure
- codesyle: use black
- modification: record schema
- modification: access schema
- feature(index): cli command rebuild marc21 index
- bugfix: RDMRecordService.update_draft changed parameter order
- wip: fix test cases
- make code compatible to v8
- test: datamodel
- modification: change schema
- tests: testset for datamodel
- feature: validate marc21 records
- modification(serializers): convert new datamodel
- feature(datamodel): marc21 to json
- tests: external pids testset
- feature: pids tasks register external pid
-  feature: marc21 datacite json serializer
- modification: init configuration doi
- modification: customization service config
- feature: external pid field
- modification: codestyle
- build: update dependencies
- tests: adding marc21 metadata load etree testset
- modification: codequality improved
- bugfix: remove deprecated function call
- modification: improve codequality
- modification: imporve codequality
- modification: imporve codestyle
- bugfix: format search string
- modification(tests): marc21metadata testset
- modification: use lxml
- modification: convert marcxml
- modification: codestyle
- build: dependency update
- modification: docstyle
- modification(tests): update conversion testset
- modification: delete conversion in schema
- modification: store etree from string
- bugfix: default access
- modification:  convert marc21 xml string
- bugfix: docstring was wrong
- rewrite: changed the details part of the landing page to one column
- bugfix: get from variable after check variable not none
- bugfix: title could be not a string, be careful
- bugfix: not present variable cause page rendering fault
- modification: empty subfields
- modifcation: save draft
- bugfix(ui): dump empty subfields
- modification: deepcopy metadata
- tests: resource serializer
- modification(resources): serializer xml metadata
- bugfix(ui): record publisher
- modification(tests): serializer xml
- build(ui): dependency update
- feature: add AccessRightField
- modification: dump marc21 metadata as string
- modification: title deposit page
- modification: deposit_config default parameter
- modification: deserialize default metadata
- bugfix: typo record api links
- feature: deposit edit view
- bugfix(ui): record exporter page
- improvement: not use records_version from invenio-rdm-records
- bugfix: not updated the check, after updating the output key
- modification(ui): change sidebar
- bugfix: access protection to record
- modification: add landing page react component
- modification: sidebar landing page
- modification: build assets marc21 landingpage
- feature: marc21 records version
- fix tests
- add functionality to set a pre-calculated marcid
- bugfix: the shown version number on the landing page was wrong
- codestyle:change variable name
- modification:  translations
- codestyle: prettier for less files
- modification: change html code
- modification: record author
- modification: landing page
- modification: update translation strings
- modification: move string wrapper to own file
- modification: codestyle
- modification: update translations
- feature: personal name filter
- modification: remove unwanted details
- build: remove unnaccessary dependencies
- modification: stylesheet
- modification: update translation strings
- modification: landing page title
- modification: landing page details
- feature: summary section
- docs: modify documentation
- docs: modify marc21 service documentation
- bugfix: typehints breaks autodocs
- bugfix:  initialize Marc21Record to RecordFile
- docs: update invenio-records-marc21 documentation
- tests: record protection
- modification: codestyle update
- modification: FieldsPermissionMixin
- modification: record schema
- modification: enable files support in services
- feature: add filepreviewer
- codestyle: imporve code quality
- modification: remove __versioned__ in models
- bugfix: init files service in registry
- tests: diable files
- modification: disable file support
- bugfix: lambda function remove
- bugfix: on publish get files from draft
- codestyle: prettify jsavascript
- codestyle: format code
- build: reducing ci build time
- modification: update testset
- modification: update record acces schema
- bugfix: pycodestyle
- bugfix: add missing manifest entry
- feature:  init depsit app
- feature: deposit app
- modification: webpaclk update
- modification: create backend links
- modification: template service
- feature: template service
- modification: loading record
- modification: init subfield
- modification: leader field from string
- feature: load etree metadata
- style:  codestyle
- test: reduce fixture calls
- test(metadata): metadata schema
- modification: codestyle
- test(metadata): metadata structure
- modification: metadata  ui presentation
- modification: metadata field in ui
- modification: codestyle
- modification: metadata  field
- modification(ui): export record using pid_value
- modification(ui): marc21 file service
- bugfix(service): file service links
- modification(ui): decorator resolve record
- CI: build errors
- modification: use  newer postgresql versions
- modification: subjects listing
- test(services): create records
- modification: message box color
- modification: access status to search result
- test(serializer): test-set
- modification: doc string class name
- modification: add links to record
- modification: record pages
- modification: update record endpoints
- modification: serializer config
- feature: marc21 record serializers
- modification: marc21 record ui schema
- modification: metadata schema
- modification: exception handling
- build: update manifest
- test: invenio cli create demo records test set
- feature: display error message
- modification: remove comments
- modification: rename private service  function
- build: add celery dependency
- modification: config celery tasks
- tests: add service lift embargo
- feature: celery task lift embargo
- feature: service lift embargo
- feature: add record check_draft field
- test: service schemas
- modification: AccessSchema
- bugfix: protection string
- test: add parent fixture
- test: pid field test-set
- modification: move systemfield test-set
- test: access component
- bugfix: correct import AccessStatusEnum
- test: update embargo
- bugfix: embargo date in the future
- modification: date modification
- test: test-set for access component
- feature: set access property
- modification: moved access status enum
- feature:  add access systemfield
- modification: update parent access shema
- bugfix: use explicit record models
- build: update dependencies
- modification: update imports
- build: update dependencies
- refactor: update ES mapping
- bugfix: lxml  parsetree adds xmlns to tag name
- modification: rename metadata functions
- modification: update manifest
- tests(Marc21Metadata): add Marc21Metadata testset
- refactor(Marc21Metadata): import Marc21Metadata
- build(setup): add lxml module dependency
- modification: marc21 metadata
- bugfix(search): update record search  config
- build: update dependencies versions
- style: rupdate formatting
- tests: update tests to new record structure
- modification: validate embargo present
- modification: update resources
- bugfix: import external modules
- modification: build api endpoints
- modification: clean up unused code
- modification(tests): update root keys
- bugfix:  fields marshmallow instead of marshmallow_utils
- modification(tests): tests clean up
- modification: remove component file
- bugfix(tests): using local jsonschema resolver
- modification: removing unused vocabulary functions
- bugfix(test): removing conceptid in testset
- modification: add parent schema to init file
- bugfix: move record file below record
- modification: move acces schema for marc21 records
- tests: update access schema testset
- modification: update schema access testset
- modification: removing vocabularies in module
- build(setup): update dependencies
- modification: update services in ext
- modification: removing new_version in MetadataComponent
- modification: schemas
- modification: update service
- modification: update db models
- modification: introducing parent record schema
- modification: move record components
- modification: jsonschemas update
- modification adding js file to manifest
- modification: codestyle
- feature: add search engine
- modification: adding json export
- bugfix: show link shema in the record
- modification: moving ui records
- modification: changes translation string
- modification: adding german translation strings
- modification: add welcome string to translation
- modification: no blank lines after docstring
- feature: update language files
- modification: updates semantic ui tags
- modification: codestyle
- feature: export record
- modification: convert datetime to format
- modification: homogenous config names
- modification: finalize record presentation
- modification: codestyle
- modification: add marc21 filters
- modification: provide a example record
- feature: record landing page
- refactor: update record landing page
- refactor: create a module index page
- refactor: codestyle
- build: modify entry_points change ui presentation entypoint to added ui presentation module
- feature: jinia templates
- feature: record presentation
- refactor: module config
- feature: current record proxy


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
