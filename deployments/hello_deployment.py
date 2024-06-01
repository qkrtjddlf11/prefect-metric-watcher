# pylint: disable=C0114, C0115, C0116, C0413
# coding: utf-8
import os
import sys

from prefect import Flow, get_run_logger
from prefect.blocks.system import Secret
from prefect.runner.storage import RemoteStorage
from prefect.server.schemas.schedules import CronSchedule

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from common_modules.define.name import (
    HELLO_SCHEDULER_NAME,
    METRIC_WATCHER_POOL_NAME,
    METRIC_WATCHER_QUEUE_NAME,
)
from flows.hello import hello_flow


def get_remote_storage() -> RemoteStorage:
    storage = RemoteStorage(
        url="s3://prefect-metric-watcher/my-folder",
        # Use Secret blocks to keep credentials out of your code
        key=Secret.load("prefect-metric-watcher-access-key").get(),
        secret=Secret.load("prefect-metric-watcher-secret-key").get(),
    )
    storage.pull_code()

    return storage


if __name__ == "__main__":
    hello_flow_from_source: Flow = hello_flow.from_source(
        source=get_remote_storage(), entrypoint=""
    )
    hello_flow_uuid = hello_flow_from_source.deploy(
        name=f"run_{HELLO_SCHEDULER_NAME}_flow",
        tags=[HELLO_SCHEDULER_NAME],
        work_pool_name=METRIC_WATCHER_POOL_NAME,
        work_queue_name=METRIC_WATCHER_QUEUE_NAME,
        schedule=[CronSchedule(cron="* * * * *", timezone="UTC")],
        is_schedule_active=True,
        description="Test deployment for Infrastructure Docker Container based flow",
    )

    logger = get_run_logger()
    logger.info(f"{HELLO_SCHEDULER_NAME}_uuid: {hello_flow_uuid}")
