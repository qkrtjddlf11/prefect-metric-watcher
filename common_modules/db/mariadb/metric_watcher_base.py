# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, String
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
    svr_vrc_list = Column(String(100), comment="SVR_VRC List")
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
    t_code_metric_type = relationship(
        "TCodeMetricType", back_populates="t_metric_eval_threshold"
    )
    t_code_eval_operator_type = relationship(
        "TCodeEvalOperatorType", back_populates="t_metric_eval_threshold"
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

    # 외래 키에 대한 참조를 정의합니다.
    t_metric_eval_threshold = relationship(
        "TMetricEvalThreshold", back_populates="t_metric_eval_history"
    )
    t_metric_eval_result_type = relationship(
        "TCodeMetricEvalResultType", back_populates="t_metric_eval_history"
    )


# TCodeMetricEvalResultType 클래스 정의
class TCodeMetricEvalResultType(Base):
    __tablename__ = "t_code_metric_eval_result_type"

    metric_eval_result_seq = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="metric eval result name")

    t_metric_eval_history = relationship(
        "TMetricEvalHistory", back_populates="t_code_metric_eval_result_type"
    )
