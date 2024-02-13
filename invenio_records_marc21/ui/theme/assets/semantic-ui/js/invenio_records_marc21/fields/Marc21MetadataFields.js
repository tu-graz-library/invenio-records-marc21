// This file is part of Invenio.
//
// Copyright (C) 2021-2024 Graz University of Technology.
//
// React-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import _get from "lodash/get";
import _set from "lodash/set";
import _cloneDeep from "lodash/cloneDeep";
import _pick from "lodash/pick";
import _has from "lodash/has";

import { Field } from "./Field";

const { Marc, Record } = require("marcjs");

export class Marc21MetadataFields extends Field {
  controlfields = ["001", "003", "005", "006", "007", "008", "009"];
  constructor({ fieldpath, deserializedDefault = [], serializedDefault = [] }) {
    super({ fieldpath, deserializedDefault, serializedDefault });
  }

  /**
   * Compare Metadata field order for sorting in frontend.
   * @method
   * @param {object} field1 - first field to compare
   * @returns {object} field1 -  second field to compare
   */
  compare(field1, field2) {
    if (field1.id < field2.id) {
      return -1;
    }
    if (field1.id > field2.id) {
      return 1;
    }
    return 0;
  }

  /**
   * Deserialize backend record into format compatible with frontend.
   * @method
   * @param {object} record - potentially empty object
   * @returns {object} frontend compatible record object
   */
  deserialize(record) {
    let deserializedRecord = record;
    deserializedRecord = _pick(deserializedRecord, [
      "metadata",
      "id",
      "links",
      "files",
      "pids",
    ]);
    for (let key in this.depositRecordSchema) {
      deserializedRecord = this.depositRecordSchema[key].deserialize(
        deserializedRecord,
        this.defaultLocale
      );
    }
    return deserializedRecord;
  }

  static _deserialize_subfields(subfields) {
    let field = "";
    subfields.forEach((subfield) => {
      for (const [key, value] of Object.entries(subfield)) {
        field += " $$" + key + " " + value;
      }
    });
    return field;
  }

  _deserialize_fields(fields) {
    let metadata = [];
    for (const field of Object.values(fields)) {
      const key = Object.keys(field)[0];
      const value = Object.values(field)[0];
      let subfields = value;
      if (!this.controlfields.includes(key)) {
        subfields = Marc21MetadataFields._deserialize_subfields(
          value["subfields"]
        );
      }
      let internal = {
        id: key,
        ind1: value["ind1"],
        ind2: value["ind2"],
        subfield: subfields,
      };
      metadata.push(internal);
    }
    return metadata;
  }

  /**
   * Deserialize backend field into format compatible with frontend using
   * the given schema.
   * @method
   * @param {object} element - potentially empty object
   * @returns {object} frontend compatible element object
   */
  deserialize(record) {
    record = _cloneDeep(record);

    let marcxml = _get(record, this.fieldpath);

    let record_dict;

    if (marcxml != null) {
      const marcjs = Marc.parse(marcxml, "marcxml");
      record_dict = marcjs.mij();
      record_dict.fields = this._deserialize_fields(record_dict.fields);
      record_dict.fields.sort(this.compare);
    } else {
      record_dict = this.deserializedDefault;
    }

    return _set(record, this.fieldpath, record_dict);
  }

  static _serialize_subfields(subfields) {
    let fields = [];
    subfields = subfields.trim();
    const subfield_list = subfields.split("$$").filter(String);

    for (let i = 0; i < subfield_list.length; i++) {
      const subfield = subfield_list[i].split(" ");
      fields = fields.concat([subfield[0], subfield.slice(1).join(" ").trim()]);
    }
    return fields;
  }

  _serialize_fields(marc_record, fields) {
    let metadata = [];
    for (const field of Object.values(fields)) {
      let internal;

      if (this.controlfields.includes(field["id"])) {
        internal = [field["id"], field["subfield"]];
      } else {
        const subfields = Marc21MetadataFields._serialize_subfields(
          field["subfield"]
        );
        const ind1 = field.ind1?.replace(" ", "_");
        const ind2 = field.ind2?.replace(" ", "_");
        internal = [field["id"], ind1 + ind2].concat(subfields);
      }

      marc_record.append(internal);
    }
    return metadata;
  }

  /**
   * Serialize element to send to the backend.
   * @method
   * @param {object} element - in frontend format
   * @returns {object} element - in API format
   *
   */
  serialize(record) {
    let record_dict = _get(record, this.fieldpath, this.serializedDefault);
    let metadata = new Record();
    if (_has(record_dict, ["leader"])) {
      metadata.leader = record_dict.leader;
    } else {
      metadata.leader = "";
    }
    if (_has(record_dict, ["fields"])) {
      record_dict.fields = this._serialize_fields(metadata, record_dict.fields);
    }
    const marcxml = metadata.as("marcxml");

    return _set(_cloneDeep(record), this.fieldpath, marcxml);
  }
}
