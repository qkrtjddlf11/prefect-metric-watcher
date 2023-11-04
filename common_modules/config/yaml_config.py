# pylint: disable=C0114, C0115, C0116
# coding: utf-8

import logging
from functools import reduce
from operator import getitem

import yaml


class YamlConfig:
    def __init__(self, logger: logging, config_path="config.yaml"):
        self.logger = logger
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self):
        with open(self.config_path, "r", encoding="utf8") as config_file:
            return yaml.safe_load(config_file)

    def get_all_config(self):
        return self._config

    def get_value(self, key):
        keys = key.split(":")

        try:
            value = reduce(getitem, keys, self._config)
            return value
        except KeyError:
            self.logger.error("config key not found: %s", key)
            raise
