# prefect-metric-watcher

# Before you start
# How to create work-pool
```
prefect work-pool create METRIC_WATCHER_POOL -t docker
prefect work-pool create POSTGRESQL_MANAGER_POOL -t docker
prefect work-pool create MARIADB_MANAGER_POOL -t docker
```

# How to create work-queue
```
prefect work-queue create METRIC_WATCHER_QUEUE -p METRIC_WATCHER_POOL
prefect work-queue create POSTGRESQL_MANAGER_QUEUE -p POSTGRESQL_MANAGER_POOL
prefect work-queue create MARIADB_MANAGER_QUEUE -p MARIADB_MANAGER_POOL
```

# Deploy your flow (You need to run project home)
```
python3.11 app/deployments/postgres_clean_deployment.py
python3.11 app/deployments/mariadb_clean_deployment.py
python3.11 app/deployments/cpu_used_percent_deployment.py
python3.11 app/deployments/memory_used_percent_deployment.py
```

# Run flow in POSTGRESQL_MANAGER_POOL
```
> vim /etc/systemd/system/prefect_postgres_clean_flow.service
[Unit]
Description=Prefect PostgreSQL Clean Worker
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/.prefect
ExecStart=/usr/local/bin/prefect worker start --pool POSTGRESQL_MANAGER_POOL --work-queue POSTGRESQL_MANAGER_QUEUE
Restart=always
RestartSec=10
KillMode=process
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target

> systemctl daemon-reload
> systemctl enable prefect_postgres_clean_flow
> systemctl start prefect_postgres_clean_flow
```

# Run flow in MARIADB_MANAGER_POOL
```
> vim /etc/systemd/system/prefect_mariadb_clean_flow.service
[Unit]
Description=Prefect MariaDB Clean Worker
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/.prefect
ExecStart=/usr/local/bin/prefect worker start --pool MARIADB_MANAGER_POOL --work-queue MARIADB_MANAGER_QUEUE
Restart=always
RestartSec=10
KillMode=process
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target

> systemctl daemon-reload
> systemctl enable prefect_mariadb_clean_flow
> systemctl start prefect_mariadb_clean_flow
```

# Run flows in METRIC_WATCHER_POOL
```
> vim /etc/systemd/system/prefect_metric_watcher_flow.service 
[Unit]
Description=Prefect Cpu Used Percent Worker
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/.prefect
ExecStart=/usr/local/bin/prefect worker start --pool METRIC_WATCHER_POOL --work-queue METRIC_WATCHER_QUEUE
Restart=always
RestartSec=10
KillMode=process
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target

> systemctl daemon-reload
> systemctl enable prefect_metric_watcher_flow
> systemctl start prefect_metric_watcher_flow
```