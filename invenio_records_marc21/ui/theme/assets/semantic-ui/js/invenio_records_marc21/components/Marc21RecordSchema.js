// This file is part of Invenio.
//
// Copyright (C) 2021-2024 Graz University of Technology.
//
// React-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import { has, get } from "lodash";
import axios from "axios";

export class Marc21RecordSchema {
  /**
   *  Make sure RecordSchema called first time with props.link
   */

  constructor(link, schema) {
    this.schema = {};
    this.link = link;
    this.leader_field = "LDR";
    this.loaded = schema !== {};

    if (this.loaded) {
      this.setSchema(schema);
    }
  }

  isReady() {
    return this.loaded;
  }

  setSchema(schema) {
    this.schema = schema;
  }

  loadSchema() {
    axios.get(this.state.link).then(
      (result) => {
        this.loaded = true;
        this.schema = result.data;
      },
      // Note: it's important to handle errors here
      // instead of a catch() block so that we don't swallow
      // exceptions from actual bugs in components.
      (error) => {
        this.loaded = false;
        this.schema = {};
        this.error = error;
      }
    );
  }

  isLeaderField(key) {
    let keys = this.getLeaderFieldKeys();
    return keys.includes(key);
  }

  isDataField(key) {
    let keys = this.getDataFieldKeys();
    return keys.includes(key);
  }

  hasLeaderKey(key) {
    return has(this.schema, ["fields", this.leader_field, "positions", key]);
  }

  getLeaderFieldKeys() {
    let fields = this.getLeaderFields();
    let keys = [];
    for (const [key, value] of Object.entries(fields)) {
      keys.push(key);
    }
    return keys;
  }

  getLeaderFields() {
    return get(this.schema, ["fields", this.leader_field, "positions"], {});
  }

  getLeaderField(key) {
    const leaderfields = this.getLeaderFields();
    return leaderfields[key];
  }

  getLeaderFieldOptions(key) {
    const leaderfield = this.getLeaderField(key);
    const leaderfield_codes = get(leaderfield, ["codes"], {});
    let codes = this.generateDropdownOptions(leaderfield_codes);
    return codes;
  }

  getDataFields() {
    return get(this.schema, ["fields"], {});
  }

  getDataFieldKeys() {
    let fields = this.getDataFields();
    let keys = [];
    for (const [key, value] of Object.entries(fields)) {
      keys.push(key);
    }
    return keys;
  }

  getDataField(key) {
    const datafield = this.getDataFields();
    return datafield[key];
  }

  generateDropdownOptions(fields) {
    let codes = [];
    for (const [key, value] of Object.entries(fields)) {
      let code = { key: key, label: key, value: key, text: value["label"] };
      codes.push(code);
    }
    return codes;
  }

  /**
   * Finds tag and indicator position select options
   *
   * @param {string} key - tag key name
   * @param {string} ind - indicator key name
   */
  getDataFieldOptions(key, ind) {
    let codes = [];
    const datafield = this.getDataField(key);
    if (datafield[ind] === null) {
      return codes;
    }
    const datafield_codes = datafield[ind]["codes"];
    codes = this.generateDropdownOptions(datafield_codes);

    return codes;
  }
}
