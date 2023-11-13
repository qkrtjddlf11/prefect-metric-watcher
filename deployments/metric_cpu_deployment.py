# pylint: disable=C0114, C0115, C0116, C0413
# coding: utf-8
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from flows.metric_cpu import METRIC_CPU_NAME, metric_cpu_flow

deployment = Deployment.build_from_flow(
    flow=metric_cpu_flow,
    name="run_" + METRIC_CPU_NAME + "_flow",
    tags=[METRIC_CPU_NAME],
    version=1,
    work_pool_name="METRIC_WATCHER_POOL",
    work_queue_name="METRIC_WATCHER_CPU_QUEUE",
    path="/opt/prefect/",
    schedule=(CronSchedule(cron="* * * * *", timezone="UTC")),
)

if __name__ == "__main__":
    deployment.apply()
