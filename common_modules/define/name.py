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

# Prefect Varaiables
PREFECT_POSTGRES_AFTER_DAYS_NAME = "prefect_postrgres_after_days"
MARIADB_AFTER_DAYS_NAME = "mariadb_after_days"
