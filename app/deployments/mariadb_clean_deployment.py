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

from app.core.define.flows import MariaDBManager
from app.core.define.prefect import Blocks
from app.flows.mariadb_clean import mariadb_clean_flow

VERSION = "v0.0.1"


if __name__ == "__main__":
    s3_bucket = S3Bucket.load(Blocks.S3Bucket.MINIO_STORAGE_CODE_NAME)

    from_source: Flow = mariadb_clean_flow.from_source(
        source=s3_bucket,
        entrypoint="app/flows/mariadb_clean.py:mariadb_clean_flow",
    )

    flow_name = MariaDBManager.Flows.MARIADB_CLEAN_FLOW_NAME

    flow_uuid = from_source.deploy(
        name=f"{flow_name}_deployment",
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
        tags=[flow_name],
        work_pool_name=MariaDBManager.POOL_NAME,
        work_queue_name=MariaDBManager.QUEUE_NAME,
        schedule=CronSchedule(cron="0 4 * * *", timezone="UTC"),
        description="Docker-based infrastructure flow for MariaDB cleanup.",
    )

    print(f"{flow_name}_uuid: {flow_uuid}")
