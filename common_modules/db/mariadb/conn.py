# pylint: disable=C0114, C0115, C0116
# coding: utf-8


from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker


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
