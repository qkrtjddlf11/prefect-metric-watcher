# prefect-metric-watcher

# Before you start
# How to create work-pool
> prefect work-pool create METRIC_WATCHER_POOL -t prefect-agent

# How to create work-queue
> prefect work-queue create METRIC_WATCHER_CPU_QUEUE -p METRIC_WATCHER_POOL

# Build docker image
> /bin/sh docker-build-dev.sh

# Run docker
> docker run -d --name metric_watcher_cpu_agent -e PREFECT_API_URL='http://172.30.1.150:14200/api' prefect-metric-watcher:v0.0.1 prefect agent start -p METRIC_WATCHER_POOL -q METRIC_WATCHER_CPU_QUEUE --limit 3