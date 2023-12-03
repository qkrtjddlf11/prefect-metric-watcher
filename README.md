# prefect-metric-watcher

# Before you start
# How to create work-pool
prefect work-pool create METRIC_WATCHER_POOL -t prefect-agent  
prefect work-pool create METRIC_WATCHER_POSTGRES_MANAGEMENT_POOL -t prefect-agent  
prefect work-pool create METRIC_WATCHER_MARIADB_MANAGEMENT_POOL -t prefect-agent  

# How to create work-queue
prefect work-queue create METRIC_WATCHER_CPU_QUEUE -p METRIC_WATCHER_POOL  
prefect work-queue create METRIC_WATCHER_MEMORY_QUEUE -p METRIC_WATCHER_POOL  
prefect work-queue create METRIC_WATCHER_POSTGRES_MANAGEMENT_QUEUE -p METRIC_WATCHER_POSTGRES_MANAGEMENT_POOL  
prefect work-queue create METRIC_WATCHER_MARIADB_MANAGEMENT_QUEUE -p METRIC_WATCHER_MARIADB_MANAGEMENT_POOL  

# Build docker image
/bin/sh docker-build-dev.sh  

# Run docker
docker run -d --name metric_watcher_cpu_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.6 prefect agent start -p METRIC_WATCHER_POOL -q METRIC_WATCHER_CPU_QUEUE --limit 3  
docker run -d --name metric_watcher_memory_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.6 prefect agent start -p METRIC_WATCHER_POOL -q METRIC_WATCHER_MEMORY_QUEUE --limit 3  
docker run -d --name metric_watcher_postgres_management_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.6 prefect agent start -p METRIC_WATCHER_POSTGRES_MANAGEMENT_POOL -q METRIC_WATCHER_POSTGRES_MANAGEMENT_QUEUE --limit 1  
docker run -d --name metric_watcher_mariadb_management_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.6 prefect agent start -p METRIC_WATCHER_MARIADB_MANAGEMENT_POOL -q METRIC_WATCHER_MARIADB_MANAGEMENT_QUEUE --limit 1  
