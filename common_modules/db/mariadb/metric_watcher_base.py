# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# TCodeEvalType 클래스 정의
class TCodeEvalType(Base):
    __tablename__ = "t_code_eval_type"

    eval_type_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Evaluate Type Sequence"
    )
    name = Column(String(100), nullable=False, comment="Evaluate Name")

    # TMetricEvalThreshold 모델과의 관계 설정
    t_metric_eval_threshold = relationship(
        "TMetricEvalThreshold", back_populates="t_code_eval_type"
    )


# TCodeMetricType 클래스 정의
class TCodeMetricType(Base):
    __tablename__ = "t_code_metric_type"

    metric_type_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Metric Sequence"
    )
    name = Column(String(100), nullable=False, comment="Metric Name")

    # TMetricEvalThreshold 모델과의 관계 설정
    t_metric_eval_threshold = relationship(
        "TMetricEvalThreshold", back_populates="t_code_metric_type"
    )


# TMetricEvalThreshold 클래스 정의
class TMetricEvalThreshold(Base):
    __tablename__ = "t_metric_eval_threshold"

    metric_eval_threshold_seq = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Individual Metric Sequence",
    )
    metric_type_seq = Column(
        Integer,
        ForeignKey("t_code_metric_type.metric_type_seq"),
        nullable=False,
        comment="Metric Type Sequence",
    )
    eval_type_seq = Column(
        Integer,
        ForeignKey("t_code_eval_type.eval_type_seq"),
        nullable=False,
        comment="Evaluate Type Sequence",
    )
    operation_server_seq = Column(
        Integer,
        ForeignKey("t_operation_server.operation_server_seq"),
        nullable=False,
        comment="Operation Server Sequence",
    )
    eval_operator_type_seq = Column(
        Integer,
        ForeignKey("t_code_eval_operator_type.eval_operator_type_seq"),
        nullable=False,
        comment="Evaluate Operator Type Sequence",
    )
    eval_value = Column(Integer, nullable=False, comment="임계치")

    # 외래 키로 연결된 테이블과의 관계 설정
    t_code_eval_type = relationship(
        "TCodeEvalType", back_populates="t_metric_eval_threshold"
    )
    t_operation_server = relationship(
        "TOperationServer", back_populates="t_metric_eval_threshold"
    )
    t_code_metric_type = relationship(
        "TCodeMetricType", back_populates="t_metric_eval_threshold"
    )
    t_code_eval_operator_type = relationship(
        "TCodeEvalOperatorType", back_populates="t_metric_eval_threshold"
    )
    t_metric_eval_history = relationship(
        "TMetricEvalHistory", back_populates="t_metric_eval_threshold"
    )


# EvalOperatorType 클래스 정의
class TCodeEvalOperatorType(Base):
    __tablename__ = "t_code_eval_operator_type"

    eval_operator_type_seq = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Evaluate Operator Type Sequence",
    )
    name = Column(String(100), nullable=False, comment="Evaluate Operator Name")
    eval_operator = Column(String(100), nullable=False, comment="Evaluate Operator")

    # TMetricEvalThreshold 모델과의 관계 설정
    t_metric_eval_threshold = relationship(
        "TMetricEvalThreshold", back_populates="t_code_eval_operator_type"
    )


# MetricEvalHistory 클래스 정의
class TMetricEvalHistory(Base):
    __tablename__ = "t_metric_eval_history"

    metric_eval_history_seq = Column(Integer, primary_key=True, autoincrement=True)
    metric_eval_threshold_seq = Column(
        Integer,
        ForeignKey("t_metric_eval_threshold.metric_eval_threshold_seq"),
        nullable=False,
    )
    metric_eval_result_seq = Column(
        Integer,
        ForeignKey("t_code_metric_eval_result_type.metric_eval_result_seq"),
        nullable=False,
    )
    operation_server_seq = Column(
        Integer,
        ForeignKey("t_operation_server.operation_server_seq"),
        nullable=False,
    )
    metric_eval_result_value = Column(
        Float, nullable=False, default=0, comment="Evaluate result value"
    )
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    # 외래 키에 대한 참조를 정의합니다.
    t_metric_eval_threshold = relationship(
        "TMetricEvalThreshold", back_populates="t_metric_eval_history"
    )
    t_code_metric_eval_result_type = relationship(
        "TCodeMetricEvalResultType", back_populates="t_metric_eval_history"
    )
    t_operation_server = relationship(
        "TOperationServer", back_populates="t_metric_eval_history"
    )


# TCodeMetricEvalResultType 클래스 정의
class TCodeMetricEvalResultType(Base):
    __tablename__ = "t_code_metric_eval_result_type"

    metric_eval_result_seq = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="metric eval result name")

    t_metric_eval_history = relationship(
        "TMetricEvalHistory", back_populates="t_code_metric_eval_result_type"
    )


# TOperationServer 클래스 정의
class TOperationServer(Base):
    __tablename__ = "t_operation_server"

    operation_server_seq = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Operation Server Sequence",
    )
    name = Column(String(100), nullable=False, comment="Operation Server name")
    ip_address = Column(
        String(15),
        nullable=False,
        default="0.0.0.0",
        comment="Operation Server IP Address",
    )

    t_metric_eval_history = relationship(
        "TMetricEvalHistory", back_populates="t_operation_server"
    )
    t_metric_eval_threshold = relationship(
        "TMetricEvalThreshold", back_populates="t_operation_server"
    )


class TAlertHistory(Base):
    __tablename__ = "t_alert_history"

    alert_history_seq = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Alert History Sequence",
    )
    alert_content = Column(Text, default=None, comment="Alert Content")
    alert_send_status = Column(
        String(1), nullable=False, default="N", comment="Alert Send Status"
    )
    reg_datetime = Column(
        DateTime,
        nullable=False,
        # default="current_timestamp()",
        default=datetime.utcnow,
        comment="Alert register datetime",
    )
    send_datetime = Column(DateTime, default=None, comment="Alert send datetime")
