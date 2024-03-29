// This file is part of Invenio.
//
// Copyright (C) 2021-2022 Graz University of Technology.
//
// React-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import _get from "lodash/get";
import _set from "lodash/set";
import _cloneDeep from "lodash/cloneDeep";
export class Field {
  constructor({ fieldpath, deserializedDefault = null, serializedDefault = null }) {
    this.fieldpath = fieldpath;
    this.deserializedDefault = deserializedDefault;
    this.serializedDefault = serializedDefault;
  }

  deserialize(record) {
    let fieldValue = _get(record, this.fieldpath, this.deserializedDefault);
    if (fieldValue !== null) {
      return _set(_cloneDeep(record), this.fieldpath, fieldValue);
    }
    return record;
  }

  serialize(record) {
    let fieldValue = _get(record, this.fieldpath, this.serializedDefault);
    if (fieldValue !== null) {
      return _set(_cloneDeep(record), this.fieldpath, fieldValue);
    }
    return record;
  }
}
