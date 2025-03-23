# pylint: disable=C0114, C0116, C0115
# coding: utf-8

from prefect import Flow
from prefect.blocks.notifications import SlackWebhook
from prefect.client.schemas.objects import Flow, FlowRun, State

from app.core.alert.generate import SlackAlertGenerator


def flow_failure_webhook(flow: Flow, flow_run: FlowRun, state: State):
    body = SlackAlertGenerator.generate_alert_message(flow, flow_run, state)
    slack_webhook_block = SlackWebhook.load("slack-webhook-block")
    slack_webhook_block.notify(body)
