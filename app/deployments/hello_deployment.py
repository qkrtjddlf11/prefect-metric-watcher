# pylint: disable=C0114, C0115, C0116, C0413, C0412
# coding: utf-8
import os
import sys

from prefect import Flow
from prefect.client.schemas.schedules import CronSchedule
from prefect.docker.docker_image import DockerImage
from prefect_aws.s3 import S3Bucket
from prefect_docker.worker import ImagePullPolicy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.define.flows import MetricWatcher
from app.core.define.prefect import Blocks
from app.flows.hello import hello_flow

VERSION = "v0.0.1"


if __name__ == "__main__":
    s3_bucket = S3Bucket.load(Blocks.S3Bucket.MINIO_STORAGE_CODE_NAME)

    hello_flow_from_source: Flow = hello_flow.from_source(
        source=s3_bucket,
        entrypoint="app/flows/hello_flow.py:hello_flow",
    )

    hello_flow_uuid = hello_flow_from_source.deploy(
        name=f"{MetricWatcher.Flows.HELLO_FLOW_NAME}_deployment",
        image=DockerImage(
            name="prefect-metric-watcher", tag=VERSION, dockerfile="Dockerfile"
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
        tags=[MetricWatcher.Flows.HELLO_FLOW_NAME],
        work_pool_name=MetricWatcher.POOL_NAME,
        work_queue_name=MetricWatcher.QUEUE_NAME,
        schedule=CronSchedule(cron="* * * * *", timezone="UTC"),
        description="Test deployment for Infrastructure Docker Container based flow",
    )

    print(f"{MetricWatcher.Flows.HELLO_FLOW_NAME}_uuid: {hello_flow_uuid}")
