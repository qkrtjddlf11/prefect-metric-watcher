from prefect import flow


@flow(log_prints=True)
def hello_flow(name: str):
    print(f"Hello {name}")
