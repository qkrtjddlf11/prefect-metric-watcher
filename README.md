# prefect-metric-watcher

# Before you start
# How to create work-pool
prefect work-pool create METRIC_WATCHER_POOL -t docker
prefect work-pool create POSTGRESQL_MANAGER_POOL -t docker

# How to create work-queue
prefect work-queue create METRIC_WATCHER_QUEUE -p METRIC_WATCHER_POOL
prefect work-queue create POSTGRESQL_MANAGER_QUEUE -p POSTGRESQL_MANAGER_POOL

# Deploy your flow (You need to run project home)
python3.11 app/deployments/hello_deployment.py
python3.11 app/deployments/postgres_clean_deployment.py


# Build docker image
/bin/sh docker-build-dev.sh  

# Run docker
docker run -d --name metric_watcher_cpu_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8 prefect agent start -p METRIC_WATCHER_POOL -q METRIC_WATCHER_CPU_QUEUE --limit 3  
docker run -d --name metric_watcher_memory_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8 prefect agent start -p METRIC_WATCHER_POOL -q METRIC_WATCHER_MEMORY_QUEUE --limit 3  
docker run -d --name metric_watcher_disk_root_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8 prefect agent start -p METRIC_WATCHER_POOL -q METRIC_WATCHER_DISK_ROOT_QUEUE --limit 3  
docker run -d --name metric_watcher_postgres_management_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8 prefect agent start -p METRIC_WATCHER_POSTGRES_MANAGEMENT_POOL -q METRIC_WATCHER_POSTGRES_MANAGEMENT_QUEUE --limit 1  
docker run -d --name metric_watcher_mariadb_management_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.8 prefect agent start -p METRIC_WATCHER_MARIADB_MANAGEMENT_POOL -q METRIC_WATCHER_MARIADB_MANAGEMENT_QUEUE --limit 1  
