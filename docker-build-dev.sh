#!/bin/bash
docker stop `docker ps | grep -v CONTAINER | awk '{print $1}'`
docker rm `docker ps -a | grep -v CONTAINER | awk '{print $1}'`

docker build --force-rm -f Dockerfile -t prefect-metric-watcher:v0.0.8 .

docker run -d --name metric_watcher_cpu_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8prefect agent start -p METRIC_WATCHER_POOL -q METRIC_WATCHER_CPU_QUEUE --limit 3  
docker run -d --name metric_watcher_memory_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8prefect agent start -p METRIC_WATCHER_POOL -q METRIC_WATCHER_MEMORY_QUEUE --limit 3  
docker run -d --name metric_watcher_disk_root_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8prefect agent start -p METRIC_WATCHER_POOL -q METRIC_WATCHER_DISK_ROOT_QUEUE --limit 3  
docker run -d --name metric_watcher_postgres_management_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8prefect agent start -p METRIC_WATCHER_POSTGRES_MANAGEMENT_POOL -q METRIC_WATCHER_POSTGRES_MANAGEMENT_QUEUE --limit 1  
docker run -d --name metric_watcher_mariadb_management_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8prefect agent start -p METRIC_WATCHER_MARIADB_MANAGEMENT_POOL -q METRIC_WATCHER_MARIADB_MANAGEMENT_QUEUE --limit 1  
