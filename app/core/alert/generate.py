# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from abc import ABC, abstractmethod

import pytz
from prefect.client.schemas.objects import Flow, FlowRun, State
from prefect.settings import PREFECT_UI_URL

from app.core.alert.templates.slack import SLACK_WEBHOOK_TEMPLATE


class AlertGenerator(ABC):
    @abstractmethod
    def generate_alert_message(self):
        pass


class GmailAlertGenerator(AlertGenerator):
    def generate_alert_message(self) -> str:
        return ""


class SlackAlertGenerator(AlertGenerator):
    @staticmethod
    def generate_alert_message(flow: Flow, flow_run: FlowRun, state: State) -> str:
        return SLACK_WEBHOOK_TEMPLATE.substitute(
            pool=flow_run.work_pool_name,
            queue=flow_run.work_queue_name,
            flow=flow.name,
            job=flow_run.name,
            state=state.name,
            url=f"{PREFECT_UI_URL.value()}/runs/flow-run/{flow_run.id}",
            tags=flow_run.tags,
            scheduled_start=flow_run.expected_start_time.astimezone(
                pytz.timezone("Asia/Seoul")
            ),
        )
