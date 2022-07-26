// This file is part of Invenio.
//
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { useState } from "react";
import ReactDOM from "react-dom";
import _camelCase from "lodash/camelCase";
import _truncate from "lodash/truncate";
import {
  Button,
  Card,
  Checkbox,
  Icon,
  Input,
  Item,
  Label,
  List,
} from "semantic-ui-react";
import { BucketAggregation } from "react-searchkit";
import _get from "lodash/get";
import { loadComponents } from "@js/invenio_theme/templates";
import Overridable from "react-overridable";
import { SearchBar, SearchApp } from "@js/invenio_search_ui/components";

export const Marc21RecordResultsListItem = ({ result, index }) => {
  const createdDate = _get(result, "ui.created", "No creation date found.");

  const publicationDate = _get(result, "ui.updated", "No update date found.");
  const access = _get(result, ["ui", "access_status"], []);

  const access_id = _get(access, "id", "public");
  const access_status = _get(access, "title", "Public");
  const access_icon = _get(access, "icon", "unlock");

  const metadata = _get(result, ["ui", "metadata"], []);
  const description = _get(metadata, ["summary", "summary"], "No description");
  const subjects = _get(metadata, "subject_added_entry_topical_term", []);

  const publication = _get(
    metadata,
    ["production_publication_distribution_manufacture_and_copyright_notice"],
    []
  );
  const creators = _get(
    publication,
    "name_of_producer_publisher_distributor_manufacturer",
    []
  );

  const title = _get(metadata, ["title_statement", "title"], "No title");
  const version = _get(result, "revision_id", null);

  const viewLink = `/marc21/${result.id}`;

  return (
    <Item key={index} href={viewLink}>
      <Item.Content>
        <Item.Extra>
          <div>
            <Label size="tiny" color="blue">
              {publicationDate} {version ? `(${version})` : null}
            </Label>
            <Label size="tiny" className={`access-status ${access_id}`}>
              {access_icon && <i className={`icon ${access_icon}`}></i>}
              {access_status}
            </Label>
            <Button basic floated="right">
              <Icon name="eye" />
              View
            </Button>
          </div>
        </Item.Extra>
        <Item.Header>{title}</Item.Header>
        <Item.Meta>
          {creators.map((creator, index) => (
            <span key={index}>
              {creator}
              {index < creators.length - 1 && ","}
            </span>
          ))}
        </Item.Meta>
        <Item.Description>
          {_truncate(description, { length: 350 })}
        </Item.Description>
        <Item.Extra>
          {subjects.map((subject, index) => (
            <Label key={index} size="tiny">
              {subject.miscellaneous_information}
            </Label>
          ))}
          {createdDate && (
            <div>
              <small>
                Uploaded on <span>{createdDate}</span>
              </small>
            </div>
          )}
        </Item.Extra>
      </Item.Content>
    </Item>
  );
};

export const Marc21RecordResultsGridItem = ({ result, index }) => {
  const metadata = _get(result, ["ui", "metadata", "json"], []);
  const description = _get(
    metadata,
    ["summary", "0", "summary"],
    "No description"
  );
  return (
    <Card fluid key={index} href={`/marc21/${result.pid}`}>
      <Card.Content>
        <Card.Header>{result.metadata.json.title_statement.title}</Card.Header>
        <Card.Description>
          {_truncate(description, { length: 200 })}
        </Card.Description>
      </Card.Content>
    </Card>
  );
};
