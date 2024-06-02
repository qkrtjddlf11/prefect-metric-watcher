# pylint: disable=C0114, C0115, C0116, C0413
# coding: utf-8
import os
import sys

from prefect import Flow
from prefect.client.schemas.schedules import CronSchedule
from prefect.runner.storage import GitRepository
from prefect.blocks.system import Secret
from prefect_docker.worker import ImagePullPolicy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from common_modules.define.name import (
    HELLO_SCHEDULER_NAME,
    METRIC_WATCHER_DOCKER_POOL_NAME,
    METRIC_WATCHER_DOCKER_QUEUE_NAME,
)
from flows.hello import hello_flow


if __name__ == "__main__":
    hello_flow_from_source: Flow = hello_flow.from_source(
        source=GitRepository(
            url="https://github.com/qkrtjddlf11/prefect-metric-watcher.git",
            credentials={"access_token": Secret.load("github-access-token")},
        ),
        entrypoint="flows/hello.py:hello_flow",
    )

    hello_flow_uuid = hello_flow_from_source.deploy(
        name=f"run_{HELLO_SCHEDULER_NAME}_flow",
        image="prefecthq/prefect:2.19.3-python3.11",
        build=False,
        push=False,
        job_variables={
            "auto_remove": True,
            "image_pull_policy": ImagePullPolicy.IF_NOT_PRESENT,
            "privileged": True,
            "network_mode": "host",
        },
        parameters={"name": "Marvin"},
        tags=[HELLO_SCHEDULER_NAME],
        work_pool_name=METRIC_WATCHER_DOCKER_POOL_NAME,
        work_queue_name=METRIC_WATCHER_DOCKER_QUEUE_NAME,
        schedule=CronSchedule(cron="* * * * *", timezone="UTC"),
        is_schedule_active=True,
        description="Test deployment for Infrastructure Docker Container based flow",
    )

    print(f"{HELLO_SCHEDULER_NAME}_uuid: {hello_flow_uuid}")
