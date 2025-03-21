from sqlalchemy import TIMESTAMP, BigInteger, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import registry

mapper_registry = registry()


@mapper_registry.mapped
class TAlertGmail:
    __tablename__ = "t_alert_gmail"

    alert_gmail_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Alert gmail sequence"
    )
    alert_type_seq = Column(
        Integer,
        ForeignKey("t_code_alert_type.alert_type_seq"),
        nullable=False,
        comment="Alert type sequence",
    )
    evaluate_flow_seq = Column(
        Integer,
        ForeignKey("t_evaluate_flow.evaluate_flow_seq"),
        nullable=False,
        comment="Evaluate flow sequence",
    )
    gmail_from = Column(String(50), nullable=False, comment="Gmail Sender")
    gmail_to = Column(String(50), nullable=False, comment="Gmail Receiver")
    gmail_app_password = Column(
        String(16), nullable=False, comment="Gmail app password"
    )
    deleted_yn = Column(
        String(1), nullable=False, default="N", comment="Alert gmail deleted or not"
    )
    reg_datetime = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        comment="Alert gmail register datetime",
    )
    upd_datetime = Column(
        TIMESTAMP,
        nullable=True,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="Alert gmail update datetime",
    )
    description = Column(String(100), nullable=True, comment="Alert gmail description")


@mapper_registry.mapped
class TCodeAlertType:
    __tablename__ = "t_code_alert_type"

    alert_type_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Alert type sequence"
    )
    name = Column(String(20), nullable=False, comment="Alert type name")


@mapper_registry.mapped
class TCodeAlertSendResultType:
    __tablename__ = "t_code_alert_send_result_type"

    alert_send_result_type_seq = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Alert send result type sequence",
    )
    name = Column(
        String(10),
        nullable=False,
        default="PENDING",
        comment="Alert send result type name",
    )
    description = Column(
        String(100), nullable=True, comment="Alert send result type description"
    )


@mapper_registry.mapped
class TEvaluateFlow:
    __tablename__ = "t_evaluate_flow"

    evaluate_flow_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Flow sequence"
    )
    name = Column(String(50), nullable=False, comment="Flow name")
    metric_type_seq = Column(
        Integer,
        ForeignKey("t_code_metric_type.metric_type_seq"),
        nullable=False,
        comment="Metric type sequence",
    )
    comparison_operator_type_seq = Column(
        Integer,
        ForeignKey("t_code_comparison_operator_type.comparison_operator_type_seq"),
        nullable=False,
        comment="Comparison operator type sequence",
    )
    evaluate_value = Column(
        BigInteger, nullable=False, default=80, comment="Flow evaluate value"
    )
    evaluate_target_type_seq = Column(
        Integer,
        ForeignKey("t_code_evaluate_target_type.evaluate_target_type_seq"),
        nullable=False,
        comment="Evaluate target type sequence",
    )
    deleted_yn = Column(
        String(1), nullable=False, default="N", comment="Evaluate flow deleted or not"
    )
    reg_datetime = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        comment="Evaluate flow register datetime",
    )
    upd_datetime = Column(
        TIMESTAMP,
        nullable=True,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="Evaluate flow update datetime",
    )
    description = Column(
        String(100), nullable=True, comment="Evaluate flow description"
    )


@mapper_registry.mapped
class TCodeEvaluateResultType:
    __tablename__ = "t_code_evaluate_result_type"

    evaluate_result_type_seq = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Evaluate result type sequence",
    )
    name = Column(
        String(10),
        nullable=False,
        comment="Evalueate result type name",
    )
    description = Column(
        String(100), nullable=True, comment="Evaluate result type description"
    )


@mapper_registry.mapped
class TEvaluateResultHistory:
    __tablename__ = "t_evaluate_result_history"

    alert_history_seq = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="Alert history sequence",
    )
    evaluate_flow_seq = Column(
        Integer,
        ForeignKey("t_evaluate_flow.evaluate_flow_seq"),
        nullable=False,
        comment="Evaluate flow sequence",
    )
    evaluate_result_type_seq = Column(
        Integer,
        ForeignKey("t_code_evaluate_result_type.evaluate_result_type_seq"),
        nullable=False,
        comment="Evaluate result type sequence",
    )
    result_value = Column(BigInteger, nullable=False, comment="Result value")
    node_id = Column(
        String(10), ForeignKey("t_node.node_id"), nullable=False, comment="Node id"
    )
    server_id = Column(
        String(10),
        ForeignKey("t_server.server_id"),
        nullable=False,
        comment="Server id",
    )
    reg_datetime = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        comment="Evaluate result register datetime",
    )


@mapper_registry.mapped
class TCodeComparisonOperatorType:
    __tablename__ = "t_code_comparison_operator_type"

    comparison_operator_type_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Operator type sequence"
    )
    name = Column(String(2), nullable=False, comment="Operator")
    description = Column(String(50), nullable=False, comment="Operator name")


@mapper_registry.mapped
class TCodeMetricType:
    __tablename__ = "t_code_metric_type"

    metric_type_seq = Column(
        Integer, primary_key=True, autoincrement=True, comment="Metric type sequence"
    )
    name = Column(String(50), nullable=False, comment="Metric type name")
    description = Column(String(100), nullable=True, comment="Metric type description")


@mapper_registry.mapped
class TCodeEvaluateTargetType:
    __tablename__ = "t_code_evaluate_target_type"

    evaluate_target_type_seq = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Evaluate target type sequence",
    )
    name = Column(String(10), nullable=False, comment="Evaluate target type name")
    description = Column(
        String(100), nullable=True, comment="Evaluate target type description"
    )


@mapper_registry.mapped
class TNode:
    __tablename__ = "t_node"

    node_id = Column(String(5), primary_key=True, comment="Node id")
    name = Column(String(20), nullable=False, comment="Node name")
    deleted_yn = Column(
        String(1), nullable=False, default="N", comment="Node deleted or not"
    )
    reg_datetime = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        comment="Node register datetime",
    )
    upd_datetime = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="Node update datetime",
    )
    description = Column(String(100), nullable=True, comment="Node description")


@mapper_registry.mapped
class TServer:
    __tablename__ = "t_server"

    server_id = Column(String(10), primary_key=True, comment="Server ID")
    node_id = Column(String(5), ForeignKey("t_node.node_id"), nullable=False)
    name = Column(String(20), nullable=False, unique=True, comment="Server hostname")
    deleted_yn = Column(
        String(1), nullable=False, default="N", comment="Server deleted or not"
    )
    reg_datetime = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="Server register datetime",
    )
    upd_datetime = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="Server update datetime",
    )
    description = Column(String(100), nullable=True, comment="Server description")
