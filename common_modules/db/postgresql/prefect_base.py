# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FlowRun(Base):
    __tablename__ = "flow_run"

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
    state_type = Column(String)
    run_count = Column(Integer, nullable=False, server_default="0")
    expected_start_time = Column(DateTime(timezone=True))
    next_scheduled_start_time = Column(DateTime(timezone=True))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    total_run_time = Column(String, nullable=False, server_default="00:00:00")
    flow_version = Column(String)
    parameters = Column(JSON, nullable=False, server_default="{}")
    idempotency_key = Column(String)
    context = Column(JSON, nullable=False, server_default="{}")
    empirical_policy = Column(JSON, nullable=False, server_default="{}")
    tags = Column(JSON, nullable=False, server_default="[]")
    auto_scheduled = Column(Boolean, nullable=False, server_default="false")
    flow_id = Column(UUID(as_uuid=True), ForeignKey("flow.id"), nullable=False)
    deployment_id = Column(UUID(as_uuid=True))
    parent_task_run_id = Column(UUID(as_uuid=True), ForeignKey("task_run.id"))
    state_id = Column(UUID(as_uuid=True), ForeignKey("flow_run_state.id"))
    state_name = Column(String)
    infrastructure_document_id = Column(
        UUID(as_uuid=True), ForeignKey("block_document.id")
    )
    work_queue_name = Column(String)
    state_timestamp = Column(DateTime(timezone=True))
    created_by = Column(JSON)
    infrastructure_pid = Column(String)
    work_queue_id = Column(UUID(as_uuid=True), ForeignKey("work_queue.id"))
