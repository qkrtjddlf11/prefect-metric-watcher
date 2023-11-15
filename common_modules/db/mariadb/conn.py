# pylint: disable=C0114, C0115, C0116
# coding: utf-8


from contextlib import contextmanager
from typing import List, Tuple

from sqlalchemy import Engine, Row, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from common_modules.db.mariadb.metric_watcher_base import (
    TCodeEvalOperatorType,
    TCodeEvalType,
    TCodeMetricType,
    TMetricEvalThreshold,
)

DRIVER_NAME = "mysql+mysqlconnector"


class MariaDBConnection:
    """
    MariaDB Connection Class
    """

    def __init__(
        self,
        logger,
        server_ips="localhost",
        port=3306,
        username="root",
        password="root",
        db="metric_watcher",
    ) -> None:
        self.logger = logger
        self.server_ips = server_ips
        self.port = port
        self.user = username
        self.password = password
        self.db = db
        self._engine = self._create_engine()
        self.session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            )
        )

    def _create_engine(self) -> Engine:
        return create_engine(
            f"{DRIVER_NAME}://{self.user}:{self.password}@{self.server_ips}:{self.port}/{self.db}",
            pool_size=10,
            max_overflow=20,
            echo=False,
        )

    @contextmanager
    def get_resources(self):
        try:
            yield self.session  # with 블록으로 진입
        except Exception as e:
            raise e
        finally:
            self.session.close()  # 세션 닫기

    # TODO 공통 쿼리 만들기
    def execute_sessin_query(self, query, *args, **kwargs):
        pass

    def sql_get_metric_eval_threshold_list(
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
                    TCodeEvalType,
                    TMetricEvalThreshold.eval_type_seq == TCodeEvalType.eval_type_seq,
                )
                .join(
                    TCodeMetricType,
                    TMetricEvalThreshold.metric_type_seq
                    == TCodeMetricType.metric_type_seq,
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
