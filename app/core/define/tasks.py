# pylint: disable=C0114, C0115, C0116
# coding: utf-8


class MariadbClean:
    class Tasks:
        CLEANUP_MARIADB_TABLES_NAME: str = "cleanup_mariadb_tables"


class PostgresClean:
    class Tasks:
        CLEANUP_POSTGRESQL_TABLES_NAME: str = "cleanup_postgresql_tables"


class CpuUsedPercent:
    class Tasks:
        GET_CPU_POINTS_NAME: str = "get_cpu_points"
        COMPARE_CPU_USED_PERCENT_NAME: str = "compare_cpu_used_percent"


class MemoryUsedPercent:
    class Tasks:
        GET_MEMORY_POINTS_NAME: str = "get_memory_points"
        COMPARE_MEMORY_USED_PERCENT_NAME: str = "compare_memory_used_percent"


class DiskRootUsedPercent:
    class Tasks:
        GET_DISK_ROOT_POINTS_NAME: str = "get_disk_root_points"
        COMPARE_DISK_ROOT_USED_PERCENT_NAME: str = "compare_disk_root_used_percent"
