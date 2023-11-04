# pylint: disable=C0114, C0115, C0116
# coding: utf-8


import logging
import sys
from contextlib import contextmanager

from influxdb import InfluxDBClient, exceptions


class InfluxDBConnection:
    """
    InfluxDB Connection Class
    """

    def __init__(
        self,
        logger: logging,
        host="localhost",
        port=8086,
        username="root",
        password="root",
        database="influx",
    ) -> None:
        self.logger = logger
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.conn = self._create_connection()

    def _create_connection(self) -> InfluxDBClient:
        return InfluxDBClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
            timeout=1,
            retries=5,
        )

    @contextmanager
    def get_resource(self):
        try:
            yield self.conn
        except exceptions.InfluxDBServerError as err:
            self.logger.error("Server Error : %s", str(err))
            sys.exit(1)
        finally:
            self.conn.close()

    def get_metric_data(self):
        self._close_connection()

    def generate_sql_statements(self):
        pass

    def __str__(self) -> str:
        return (
            f"Connection Info :\n"
            + f"\thost={self.host}\n"
            + f"\tport={self.port}\n"
            + f"\tusername={self.username}\n"
            + f"\tpassword={self.password}\n"
            + f"\tdatabase={self.database}"
        )
