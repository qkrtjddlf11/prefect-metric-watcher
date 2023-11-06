# pylint: disable=C0114, C0115, C0116
# coding: utf-8


from contextlib import contextmanager
from typing import List, Tuple

from sqlalchemy import Engine, Row, create_engine
from sqlalchemy.orm import sessionmaker

from common_modules.db.mariadb.metric_watcher_base import (
    TCodeEvalOperatorType,
    TCodeEvalType,
    TCodeMetricType,
    TMetricEvalThreshold,
)


class MariaDBConnection:
    """
    MariaDB Connection Class
    """

    def __init__(
        self, logger, host="localhost", port=3306, user="root", password="root", db="metric_watcher"
    ) -> None:
        self.logger = logger
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        self._engine = self._create_engine()

    def _create_engine(self) -> Engine:
        return create_engine(
            f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )

    @contextmanager
    def get_resources(self):
        # Session 생성
        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            yield session  # with 블록으로 진입
            session.commit()  # with 블록을 빠져나올 때 커밋
        except Exception as e:
            session.rollback()  # 예외 발생 시 롤백
            raise e
        finally:
            session.close()  # 세션 닫기

    def implement_query(
        self, metric_type_seq: int, eval_type_seq
    ) -> List[Row[Tuple[int, str, int, int, str]]]:
        with self.get_resources() as session:
            query = (
                session.query(
                    TMetricEvalThreshold.metric_type_seq,
                    TCodeMetricType.name,
                    TMetricEvalThreshold.eval_value,
                    TMetricEvalThreshold.eval_operator_type_seq,
                    TCodeEvalOperatorType.name,
                )
                .select_from(TMetricEvalThreshold)
                .join(
                    TCodeEvalType, TMetricEvalThreshold.eval_type_seq == TCodeEvalType.eval_type_seq
                )
                .join(
                    TCodeMetricType,
                    TMetricEvalThreshold.metric_type_seq == TCodeMetricType.metric_type_seq,
                )
                .join(
                    TCodeEvalOperatorType,
                    TMetricEvalThreshold.eval_operator_type_seq
                    == TCodeEvalOperatorType.eval_operator_type_seq,
                )
                .filter(TMetricEvalThreshold.metric_type_seq == metric_type_seq)
                .filter(TMetricEvalThreshold.eval_type_seq == eval_type_seq)
            )

            print("=============== Query Statement Start ================")
            print(query.statement)
            print("=============== End Query Statement ================")

            return query.all()
