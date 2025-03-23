from pydantic import BaseModel, Field


class BasePoint(BaseModel):
    time: str = Field(..., description="Point time")
    server_id: str = Field(..., description="Telegraf server_id")
    node_id: str = Field(..., description="Telegraf node_id")


class CpuUsedPercentPoint(BasePoint):
    used_percent: float = Field(..., description="CPU used percent")

    def __str__(self):
        return (
            f"CpuUsedPercentPoint(time={self.time}, "
            + f"server_id={self.server_id}, "
            + f"node_id={self.node_id}, "
            + f"used_percent={self.used_percent})"
        )


class MemoryUsedPercentPoint(BasePoint):
    used_percent: float = Field(..., description="Memory used percent")

    def __str__(self):
        return (
            f"MemoryUsedPercentPoint(time={self.time}, "
            + f"server_id={self.server_id}, "
            + f"node_id={self.node_id}, "
            + f"used_percent={self.used_percent})"
        )


class DiskRootUsedPercentPoint(BasePoint):
    used_percent: float = Field(..., description="Disk root used percent")

    def __str__(self):
        return (
            f"DiskRootUsedPercentPoint(time={self.time}, "
            + f"server_id={self.server_id}, "
            + f"node_id={self.node_id}, "
            + f"used_percent={self.used_percent})"
        )
