# pylint: disable=C0114, C0115, C0116,
# coding: utf-8

import logging
import time
from contextlib import contextmanager

import psycopg2
from psycopg2 import pool


class PostgreSQLConnection:
    def __init__(
        self,
        logger: logging.Logger,
        server_ips="localhost",
        port=5432,
        username="postgres",
        password="postgres",
        db="prefect",
        max_retries=65535,
        retry_interval=5,
        pool_size=1,
    ):
        self.logger = logger
        self.user = username
        self.passwd = password
        self.server_ips = server_ips
        self.server_port = port
        self.db_name = db
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.pool_size = pool_size
        self._connection_pool = self._create_connection_pool()

    def _create_connection_pool(self):
        return pool.SimpleConnectionPool(
            minconn=1,
            maxconn=self.pool_size,
            user=self.user,
            password=self.passwd,
            host=",".join(self.server_ips),
            port=self.server_port,
            database=self.db_name,
            connect_timeout=1,
        )

    def close(self):
        if self._connection_pool is not None:
            self._connection_pool.closeall()

    @contextmanager
    def get_resources(self, autocommit=False):
        conn = self._connection_pool.getconn()
        conn.autocommit = autocommit
        cursor = conn.cursor()

        try:
            yield cursor, conn
        finally:
            cursor.close()
            self._connection_pool.putconn(conn)

    def execute_and_fetchall(self, sql: str):
        retries = 0
        while retries < self.max_retries:
            try:
                with self.get_resource() as (cursor, _):
                    cursor.execute(sql)
                    return cursor.fetchall()
            except psycopg2.Error as err:
                self.logger.error(f"execute_and_fetchall SQL : {sql}, err : {err}")
                self.logger.info("Retrying...")
                retries += 1
                time.sleep(self.retry_interval)
        return None
