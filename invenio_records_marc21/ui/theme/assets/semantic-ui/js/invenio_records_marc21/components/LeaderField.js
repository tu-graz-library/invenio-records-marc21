// This file is part of Invenio.
//
// Copyright (C) 2021-2022 Graz University of Technology.
//
// React-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { Component } from "react";
import PropTypes from "prop-types";

import { TextField } from "react-invenio-forms";

export class LeaderField extends Component {
  render() {
    const { fieldPath } = this.props;
    return (
      <>
        <TextField
          fieldPath={`ldr`}
          value={"LDR"}
          width={3}
          className={"key narrow"}
          disabled
        />
        <TextField
          fieldPath={`${fieldPath}`}
          width={15}
          required
          maxLength={24}
          className={"narrow"}
        />
      </>
    );
  }
}

LeaderField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  helpText: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
};

LeaderField.defaultProps = {
  helpText: "",
};
