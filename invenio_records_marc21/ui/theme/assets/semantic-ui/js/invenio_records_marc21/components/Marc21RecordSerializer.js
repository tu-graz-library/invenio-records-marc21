// This file is part of Invenio.
//
// Copyright (C) 2021-2023 Graz University of Technology.
//
// React-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import _cloneDeep from "lodash/cloneDeep";
import _defaults from "lodash/defaults";
import _pick from "lodash/pick";
import _set from "lodash/set";
import _get from "lodash/get";
import { DepositRecordSerializer } from "@js/invenio_rdm_records";
import { Field, Marc21MetadataFields } from "@js/invenio_records_marc21/fields";

export class Marc21RecordSerializer extends DepositRecordSerializer {
  constructor(defaultLocale) {
    super();
    this.defaultLocale = defaultLocale;
    this.current_record = {};
  }

  depositRecordSchema = {
    access: new Field({
      fieldpath: "access",
      deserializedDefault: {
        record: "public",
        files: "public",
      },
    }),
    files: new Field({
      fieldpath: "files",
    }),
    links: new Field({
      fieldpath: "links",
    }),
    parent: new Field({
      fieldpath: "parent",
    }),
    pids: new Field({
      fieldpath: "pids",
      deserializedDefault: {},
      serializedDefault: {},
    }),
    metadata: new Marc21MetadataFields({
      fieldpath: "metadata",
      deserializedDefault: { leader: "00000nam a2200000zca4500", fields: [] },
      serializedDefault: "",
    }),
  };

  /**
   * Deserialize backend record into format compatible with frontend.
   * @method
   * @param {object} record - potentially empty object
   * @returns {object} frontend compatible record object
   */
  deserialize(record) {
    record = _cloneDeep(record);

    let deserializedRecord = record;
    deserializedRecord = _pick(deserializedRecord, [
      "access",
      "expanded",
      "metadata",
      "id",
      "links",
      "files",
      "is_published",
      "versions",
      "parent",
      "status",
      "pids",
    ]);
    for (let key in this.depositRecordSchema) {
      deserializedRecord =
        this.depositRecordSchema[key].deserialize(deserializedRecord);
    }

    this.current_record = deserializedRecord;
    return deserializedRecord;
  }

  /**
   * Deserialize backend record errors into format compatible with frontend.
   * @method
   * @param {array} errors - array of error objects
   * @returns {object} - object representing errors
   */
  deserializeErrors(errors) {
    let deserializedErrors = {};
    for (const e of errors) {
      if (e.field.startsWith("metadata")) {
        let keys = e.field.split(".");
        if (keys[1] == "fields") {
          let fields = _get(this.current_record, "metadata.fields");
          const field = keys[2];
          let j = 0;
          while (j < fields.length) {
            if (field == fields[j].id) {
              _set(
                deserializedErrors,
                `metadata.fields.${j}.${keys[4]}`,
                e.messages.join(" ")
              );
              break;
            }
            j++;
          }
        }
      } else {
        _set(deserializedErrors, e.field, e.messages.join(" "));
      }
    }
    return deserializedErrors;
  }

  /**
   * Serialize record to send to the backend.
   * @method
   * @param {object} record - in frontend format
   * @returns {object} record - in API format
   *
   */
  serialize(record) {
    record = _cloneDeep(record);
    let serializedRecord = record; //this.removeEmptyValues(record);
    serializedRecord = _pick(serializedRecord, [
      "access",
      "metadata",
      "id",
      "links",
      "files",
      "pids",
      "parent",
    ]);
    for (let key in this.depositRecordSchema) {
      serializedRecord =
        this.depositRecordSchema[key].serialize(serializedRecord);
    }

    _defaults(serializedRecord, { metadata: {} });

    return serializedRecord;
  }
}
