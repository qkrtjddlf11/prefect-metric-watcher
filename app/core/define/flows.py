class MetricWatcher:
    POOL_NAME: str = "METRIC_WATCHER_POOL"
    QUEUE_NAME: str = "METRIC_WATCHER_QUEUE"

    class Flows:
        HELLO_FLOW_NAME: str = "hello"
        CPU_USED_PERCENT_FLOW_NAME: str = "cpu_used_percent"
        MEMORY_USED_PERCENT_FLOW_NAME: str = "memory_used_percent"
        DISK_USED_PERCENT_ROOT_FLOW_NAME: str = "disk_used_percent_root"


class PostgreSQLManager:
    POOL_NAME: str = "POSTGRESQL_MANAGER_POOL"
    QUEUE_NAME: str = "POSTGRESQL_MANAGER_QUEUE"

    class Flows:
        POSTGRES_CLEAN_FLOW_NAME: str = "postgres_clean"


class MariaDBManager:
    POOL_NAME: str = "MARIADB_MANAGER_POOL"
    QUEUE_NAME: str = "MARIADB_MANAGER_QUEUE"

    class Flows:
        MARIADB_CLEAN_FLOW_NAME: str = "mariadb_clean"
