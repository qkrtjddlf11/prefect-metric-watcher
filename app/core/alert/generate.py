# pylint: disable=C0114, C0115, C0116
# coding: utf-8
from abc import ABC, abstractmethod


class AlertGenerator(ABC):
    @abstractmethod
    def generate_alert_message(self):
        pass


class GmailAlertGenerator(AlertGenerator):
    def generate_alert_message(self) -> str:
        return ""


class SlackAlertGenerator(AlertGenerator):
    def generate_alert_message(self) -> str:
        return ""
