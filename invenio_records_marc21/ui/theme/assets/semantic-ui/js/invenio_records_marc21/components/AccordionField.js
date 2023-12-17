// This file is part of Invenio.
//
// Copyright (C) 2021-2022 Graz University of Technology.
//
// React-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.
import React, { Component } from "react";
import PropTypes from "prop-types";
import { Field, FastField } from "formik";
import { Container, Icon, Segment } from "semantic-ui-react";

export class AccordionField extends Component {
  constructor(props) {
    super(props);
    this.state = { active: props.active || false };
  }

  iconActive = (<Icon name="angle down" size="large" style={{ float: "right" }} />);

  iconInactive = (<Icon name="angle right" size="large" style={{ float: "right" }} />);

  handleClick = (showContent) => {
    this.setState({ active: !showContent });
  };

  hasError(errors) {
    if (this.props.fieldPath in errors) {
      return true;
    }
    return false;
  }

  renderAccordion = (props) => {
    const {
      form: { errors, status },
    } = props;
    const { active } = this.state;
    const hasError = status ? this.hasError(status) : this.hasError(errors);

    return (
      <>
        <Segment
          onClick={() => this.handleClick(active)}
          {...(hasError && { ...this.props.ui?.error })}
          {...this.props.ui?.header}
        >
          <label>{this.props.label}</label>
          <span>{active ? this.iconActive : this.iconInactive}</span>
        </Segment>
        <Container {...this.props.ui?.content}>
          {active && this.props.children}
        </Container>
      </>
    );
  };

  render() {
    const FormikField = this.props.optimized ? FastField : Field;
    return <FormikField name={this.props.fieldPath} component={this.renderAccordion} />;
  }
}

AccordionField.propTypes = {
  active: PropTypes.bool,
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.string,
  required: PropTypes.bool,
  ui: PropTypes.shape({
    header: PropTypes.object,
    content: PropTypes.object,
    error: PropTypes.object,
  }),
  optimized: PropTypes.bool,
};

AccordionField.defaultProps = {
  active: false,
  label: "",
  required: false,
  ui: {
    error: { inverted: true, color: "red", secondary: true },
  },
  optimized: false,
};
