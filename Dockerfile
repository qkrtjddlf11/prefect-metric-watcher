FROM prefecthq/prefect:2.14.4-python3.9

COPY requirements.txt .

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

ADD common_modules /opt/prefect/common_modules
ADD config /opt/prefect/config
ADD deployments /opt/prefect/deployments
ADD flows /opt/prefect/flows