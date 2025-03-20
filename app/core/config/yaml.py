# pylint: disable=C0114, C0115, C0116
# coding: utf-8

import logging
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, SecretStr
from yaml import YAMLError


class InfluxDBConfig(BaseModel):
    host: str = Field(..., description="InfluxDB Host")
    port: int = Field(..., gt=0, lt=65536, description="InfluxDB Port")
    username: str = Field(..., description="InfluxDB Username")
    password: SecretStr = Field(..., description="InfluxDB Password")
    db_name: str = Field(..., description="InfluxDB Database Name")


class MariaDBConfig(BaseModel):
    host: str = Field(..., description="MariaDB Host")
    port: int = Field(..., gt=0, lt=65536, description="MariaDB Port")
    username: str = Field(..., description="MariaDB Username")
    password: SecretStr = Field(..., description="MariaDB Password")
    db_name: str = Field(..., description="MariaDB Database Name")


class PostgreSQLConfig(BaseModel):
    host: str = Field(..., description="PostgreSQL Host")
    port: int = Field(..., gt=0, lt=65536, description="PostgreSQL Port")
    username: str = Field(..., description="PostgreSQL Username")
    password: SecretStr = Field(..., description="PostgreSQL Password")
    db_name: str = Field(..., description="PostgreSQL Database Name")


class YamlConfig(BaseModel):
    influxdb: InfluxDBConfig
    mariadb: MariaDBConfig
    postgresql: PostgreSQLConfig

    @classmethod
    def load_yaml(cls, base_path: str, mode: str):
        file_path = Path(base_path) / f"config_{mode.lower()}.yml"

        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with open(file_path, "r") as f:
            config = yaml.safe_load(f)

        return cls(**config)


def get_yaml_config(logger: logging.Logger, base_path: str, mode="dev") -> YamlConfig:
    try:
        yaml_config = YamlConfig.load_yaml(base_path=base_path, mode=mode)
    except FileNotFoundError as err:
        logger.error("File Not Found : %s", str(err))
        raise
    except YAMLError as err:
        logger.error("Yaml load Error : %s", str(err))
        raise
    return yaml_config
