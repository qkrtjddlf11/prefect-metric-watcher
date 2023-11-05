# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class TAlertType(Base):
    __tablename__ = "t_code_alert_type"

    alert_type_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Alert Type Sequence"
    )
    name = Column(String(100), nullable=False, comment="Alert Name")


class TMetricType(Base):
    __tablename__ = "t_code_metric_type"

    metric_seq = Column(Integer, primary_key=True, comment="Metric Sequence")
    name = Column(String(100), nullable=False, comment="Metric Name")

    # MetricThreshold 모델과의 관계 설정
    metric_thresholds = relationship("TMetricThreshold", back_populates="metric_type")


class TMetricThreshold(Base):
    __tablename__ = "t_metric_threshold"

    metric_threshold_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Metric Threshold Sequence"
    )
    threshold_value = Column(Integer, nullable=False, comment="Metric Threshold")
    metric_seq = Column(
        Integer,
        ForeignKey("t_code_metric_type.metric_seq"),
        comment="Foreign Key to t_code_metric_type",
    )

    # 외래 키로 연결된 테이블과의 관계 설정
    metric_type = relationship("TMetricType", back_populates="metric_thresholds")
