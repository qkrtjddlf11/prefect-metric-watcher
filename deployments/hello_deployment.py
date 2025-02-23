# pylint: disable=C0114, C0115, C0116, C0413, C0412
# coding: utf-8
import os
import sys

from prefect import Flow
from prefect.blocks.system import Secret, String
from prefect.client.schemas.schedules import CronSchedule
from prefect.deployments.runner import DeploymentImage
from prefect.docker.docker_image import DockerImage
from prefect.runner.storage import GitRepository
from prefect_docker.worker import ImagePullPolicy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from common_modules.define.name import (
    HELLO_SCHEDULER_NAME,
    METRIC_WATCHER_DOCKER_POOL_NAME,
    METRIC_WATCHER_DOCKER_QUEUE_NAME,
    PrefectBlockName,
)
from flows.hello import hello_flow

if __name__ == "__main__":
    # TODO
    # Private Registry를 운영중이라면 push를 True로 바꾸고
    # job_variables에서 Registry 정보를 넣어주면 Image Build와 Push를 한줄의 명령어로 가능하다. (현재는 로컬 장비에 빌드만 수행)
    with open("VERSION", mode="r", encoding="utf-8") as f:
        version = f.readline().strip()

    hello_flow_from_source: Flow = hello_flow.from_source(
        source=GitRepository(
            url=String.load(PrefectBlockName.GITHUB_URL).value,
            credentials={
                "access_token": Secret.load(PrefectBlockName.GITHUB_ACCESS_TOKEN)
            },
        ),
        entrypoint="flows/hello.py:hello_flow",
    )

    hello_flow_uuid = hello_flow_from_source.deploy(
        name=f"run_{HELLO_SCHEDULER_NAME}_flow",
        image=DeploymentImage(
            name="prefect-metric-watcher", dockerfile="Dockerfile", tag=version
        ),
        build=True,
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
