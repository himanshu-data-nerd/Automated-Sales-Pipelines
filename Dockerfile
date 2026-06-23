FROM apache/airflow:2.8.1

USER root

# Java 17 is required for Apache Spark
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless && \
    apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow

RUN pip install pyspark
