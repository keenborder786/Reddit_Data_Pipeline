FROM apache/airflow:2.2.3-python3.9

COPY requirements.txt /opt/airflow/

USER root
RUN apt-get update && apt-get install -y gcc python3-dev

USER airflow
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt