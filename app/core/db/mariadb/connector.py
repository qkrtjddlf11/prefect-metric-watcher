# pylint: disable=C0114, C0115, C0116
# coding: utf-8


from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker

DRIVER_NAME = "mysql+mysqlconnector"


class MariaDBConnector:
    """
    MariaDB Connection Class
    """

    def __init__(
        self,
        logger,
        host="localhost",
        port=3306,
        username="root",
        password="root",
        db_name="metric_watcher",
    ) -> None:
        self.logger = logger
        self.server_ips = host
        self.port = port
        self.user = username
        self.password = password.get_secret_value()
        self.db = db_name
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
            self.logger.error(e)
            raise e
        finally:
            self.session.close()  # 세션 닫기

    def execute_session_query(self, query_func, *args, **kwargs):
        try:
            with self.get_resources() as session:
                return query_func(session, *args, **kwargs)
        except SQLAlchemyError as err:
            self.logger.error(err)
            raise
