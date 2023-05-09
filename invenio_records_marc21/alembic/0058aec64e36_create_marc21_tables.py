# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Create Marc21 Tables."""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0058aec64e36"
down_revision = "109d88c6310c"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "marc21_parents_metadata",
        sa.Column(
            "created",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_marc21_parents_metadata")),
    )
    op.create_table(
        "marc21_templates",
        sa.Column(
            "created",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column(
            "values",
            sa.JSON()
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_marc21_templates")),
        sa.UniqueConstraint("name", name=op.f("uq_marc21_templates_name")),
    )
    op.create_table(
        "marc21_drafts_metadata",
        sa.Column(
            "created",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column("index", sa.Integer(), nullable=True),
        sa.Column("fork_version_id", sa.Integer(), nullable=True),
        sa.Column(
            "expires_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column("bucket_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.Column("parent_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.ForeignKeyConstraint(
            ["bucket_id"],
            ["files_bucket.id"],
            name=op.f("fk_marc21_drafts_metadata_bucket_id_files_bucket"),
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["marc21_parents_metadata.id"],
            name=op.f("fk_marc21_drafts_metadata_parent_id_marc21_parents_metadata"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_marc21_drafts_metadata")),
    )
    op.create_table(
        "marc21_records_metadata",
        sa.Column(
            "created",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column("index", sa.Integer(), nullable=True),
        sa.Column("bucket_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.Column("parent_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.ForeignKeyConstraint(
            ["bucket_id"],
            ["files_bucket.id"],
            name=op.f("fk_marc21_records_metadata_bucket_id_files_bucket"),
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["marc21_parents_metadata.id"],
            name=op.f("fk_marc21_records_metadata_parent_id_marc21_parents_metadata"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_marc21_records_metadata")),
    )
    op.create_table(
        "marc21_drafts_files",
        sa.Column(
            "created",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column(
            "key",
            sa.Text(),
            nullable=False,
        ),
        sa.Column("record_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "object_version_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["object_version_id"],
            ["files_object.version_id"],
            name=op.f("fk_marc21_drafts_files_object_version_id_files_object"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["record_id"],
            ["marc21_drafts_metadata.id"],
            name=op.f("fk_marc21_drafts_files_record_id_marc21_drafts_metadata"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_marc21_drafts_files")),
    )
    op.create_index(
        "uidx_marc21_drafts_files_id_key",
        "marc21_drafts_files",
        ["id", "key"],
        unique=True,
    )
    op.create_table(
        "marc21_records_files",
        sa.Column(
            "created",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "json",
            sa.JSON()
            .with_variant(
                postgresql.JSONB(none_as_null=True, astext_type=sa.Text()), "postgresql"
            )
            .with_variant(sqlalchemy_utils.types.json.JSONType(), "sqlite"),
            nullable=True,
        ),
        sa.Column("version_id", sa.Integer(), nullable=False),
        sa.Column(
            "key",
            sa.Text(),
            nullable=False,
        ),
        sa.Column("record_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column(
            "object_version_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["object_version_id"],
            ["files_object.version_id"],
            name=op.f("fk_marc21_records_files_object_version_id_files_object"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["record_id"],
            ["marc21_records_metadata.id"],
            name=op.f("fk_marc21_records_files_record_id_marc21_records_metadata"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_marc21_records_files")),
    )
    op.create_index(
        "uidx_marc21_records_files_id_key",
        "marc21_records_files",
        ["id", "key"],
        unique=True,
    )
    op.create_table(
        "marc21_versions_state",
        sa.Column("latest_index", sa.Integer(), nullable=True),
        sa.Column("parent_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column("latest_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
        sa.Column(
            "next_draft_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["latest_id"],
            ["marc21_records_metadata.id"],
            name=op.f("fk_marc21_versions_state_latest_id_marc21_records_metadata"),
        ),
        sa.ForeignKeyConstraint(
            ["next_draft_id"],
            ["marc21_drafts_metadata.id"],
            name=op.f("fk_marc21_versions_state_next_draft_id_marc21_drafts_metadata"),
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["marc21_parents_metadata.id"],
            name=op.f("fk_marc21_versions_state_parent_id_marc21_parents_metadata"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("parent_id", name=op.f("pk_marc21_versions_state")),
    )
    op.drop_index(
        "ix_records_metadata_version_end_transaction_id",
        table_name="records_metadata_version",
    )
    op.drop_index(
        "ix_records_metadata_version_operation_type",
        table_name="records_metadata_version",
    )
    op.drop_index(
        "ix_records_metadata_version_transaction_id",
        table_name="records_metadata_version",
    )
    op.drop_table("records_metadata_version")
    op.drop_index("ix_uq_partial_files_object_is_head", table_name="files_object")
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        "ix_uq_partial_files_object_is_head",
        "files_object",
        ["bucket_id", "key"],
        unique=False,
    )
    op.create_table(
        "records_metadata_version",
        sa.Column(
            "created", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "updated", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column("id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "json",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("version_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("transaction_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column(
            "end_transaction_id", sa.BIGINT(), autoincrement=False, nullable=True
        ),
        sa.Column("operation_type", sa.SMALLINT(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint(
            "id", "transaction_id", name="pk_records_metadata_version"
        ),
    )
    op.create_index(
        "ix_records_metadata_version_transaction_id",
        "records_metadata_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_index(
        "ix_records_metadata_version_operation_type",
        "records_metadata_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        "ix_records_metadata_version_end_transaction_id",
        "records_metadata_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.drop_table("marc21_versions_state")
    op.drop_index("uidx_marc21_records_files_id_key", table_name="marc21_records_files")
    op.drop_table("marc21_records_files")
    op.drop_index("uidx_marc21_drafts_files_id_key", table_name="marc21_drafts_files")
    op.drop_table("marc21_drafts_files")
    op.drop_table("marc21_records_metadata")
    op.drop_table("marc21_drafts_metadata")
    op.drop_table("marc21_templates")
    op.drop_table("marc21_parents_metadata")
    # ### end Alembic commands ###
