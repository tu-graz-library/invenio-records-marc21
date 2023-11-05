// This file is part of Invenio.
//
// Copyright (C) 2023 Graz University of Technology.
//
// Invenio-Records-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.
import { Card } from "semantic-ui-react";
import React from "react";
import _get from "lodash/get";
import _truncate from "lodash/truncate";

export const Marc21RecordResultsGridItem = ({ result, index }) => {
  const metadata = _get(result, ["ui", "metadata", "json"], []);
  const description = _get(
    metadata,
    ["summary", "0", "summary"],
    "No description"
  );
  return (
    <Card fluid key={index} href={`/publications/${result.pid}`}>
      <Card.Content>
        <Card.Header>{result.metadata.json.title_statement.title}</Card.Header>
        <Card.Description>
          {_truncate(description, { length: 200 })}
        </Card.Description>
      </Card.Content>
    </Card>
  );
};
