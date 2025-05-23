// This file is part of Invenio.
//
// Copyright (C) 2020-2021 CERN.
// Copyright (C) 2020-2021 Northwestern University.
// Copyright (C) 2021-2024 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import axios from "axios";
import { get } from "lodash";
import React, { useEffect, useState } from "react";
import { Divider, Grid, Icon, Message, Placeholder } from "semantic-ui-react";
import { i18next } from "@translations/invenio_records_marc21/i18next";

const deserializeRecord = (record) => ({
  id: record.id,
  parent_id: record.parent.id,
  publication_date: record.ui.publication_date_l10n_medium,
  version: record.ui.version,
  links: record.links,
  pids: record.pids,
});

const NUMBER_OF_VERSIONS = 5;

const RecordVersionItem = ({ item, activeVersion }) => {
  const doi = get(item.pids, "pk", "");
  return (
    <>
      <Grid.Row
        key={item.id}
        columns={1}
        {...(activeVersion && { className: "version-active" })}
      >
        <Grid.Column>
          <small className="text-muted" style={{ float: "right" }}>
            {item.publication_date}
          </small>
          <a href={`/publications/${item.id}`}>
            {i18next.t("Version")} {item.version}
          </a>
          {<br />}
          {doi && (
            <small className="text-muted" style={{ wordWrap: "break-word" }}>
              {doi}
            </small>
          )}
        </Grid.Column>
      </Grid.Row>
      <Divider fitted style={{ margin: "0" }} />
    </>
  );
};

const PlaceholderLoader = ({ size = NUMBER_OF_VERSIONS }) => {
  const PlaceholderItem = () => (
    <Placeholder.Header>
      <Placeholder.Line />
      <Placeholder.Line />
    </Placeholder.Header>
  );
  let numberOfHeader = [];
  for (let i = 0; i < size; i++) {
    numberOfHeader.push(<PlaceholderItem key={i} />);
  }

  return <Placeholder>{numberOfHeader}</Placeholder>;
};

const PreviewMessage = () => {
  return (
    <Grid.Row>
      <Grid.Column className="versions-preview-info">
        <Message info>
          <Message.Header>
            <Icon name="eye" />
            {i18next.t("Preview")}
          </Message.Header>
          <p>{i18next.t("Only published versions are displayed.")}</p>
        </Message>
      </Grid.Column>
    </Grid.Row>
  );
};

export const RecordVersionsList = (props) => {
  const record = deserializeRecord(props.record);
  const { isPreview } = props;
  const recid = record.id;
  const [loading, setLoading] = useState(true);
  const [currentRecordInResults, setCurrentRecordInResults] = useState(false);
  const [recordVersions, setRecordVersions] = useState({});

  useEffect(() => {
    async function fetchVersions() {
      const result = await axios(
        `${record.links.versions}?size=${NUMBER_OF_VERSIONS}&sort=version&allversions=true`,
        {
          headers: {
            Accept: "application/vnd.inveniomarc21.v1+json",
          },
          withCredentials: true,
        }
      );
      let { hits, total } = result.data.hits;
      hits = hits.map(deserializeRecord);
      setCurrentRecordInResults(hits.some((record) => record.id === recid));
      setRecordVersions({ hits, total });
      setLoading(false);
    }
    fetchVersions();
  }, []);

  return loading ? (
    <>{isPreview ? <PreviewMessage /> : <PlaceholderLoader />}</>
  ) : (
    <Grid padded>
      {isPreview ? <PreviewMessage /> : null}
      {recordVersions.hits.map((item) => (
        <RecordVersionItem
          key={item.id}
          item={item}
          activeVersion={item.id === recid}
        />
      ))}
      {!currentRecordInResults && (
        <>
          <Grid.Row centered>...</Grid.Row>
          <RecordVersionItem item={record} activeVersion={true} />
        </>
      )}
      <Grid.Row centered>
        <a
          href={`/publications/search?q=parent.id:${record.parent_id}&sort=version&f=allversions:true`}
          target="_blank"
          className="font-small"
        >
          {`View all ` + recordVersions.total + ` versions`}
        </a>
      </Grid.Row>
    </Grid>
  );
};
