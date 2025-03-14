from pydantic import BaseModel, Field


class BasePoint(BaseModel):
    time: str = Field(..., description="Point time")
    server_id: str = Field(..., description="Telegraf server_id")
    node_id: str = Field(..., description="Telegraf node_id")


class UsedPercentPoint(BasePoint):
    usage_percent: float = Field(..., description="CPU usage percent")

    def __str__(self):
        return (
            f"UsedPercentPoint(time={self.time}, "
            + f"server_id={self.server_id}, "
            + f"node_id={self.node_id}, "
            + f"usage_percent={self.usage_percent})"
        )
