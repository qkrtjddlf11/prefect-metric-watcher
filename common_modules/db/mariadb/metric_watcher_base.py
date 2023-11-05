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
    t_metric_eval_thresholds = relationship(
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
    t_metric_eval_thresholds = relationship(
        "TMetricEvalThreshold", back_populates="t_code_metric_type"
    )


# TMetricEvalThreshold 클래스 정의
class TMetricEvalThreshold(Base):
    __tablename__ = "t_metric_eval_threshold"

    metric_eval_threshold_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Individual Metric Sequence"
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
    eval_value = Column(Integer, nullable=False, comment="임계치")

    # 외래 키로 연결된 테이블과의 관계 설정
    t_code_eval_type = relationship("TCodeEvalType", back_populates="t_metric_eval_thresholds")
    t_code_metric_type = relationship("TCodeMetricType", back_populates="t_metric_eval_thresholds")
