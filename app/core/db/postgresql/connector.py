# pylint: disable=C0114, C0115, C0116
# coding: utf-8

import logging
import time
from contextlib import contextmanager

from pydantic.types import SecretStr
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


class PostgreSQLConnector:
    def __init__(
        self,
        logger: logging.Logger,
        host: str,
        port: str,
        username: str,
        password: SecretStr,
        db_name: str,
        max_retries=65535,
        retry_interval=5,
        pool_size=1,
    ):
        self.logger = logger
        self.db_url = f"postgresql://{username}:{password.get_secret_value()}@{host}:{port}/{db_name}"
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.engine = create_engine(
            self.db_url,
            pool_size=pool_size,
            max_overflow=10,  # 추가 커넥션 허용 개수
            connect_args={"connect_timeout": 10},  # 연결 타임아웃 설정
        )

        # 세션 팩토리 생성
        self.session_maker = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )

    def close(self):
        if self.engine:
            self.engine.dispose()

    @contextmanager
    def get_session(self):
        session = self.session_maker()

        try:
            yield session
            session.commit()
        except SQLAlchemyError as err:
            session.rollback()
            self.logger.error(f"DB Error: {err}")
            raise
        finally:
            session.close()

    def execute_and_fetchall(self, sql: str, params=None):
        retries = 0
        while retries < self.max_retries:
            try:
                with self.get_session() as session:
                    result = session.execute(text(sql), params or {})
                    return result.fetchall()
            except SQLAlchemyError as err:
                self.logger.error(f"SQL Execution Failed: {sql}, Error: {err}")
                self.logger.info("Retrying...")
                retries += 1
                time.sleep(self.retry_interval)

        self.logger.error(f"Max retries reached for SQL execution: {sql}")
        return None
