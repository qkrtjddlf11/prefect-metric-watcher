# pylint: disable=C0114, C0116, C0115
# coding: utf-8

from prefect import variables
from prefect.blocks.notifications import SlackWebhook
from prefect.settings import PREFECT_UI_URL


def flow_failure_webhook(flow, flow_run, state):
    slack_webhook = SlackWebhook(url=variables.get("my_slack_webhook"))
    slack_webhook_block = slack_webhook.load("slack-webhook-block")
    slack_webhook_block.notify(
        (
            f"Flow: {flow}"
            f"Your job {flow_run.name} entered {state.name} "
            f"with message:\n\n"
            f"See <{PREFECT_UI_URL.value()}/flow-runs/"
            f"flow-run/{flow_run.id}|the flow run in the UI>\n\n"
            f"Tags: {flow_run.tags}\n\n"
            f"Scheduled start: {flow_run.expected_start_time}"
        )
    )
