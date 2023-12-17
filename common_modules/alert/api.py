import random

from common_modules.common.base_impl import Metric
from common_modules.generate.messages import generate_alert_messages


def alert_send_api(metric: Metric, eval_point: dict):
    generated_messages = generate_alert_messages(metric, eval_point)
    # TODO Sent Alert..

    return generated_messages, random.choice(["Y", "N"])
