class CpuUsedPercent:
    class Tasks:
        GET_CPU_POINTS_NAME: str = "get_cpu_points"
        COMPARE_CPU_USED_PERCENT_NAME: str = "compare_cpu_used_percent"


class MariadbClean:
    class Tasks:
        CLEANUP_MARIADB_TABLES_NAME: str = "cleanup_mariadb_tables"


class PostgresClean:
    class Tasks:
        CLEANUP_POSTGRESQL_TABLES_NAME: str = "cleanup_postgresql_tables"
