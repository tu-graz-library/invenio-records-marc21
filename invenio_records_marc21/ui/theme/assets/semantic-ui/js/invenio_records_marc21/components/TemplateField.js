/*
 * SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { FastField } from "formik";
import { FieldLabel } from "react-invenio-forms";
import { Card, Form, Button } from "semantic-ui-react";

class TemplateFieldComponent extends Component {
  constructor(props) {
    super(props);
    this.formik = props.formik;
  }

  setTemplate(template) {
    let values = this.formik.form.values;
    values.metadata = template.metadata;
    this.formik.form.setValues(values);
  }

  render() {
    const { fieldPath, templates, label, labelIcon } = this.props;
    return (
      <Card className="templates">
        <Card.Content>
          <Form.Field>
            <FieldLabel
              htmlFor={`${fieldPath}.template`}
              icon={labelIcon}
              label={label}
            />

            {templates.map((value, index) => {
              const arrayPath = fieldPath;
              const indexPath = index;
              const key = `${arrayPath}.${indexPath}`;
              return (
                <Button
                  key={key}
                  onClick={() => this.setTemplate(value.values)}
                  index={index}
                  fluid
                >
                  {value.name}
                </Button>
              );
            })}
          </Form.Field>
        </Card.Content>
      </Card>
    );
  }
}

class FormikTemplateField extends Component {
  render() {
    const { fieldPath } = this.props;

    return (
      <FastField
        name={fieldPath}
        component={(formikProps) => (
          <TemplateFieldComponent formik={formikProps} {...this.props} />
        )}
      />
    );
  }
}

var TemplateJson = PropTypes.shape({
  active: PropTypes.string,
  name: PropTypes.string.isRequired,
  values: PropTypes.object.isRequired,
  created_at: PropTypes.string,
});

FormikTemplateField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  labelIcon: PropTypes.string,
  templates: PropTypes.arrayOf(TemplateJson.isRequired).isRequired,
};

FormikTemplateField.defaultProps = {
  fieldPath: "template",
};

const mapStateToProps = (state) => ({});

export const TemplateField = connect(
  mapStateToProps,
  null,
)(FormikTemplateField);
