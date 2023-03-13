// This file is part of Invenio.
//
// Copyright (C) 2021-2023 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { useState } from "react";
import { truncate, get } from "lodash";
import { Button, Card, Item, Label } from "semantic-ui-react";
import { EditButton } from "../components/EditButton";
import { i18next } from "@translations/invenio_records_marc21/i18next";

export const Marc21RecordResultsListItem = ({ result, index }) => {
  const version = get(result, "revision_id", null);

  const createdDate = get(result, "ui.created", "No creation date found");
  const publicationDate = get(result, "ui.updated", "No update date found");

  const access_id = get(result, "ui.access_status.id", "public");
  const access_status = get(result, "ui.access_status.title", "Public");
  const access_icon = get(result, "ui.access_status.icon", "unlock");

  const description = get(result, "ui.metadata.description", "No description");
  const subjects = get(result, "ui.metadata.subjects", []);
  const creators = get(result, "ui.metadata.authors", []);
  const titles = get(result, "ui.metadata.titles", ["No titles"]);

  const viewLink = `/marc21/${result.id}`;

  const [error, setError] = useState("");

  const handleError = (errorMessage) => {
    console.error(errorMessage);
    setError(errorMessage);
  };

  return (
    <Item key={index}>
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
            <EditButton recid={result.id} onError={handleError} />
            <Button
              basic
              compact
              size="small"
              floated="right"
              icon="eye"
              content={i18next.t("View")}
            />
          </div>
        </Item.Extra>
        <Item.Header href={viewLink}>
          {titles.map((title) => (
            <span>{title}</span>
          ))}
        </Item.Header>
        <Item.Meta>
          {creators.map((creator, index) => (
            <span key={index}>
              {creator.a}
              {index < creators.length - 1 && ","}
            </span>
          ))}
        </Item.Meta>
        <Item.Description>
          {truncate(description, { length: 350 })}
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
  const metadata = get(result, ["ui", "metadata", "json"], []);
  const description = get(
    metadata,
    ["summary", "0", "summary"],
    "No description"
  );
  return (
    <Card fluid key={index} href={`/marc21/${result.pid}`}>
      <Card.Content>
        <Card.Header>{result.metadata.json.title_statement.title}</Card.Header>
        <Card.Description>
          {truncate(description, { length: 200 })}
        </Card.Description>
      </Card.Content>
    </Card>
  );
};
