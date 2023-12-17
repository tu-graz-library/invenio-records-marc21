// This file is part of Invenio.
//
// Copyright (C) 2021-2022 Graz University of Technology.
//
// React-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

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

            {templates.map((value, index, array) => {
              const arrayPath = fieldPath;
              const indexPath = index;
              const key = `${arrayPath}.${indexPath}`;
              return (
                <>
                  <Button
                    key={key}
                    onClick={() => this.setTemplate(value.values)}
                    index={index}
                    fluid
                  >
                    {value.name}
                  </Button>
                </>
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
    return (
      <FastField
        name={this.props.fieldPath}
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

export const TemplateField = connect(mapStateToProps, null)(FormikTemplateField);
