from common_modules.common.base_impl import Metric


def update_point(
    point: dict,
    metric: Metric,
    metric_eval_result_seq_name: str,
    metric_eval_result_seq: int,
) -> None:
    if point is not None:
        point.update({metric_eval_result_seq_name: metric_eval_result_seq})

    metric.eval_point_group_list.append(point)
