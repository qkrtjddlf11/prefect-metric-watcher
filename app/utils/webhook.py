# pylint: disable=C0114, C0116, C0115
# coding: utf-8

import pytz
from prefect import Flow
from prefect.blocks.notifications import SlackWebhook
from prefect.client.schemas.objects import Flow, FlowRun, State
from prefect.settings import PREFECT_UI_URL

from app.core.alert.generate import SlackAlertGenerator
from app.core.alert.templates.slack import SLACK_WEBHOOK_TEMPLATE


def flow_failure_webhook(flow: Flow, flow_run: FlowRun, state: State):
    mapping = {
        "pool": flow_run.work_pool_name,
        "queue": flow_run.work_queue_name,
        "flow": flow.name,
        "job": flow_run.name,
        "state": state.name,
        "url": f"{PREFECT_UI_URL.value()}/runs/flow-run/{flow_run.id}",
        "tags": flow_run.tags,
        "scheduled_start": flow_run.expected_start_time.astimezone(
            pytz.timezone("Asia/Seoul")
        ),
    }
    body = SlackAlertGenerator.generate_alert_message(SLACK_WEBHOOK_TEMPLATE, mapping)
    slack_webhook_block = SlackWebhook.load("slack-webhook-block")
    slack_webhook_block.notify(body)
