# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from abc import ABC, abstractmethod
from string import Template
from typing import Any


class AlertGenerator(ABC):
    @abstractmethod
    def generate_alert_message(self):
        pass


class GmailAlertGenerator(AlertGenerator):
    def generate_alert_message(self) -> str:
        return ""


class SlackAlertGenerator(AlertGenerator):
    @staticmethod
    def generate_alert_message(template: Template, mapping: dict[str, Any]) -> str:
        return template.substitute(mapping)
