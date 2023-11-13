class Metric:
    def __init__(
        self,
        metric_type_seq: int = 0,
        metric_name: str = "",
        eval_value: int = 0,
        eval_operator_type_seq: int = 0,
        operator_name: str = "",
    ) -> None:
        self.metric_type_seq = metric_type_seq
        self.metric_name = metric_name
        self.eval_value = eval_value
        self.eval_operator_type_seq = eval_operator_type_seq
        self.operator_name = operator_name

    def __str__(self) -> str:
        return (
            f"Metric(metric_type_seq={self.metric_type_seq}, "
            + f"metric_name={self.metric_name}, "
            + f"eval_value={self.eval_value}, "
            + f"eval_operator_type_seq={self.eval_operator_type_seq}, "
            + f"operator_name={self.operator_name})"
        )
