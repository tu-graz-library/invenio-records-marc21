// This file is part of Invenio.
//
// Copyright (C) 2021-2023 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import _get from "lodash/get";
import { i18next } from "@translations/invenio_records_marc21/i18next";
import React, { Component, createRef } from "react";
import {
  Marc21RecordSerializer,
  MetadataFields,
  TemplateField,
} from "@js/invenio_records_marc21/components";
import { AccordionField } from "react-invenio-forms";
import { Card, Container, Grid, Ref, Sticky } from "semantic-ui-react";
import {
  AccessRightField,
  FileUploader,
  SaveButton,
  PublishButton,
  PreviewButton,
  DepositFormApp,
  FormFeedback,
  DeleteButton,
  DepositStatusBox,
} from "@js/invenio_rdm_records";
import PropTypes from "prop-types";

export class Marc21DepositForm extends Component {
  accordionStyle = {
    header: { className: "segment inverted brand" },
  };

  sidebarRef = createRef();

  constructor(props) {
    super(props);
    const { files, record } = this.props;
    this.props = props;
    this.config = props.config || {};
    this.templates = props.templates || [];
    this.files = props.files;
    this.recordSerializer = new Marc21RecordSerializer();

    this.noFiles = false;
    if (
      !Array.isArray(files.entries) ||
      (!files.entries.length && record.is_published)
    ) {
      this.noFiles = true;
    }
  }

  render() {
    const { record, files, permissions, preselectedCommunity } = this.props;
    return (
      <DepositFormApp
        config={this.config}
        record={record}
        preselectedCommunity={preselectedCommunity}
        files={files}
        permissions={permissions}
        recordSerializer={this.recordSerializer}
      >
        <FormFeedback fieldPath="message" />
        <Container style={{ marginTop: "10px" }}>
          <Grid>
            <Grid.Row>
              <Grid.Column mobile={16} tablet={16} computer={11}>
                <AccordionField
                  includesPaths={["files.enabled"]}
                  active
                  label={i18next.t("Files")}
                >
                  {this.noFiles && record.is_published && (
                    <div className="text-align-center pb-10">
                      <em>{i18next.t("The record has no files.")}</em>
                    </div>
                  )}
                  <FileUploader
                    isDraftRecord={!record.is_published}
                    quota={this.config.quota}
                    decimalSizeDisplay={this.config.decimal_size_display}
                  />
                </AccordionField>

                <AccordionField
                  includesPaths={["metadata.leader", "metadata.fields"]}
                  active
                  label={i18next.t("Metadata")}
                >
                  <MetadataFields className={"metadata"} fieldPath="metadata" />
                </AccordionField>
              </Grid.Column>
              {/* Sidebar start */}
              <Ref innerRef={this.sidebarRef}>
                <Grid.Column
                  mobile={16}
                  tablet={16}
                  computer={5}
                  className="deposit-sidebar"
                >
                  <Sticky context={this.sidebarRef} offset={20}>
                    <Card>
                      <Card.Content>
                        <DepositStatusBox />
                      </Card.Content>
                      <Card.Content>
                        <Grid relaxed>
                          <Grid.Column
                            computer={8}
                            mobile={16}
                            className="pb-0 left-btn-col"
                          >
                            <SaveButton fluid />
                          </Grid.Column>

                          <Grid.Column
                            computer={8}
                            mobile={16}
                            className="pb-0 right-btn-col"
                          >
                            <PreviewButton fluid type="submit" />
                          </Grid.Column>

                          <Grid.Column width={16} className="pt-10">
                            <PublishButton fluid type="submit" />
                          </Grid.Column>
                        </Grid>
                      </Card.Content>
                    </Card>
                  </Sticky>

                  <Sticky context={this.sidebarRef} offset={10}>
                    {this.templates.length > 0 && (
                      <TemplateField
                        label={i18next.t("Templates")}
                        labelIcon={"bookmark"}
                        templates={this.templates}
                      />
                    )}
                  </Sticky>
                  <AccessRightField
                    label={i18next.t("Visibility")}
                    labelIcon="shield"
                    fieldPath="access"
                  />
                  {permissions?.can_delete_draft && (
                    <Card>
                      <Card.Content>
                        <DeleteButton
                          fluid
                          // TODO: make is_published part of the API response
                          //       so we don't have to do this
                          isPublished={record.is_published}
                        />
                      </Card.Content>
                    </Card>
                  )}
                </Grid.Column>
              </Ref>
            </Grid.Row>
          </Grid>
        </Container>
      </DepositFormApp>
    );
  }
}

DepositFormApp.propTypes = {
  config: PropTypes.object.isRequired,
  record: PropTypes.object.isRequired,
  preselectedCommunity: PropTypes.object,
  files: PropTypes.object,
  permissions: PropTypes.object,
};

DepositFormApp.defaultProps = {
  preselectedCommunity: undefined,
  permissions: null,
  files: null,
};
