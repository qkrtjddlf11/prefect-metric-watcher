# pylint: disable=C0114, C0115, C0116, C0413
# coding: utf-8
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from flows.mariadb_clean import MARIADB_SCHEDULER_NAME, mariadb_cleanup_flow

deployment = Deployment.build_from_flow(
    flow=mariadb_cleanup_flow,
    name="run_" + MARIADB_SCHEDULER_NAME + "_flow",
    tags=[MARIADB_SCHEDULER_NAME],
    version=1,
    work_pool_name="METRIC_WATCHER_MARIADB_MANAGEMENT_POOL",
    work_queue_name="METRIC_WATCHER_MARIADB_MANAGEMENT_QUEUE",
    path="/opt/prefect/",
    schedule=(CronSchedule(cron="0 0 * * *", timezone="UTC")),
)

if __name__ == "__main__":
    deployment.apply()
