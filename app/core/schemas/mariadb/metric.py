# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from pydantic import BaseModel, Field


class EvaluateFlows(BaseModel):
    evaluate_flow_seq: int = Field(..., description="Evaluate flow sequence")
    evaluate_flow_name: str = Field(..., description="Evaluate flow name")
    metric_type_seq: int = Field(..., description="Metric type sequence")
    metric_type_name: str = Field(..., description="Metric type name")
    comparison_operator_type_seq: int = Field(
        ..., description="Comparison operator type sequence"
    )
    comparison_operator_type_name: str = Field(
        ..., description="Comparison operator type name"
    )
    evaluate_value: int = Field(..., description="Evaluate value")
    evaluate_target_type_seq: int = Field(
        ..., description="Evaluate target type sequence"
    )
    evaluate_target_type_name: str = Field(..., description="Evaluate target type name")

    def __str__(self) -> str:
        return (
            f"EvaluateFlows(evaluate_flow_seq={self.evaluate_flow_seq}, "
            + f"evaluate_flow_name={self.evaluate_flow_name}, "
            + f"metric_type_seq={self.metric_type_seq}, "
            + f"metric_type_name={self.metric_type_name}, "
            + f"comparison_operator_type_seq={self.comparison_operator_type_seq}, "
            + f"comparison_operator_type_name={self.comparison_operator_type_name}, "
            + f"evaluate_value={self.evaluate_value}, "
            + f"evaluate_target_type_seq={self.evaluate_target_type_seq}, "
            + f"evaluate_target_type_name={self.evaluate_target_type_name})"
        )


class EvaluateResultHistory(BaseModel):
    evaluate_flow_seq: int = Field(..., description="Evaluate flow sequence")
    evaluate_result_type_seq: int = Field(
        ..., description="Evaluate result type sequence"
    )
    result_value: float = Field(..., description="Result value")
    node_id: str = Field(..., description="Node ID")
    server_id: str = Field(..., description="Server ID")

    def __str__(self) -> str:
        return (
            f"EvaluateResultHistory(evaluate_flow_seq={self.evaluate_flow_seq}, "
            + f"evaluate_result_type_seq={self.evaluate_result_type_seq}, "
            + f"result_value={self.result_value}, "
            + f"node_id={self.node_id}, "
            + f"server_id={self.server_id})"
        )
