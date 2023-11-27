#!/bin/bash
docker stop `docker ps | grep -v CONTAINER | awk '{print $1}'`
docker rm `docker ps -a | grep -v CONTAINER | awk '{print $1}'`

docker build --force-rm -f Dockerfile -t prefect-metric-watcher:v0.0.4 .
