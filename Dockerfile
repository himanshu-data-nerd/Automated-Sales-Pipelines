# 1. Starting with the official Airflow image (The Base)
FROM apache/airflow:2.8.1

# 2. Switching to Root user (Boss Mode) to install system software
USER root

# 3. Updating Linux and installing Java (Required for Spark)
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk-headless && \
    apt-get clean

# 4. Telling the system where Java is located
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64

# 5. Switching back to the standard Airflow user (Safety Mode)
USER airflow

# 6. Installing the PySpark library for Python
RUN pip install pyspark pandas