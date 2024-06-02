FROM prefecthq/prefect:2.19.3-python3.11

COPY requirements.txt .

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

ADD common_modules /opt/prefect/common_modules
ADD config /opt/prefect/config
ADD deployments /opt/prefect/deployments
ADD flows /opt/prefect/flows