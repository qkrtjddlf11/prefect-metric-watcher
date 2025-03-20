# pylint: disable=C0114, C0115, C0116, S1192
# coding: utf-8

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Interval,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    desc,
)
from sqlalchemy.dialects.postgresql import JSON, JSONB, UUID
from sqlalchemy.orm import registry

mapper_registry = registry()


@mapper_registry.mapped
class Artifact:
    __tablename__ = "artifact"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    created = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )
    updated = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )
    key = Column(String, nullable=True)
    type = Column(String, nullable=True)
    data = Column(JSONB, nullable=True)
    metadata_ = Column(JSONB, nullable=True)
    task_run_id = Column(
        UUID(as_uuid=True), ForeignKey("task_run.id", ondelete="CASCADE"), nullable=True
    )
    flow_run_id = Column(
        UUID(as_uuid=True), ForeignKey("flow_run.id", ondelete="CASCADE"), nullable=True
    )
    description = Column(String, nullable=True)

    __table_args__ = (
        Index("ix_artifact__flow_run_id", "flow_run_id"),
        Index("ix_artifact__key", "key"),
        Index(
            "ix_artifact__key_created_desc",
            "key",
            desc("created"),
            postgresql_include=["id", "updated", "type", "task_run_id", "flow_run_id"],
        ),
        Index("ix_artifact__task_run_id", "task_run_id"),
        Index("ix_artifact__updated", "updated"),
    )


@mapper_registry.mapped
class EventResources:
    __tablename__ = "event_resources"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    occurred = Column(DateTime(timezone=True), nullable=False)
    resource_id = Column(Text, nullable=False)
    resource_role = Column(Text, nullable=False)
    resource = Column(JSONB, nullable=False)
    event_id = Column(
        UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )
    created = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )
    updated = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )

    __table_args__ = (
        Index("ix_event_resources__resource_id__occurred", "resource_id", "occurred"),
        Index("ix_event_resources__updated", "updated"),
    )


@mapper_registry.mapped
class Events:
    __tablename__ = "events"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    occurred = Column(DateTime(timezone=True), nullable=False)
    event = Column(Text, nullable=False)
    resource_id = Column(Text, nullable=False)
    resource = Column(JSONB, nullable=False)
    related_resource_ids = Column(JSONB, nullable=False, server_default="'[]'::jsonb")
    related = Column(JSONB, nullable=False, server_default="'[]'::jsonb")
    payload = Column(JSONB, nullable=False)
    received = Column(DateTime(timezone=True), nullable=False)
    recorded = Column(DateTime(timezone=True), nullable=False)
    follows = Column(
        UUID(as_uuid=True), ForeignKey("events.id", ondelete="SET NULL"), nullable=True
    )
    created = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )
    updated = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )

    __table_args__ = (
        Index("ix_events__event__id", "event", "id"),
        Index("ix_events__event_occurred_id", "event", "occurred", "id"),
        Index("ix_events__event_related_occurred", "event", "related", "occurred"),
        Index(
            "ix_events__event_resource_id_occurred", "event", "resource_id", "occurred"
        ),
        Index("ix_events__occurred", "occurred"),
        Index("ix_events__occurred_id", "occurred", "id"),
        Index("ix_events__related_resource_ids", "related_resource_ids"),
        Index("ix_events__updated", "updated"),
    )


@mapper_registry.mapped
class FlowRun:
    __tablename__ = "flow_run"
    __table_args__ = (
        UniqueConstraint(
            "flow_id", "idempotency_key", name="uq_flow_run__flow_id_idempotency_key"
        ),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    created = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )
    updated = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )
    name = Column(String, nullable=False)
    state_type = Column(String, nullable=True)
    run_count = Column(Integer, nullable=False, server_default="0")
    expected_start_time = Column(DateTime(timezone=True), nullable=True)
    next_scheduled_start_time = Column(DateTime(timezone=True), nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    total_run_time = Column(
        Interval, nullable=False, server_default="'00:00:00'::interval"
    )
    flow_version = Column(String, nullable=True)
    parameters = Column(JSONB, nullable=False, server_default="'{}'::jsonb")
    idempotency_key = Column(String, nullable=True)
    context = Column(JSONB, nullable=False, server_default="'{}'::jsonb")
    empirical_policy = Column(JSONB, nullable=False, server_default="'{}'::jsonb")
    tags = Column(JSONB, nullable=False, server_default="'[]'::jsonb")
    auto_scheduled = Column(Boolean, nullable=False, server_default="false")
    flow_id = Column(
        UUID(as_uuid=True), ForeignKey("flow.id", ondelete="CASCADE"), nullable=False
    )
    deployment_id = Column(UUID(as_uuid=True), nullable=True)
    parent_task_run_id = Column(
        UUID(as_uuid=True),
        ForeignKey("task_run.id", ondelete="SET NULL"),
        nullable=True,
    )
    state_id = Column(
        UUID(as_uuid=True),
        ForeignKey("flow_run_state.id", ondelete="SET NULL"),
        nullable=True,
    )
    state_name = Column(String, nullable=True)
    infrastructure_document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("block_document.id", ondelete="CASCADE"),
        nullable=True,
    )
    work_queue_name = Column(String, nullable=True)
    state_timestamp = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(JSONB, nullable=True)
    infrastructure_pid = Column(String, nullable=True)
    work_queue_id = Column(
        UUID(as_uuid=True),
        ForeignKey("work_queue.id", ondelete="SET NULL"),
        nullable=True,
    )
    job_variables = Column(JSONB, nullable=True, server_default="'{}'::jsonb")
    deployment_version = Column(String, nullable=True)
    labels = Column(JSONB, nullable=True)

    __table_args__ += (
        Index(
            "ix_flow_run__coalesce_start_time_expected_start_time_asc",
            "start_time",
            "expected_start_time",
        ),
        Index(
            "ix_flow_run__coalesce_start_time_expected_start_time_desc",
            "start_time",
            desc("expected_start_time"),
        ),
        Index("ix_flow_run__deployment_version", "deployment_version"),
        Index("ix_flow_run__end_time_desc", desc("end_time")),
        Index("ix_flow_run__expected_start_time_desc", desc("expected_start_time")),
        Index("ix_flow_run__flow_id", "flow_id"),
        Index("ix_flow_run__flow_version", "flow_version"),
        Index("ix_flow_run__infrastructure_document_id", "infrastructure_document_id"),
        Index("ix_flow_run__name", "name"),
        Index(
            "ix_flow_run__next_scheduled_start_time_asc", "next_scheduled_start_time"
        ),
        Index("ix_flow_run__parent_task_run_id", "parent_task_run_id"),
        Index("ix_flow_run__start_time", "start_time"),
        Index("ix_flow_run__state_id", "state_id"),
        Index("ix_flow_run__state_name", "state_name"),
        Index("ix_flow_run__state_timestamp", "state_timestamp"),
        Index("ix_flow_run__state_type", "state_type"),
        Index("ix_flow_run__updated", "updated"),
        Index("ix_flow_run__work_queue_id", "work_queue_id"),
        Index("ix_flow_run__work_queue_name", "work_queue_name"),
    )


@mapper_registry.mapped
class Log:
    __tablename__ = "log"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    created = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )
    updated = Column(
        DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP"
    )
    name = Column(String, nullable=False)
    level = Column(SmallInteger, nullable=False)
    flow_run_id = Column(
        UUID(as_uuid=True), ForeignKey("flow_run.id", ondelete="CASCADE"), nullable=True
    )
    task_run_id = Column(
        UUID(as_uuid=True), ForeignKey("task_run.id", ondelete="CASCADE"), nullable=True
    )
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_log__flow_run_id", "flow_run_id"),
        Index("ix_log__flow_run_id_timestamp", "flow_run_id", "timestamp"),
        Index("ix_log__level", "level"),
        Index("ix_log__task_run_id", "task_run_id"),
        Index("ix_log__timestamp", "timestamp"),
        Index("ix_log__updated", "updated"),
    )
