// This file is part of Invenio.
//
// Copyright (C) 2021-2024 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { useState } from "react";
import { truncate, get } from "lodash";
import { Button, Item, Label } from "semantic-ui-react";
import { EditButton } from "@js/invenio_records_marc21/components/EditButton";
import { i18next } from "@translations/invenio_records_marc21/i18next";
import { Marc21Stats } from "./Marc21Stats";

export const Marc21RecordResultsListItem = ({ dashboard, result, index }) => {
  const version = get(result, "revision_id", null);

  const createdDate = get(result, "ui.created", "No creation date found");
  const publicationDate = get(result, "ui.updated", "No update date found");

  const access_id = get(result, "ui.access_status.id", "open");
  const access_status = get(result, "ui.access_status.title_l10n", "Open");
  const access_icon = get(result, "ui.access_status.icon", "unlock");

  const description = get(result, "ui.metadata.description", "No description");
  const subjects = get(result, "ui.metadata.subjects", []);

  const resource_type = get(result, "ui.metadata.resource_type", "");
  const creators = get(result, "ui.metadata.authors", []);
  const titles = get(result, "ui.metadata.titles", ["No titles"]);
  const is_published = get(result, "is_published", true);

  const uniqueViews = get(result, "stats.all_versions.unique_views", 0);
  const uniqueDownloads = get(result, "stats.all_versions.unique_downloads", 0);

  const copyright = get(result, "ui.metadata.copyright", []);
  let published_at = null;
  if (copyright.length > 0) {
    published_at = get(copyright[0], "subfields.c", null);
  }
  let viewLink = `/publications/${result.id}`;
  if (!is_published) {
    viewLink = `/publications/uploads/${result.id}`;
  }


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
              {published_at ? `${published_at}` : publicationDate}
              {version ? `(${version})` : null}
            </Label>
            <Label size="tiny" className={`access-status ${access_id}`}>
              {access_icon && <i className={`icon ${access_icon}`}></i>}
              {access_status}
            </Label>
            {resource_type && (
              <Label size="tiny" color="blue">
                {resource_type}
              </Label>
            )}
            {dashboard && (
              <>
                <EditButton recid={result.id} onError={handleError} />
                <Button
                  basic
                  compact
                  size="small"
                  floated="right"
                  icon="eye"
                  content={i18next.t("View")}
                  href={viewLink}
                />
              </>
            )}
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

          <div className="flex justify-space-between align-items-end">
            {createdDate && (
              <small>
                {i18next.t("Uploaded on")} <span>{createdDate}</span>
              </small>
            )}
            <small>
              <Marc21Stats
                uniqueViews={uniqueViews}
                uniqueDownloads={uniqueDownloads}
              />
            </small>
          </div>
        </Item.Extra>
      </Item.Content>
    </Item>
  );
};
