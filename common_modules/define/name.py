# pylint: disable=C0114, C0115, C0116
# coding: utf-8

# Configuration
BASE_CONFIG_PATH = "config/config_dev.yaml"

# Scheduler Name
POSTGRES_SCHEDULER_NAME = "prefect_postgresql_cleanup_scheduler"
MARIADB_SCHEDULER_NAME = "mariadb_cleanup_scheduler"
METRIC_CPU_SCHEDULER_NAME = "prefect_metric_cpu_scheduler"
METRIC_MEMORY_SCHEDULER_NAME = "prefect_metric_memory_scheduler"
METRIC_DISK_ROOT_SCHEDULER_NAME = "prefect_metric_disk_root_scheduler"
HELLO_SCHEDULER_NAME = "prefect_hello_scheduler"


# Prefect Varaiables
PREFECT_POSTGRES_AFTER_DAYS_NAME = "prefect_postrgres_after_days"
MARIADB_AFTER_DAYS_NAME = "mariadb_after_days"

# Common valuables
POINT_TIME_NAME = "time"
POINT_HOST_NAME = "host"

POINT_USED_PERCENT = "used_percent"
POINT_USAGE_PERCENT = "usage_percent"

# Pool Name
METRIC_WATCHER_POOL_NAME = "METRIC_WATCHER_POOL"
METRIC_WATCHER_DOCKER_POOL_NAME = "METRIC_WATCHER_DOCKER_POOL"

# Queue Name
METRIC_WATCHER_QUEUE_NAME = "METRIC_WATCHER_QUEUE"
METRIC_WATCHER_DOCKER_QUEUE_NAME = "METRIC_WATCHER_DOCKER_QUEUE"


class PrefectBlockName:
    CODE_STORAGE_URL: str = "code-storage-url"
    CODE_STORAGE_ACCESS_KEY: str = "code-storage-access-key"
    CODE_STORAGE_SECRET_KEY: str = "code-storage-secret-key"

    GITHUB_URL: str = "github-url"
    GITHUB_ACCESS_TOKEN: str = "github-access-token"
