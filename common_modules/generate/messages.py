# pylint: disable=C0114, C0115, C0116
# coding: utf-8
from common_modules.common.base_impl import Metric
from common_modules.define.name import POINT_USAGE_PERCENT, POINT_USED_PERCENT


def generate_alert_messages(metric: Metric, eval_point_group_list: dict) -> str:
    key = None

    for v in [POINT_USAGE_PERCENT, POINT_USED_PERCENT]:
        if v in eval_point_group_list:
            key = v
            break

    return (
        f"Time : {eval_point_group_list.get('time')}\n"
        + f"Metric : {metric.metric_type_name.upper()}\n"
        + f"Result : {round(eval_point_group_list.get(key), 2)} {metric.eval_operator} {metric.eval_value}"
    )
