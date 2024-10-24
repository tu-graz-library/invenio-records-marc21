// This file is part of Invenio.
//
// Copyright (C) 2021-2024 Graz University of Technology.
//
// React-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import { set, get} from "lodash";
import { DepositRecordSerializer } from "@js/invenio_rdm_records";

export class Marc21RecordSerializer extends DepositRecordSerializer {
  constructor(defaultLocale) {
    super();
    this.defaultLocale = defaultLocale;
    this.current_record = {};
  }

  /**
   * Deserialize backend record into format compatible with frontend.
   * @method
   * @param {object} record - potentially empty object
   * @returns {object} frontend compatible record object
   */
  deserialize(record) {
    this.current_record = record;
    return record;
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
          let fields = get(this.current_record, "metadata.fields");
          const field = keys[2];
          let j = 0;
          while (j < fields.length) {
            if (field == fields[j].id) {
              set(
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
        set(deserializedErrors, e.field, e.messages.join(" "));
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
    return record;
  }
}
