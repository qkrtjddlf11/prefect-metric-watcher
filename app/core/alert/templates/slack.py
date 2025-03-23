# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from string import Template

SLACK_WEBHOOK_TEMPLATE = Template(
    """
        🚨 Flow Failure 🚨\n\n
        Pool: $pool\n
        Queue: $queue\n
        Flow: $flow\n
        Your job $job entered $state with message:\n\n
        See <$url|the flow run in the UI>\n\n
        Tags: $tags\n\n
        Scheduled start: $scheduled_start
    """
)
