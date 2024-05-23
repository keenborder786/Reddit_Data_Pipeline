FROM apache/airflow:2.7.1-python3.11

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev openjdk-11-jdk procps && \
    apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV SPARK_VERSION=3.5.1
ENV SPARK_MAJOR_VERSION=3.5
# Download Spark
RUN mkdir -p ${SPARK_HOME} \
 && curl https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark-${SPARK_VERSION}-bin-hadoop3.tgz \
 && tar xvzf spark-${SPARK_VERSION}-bin-hadoop3.tgz --directory /opt/spark --strip-components 1 \
 && rm -rf spark-${SPARK_VERSION}-bin-hadoop3.tgz
 ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"
 RUN chmod u+x /opt/spark/sbin/* && \
 chmod u+x /opt/spark/bin/*
# Download iceberg spark runtime
ENV ICEBERG_VERSION=1.5.2
RUN mkdir -p /home/iceberg/localwarehouse /home/iceberg/notebooks /home/iceberg/warehouse /home/iceberg/spark-events /home/iceberg
RUN curl https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12/${ICEBERG_VERSION}/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12-${ICEBERG_VERSION}.jar -Lo /opt/spark/jars/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12-${ICEBERG_VERSION}.jar

# Add iceberg spark runtime jar to IJava classpath
ENV IJAVA_CLASSPATH=/opt/spark/jars/*
COPY /spark/.pyiceberg.yaml /root/.pyiceberg.yaml

USER airflow
COPY requirements.txt /opt/airflow/
RUN rm ~/.cache/pip -rf
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt