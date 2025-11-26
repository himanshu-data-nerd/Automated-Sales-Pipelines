# 🚀 Automated Event-Driven Data Platform

![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Spark](https://img.shields.io/badge/Apache%20Spark-3.8-orange)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-3.1-red)

A robust, scalable, and fault-tolerant **ETL Data Pipeline** designed to simulate a real-world enterprise data platform. This project automates the ingestion, transformation, and archival of sales data using an event-driven architecture.

---

## 🏗️ Architecture Overview

The system follows a **Bronze-Silver-Gold** data lake pattern tailored for high availability and fault tolerance.

1.  **Ingestion Layer (Sensor):** Airflow `FileSensor` monitors the landing zone (`data/incoming`) for new datasets.
2.  **Processing Layer (Spark Engine):** Triggers a **PySpark** job running on a custom Docker container (Java 17 + Python) to perform revenue calculations.
3.  **Storage Layer (Data Lake):**
    * **Bronze (Archive):** Raw files are timestamped and moved to cold storage for audit trails.
    * **Silver (Processed):** Cleaned and transformed data is stored for reporting.
4.  **Observability Layer (Alerting):** Integrated **Slack Webhooks** provide real-time notifications for any pipeline failures (Exit Code 1/2/137).

---

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestration** | Apache Airflow | Scheduling & Dependency Management |
| **Compute** | Apache Spark | Distributed Data Processing |
| **Containerization** | Docker / Compose | Environment Isolation |
| **Language** | Python | Core Logic |
| **Monitoring** | Slack API | Incident Response System |

---

## 🚀 Getting Started

Follow these instructions to deploy the platform on your local machine.

### **1. Prerequisites**
* Docker Desktop (Running)
* Git

### **2. Installation**

Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/automated-sales-pipeline.git
cd automated-sales-pipeline
```

### **3. Configuration**
The project uses a secure .env file for credentials.
 - Copy the template:
  ```bash
  cp .env.example .env
  ```
 - Open .env and add your Slack Webhook URL or SMTP Credentials.

### **4. Deployment**
 - Build the custom images and start the cluster:
  ```bash
  docker-compose up -d --build
  ```
 - *Wait for the containers (scheduler, webserver, postgres) to report "Healthy".*

## ⚡ How to Run the Pipeline

1. Access the UI: Go to http://localhost:8080 (User: admin / Pass: admin).

2. Activate DAG: Toggle ON the automated_sales_pipeline.

3. Trigger Event: Drop a CSV file into the ingress folder:
     Example Command (Windows/Linux)
     ```bash
     mv sales_data.csv data/incoming/
     ```
4. Observe:
   * The FileSensor detects the file immediately.
   * Spark processes the revenue data.
   * The raw file is moved to data/archive/ with a unique timestamp.
  
---

## 👤 Author

**Himanshu** *Aspiring Data Platform Engineer*
