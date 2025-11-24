from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from airflow.models import Variable 
from datetime import datetime, timedelta
import requests 

# --- NEW: Define the Alert Function ---
def send_slack_alert(context):
    # 1. Getting the Secret URL from Airflow Variables
    webhook_url = Variable.get("slack_webhook_url")
    
    # 2. Get details about the failure from the 'context'
    task_instance = context.get('task_instance')
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    execution_date = context.get('execution_date')
    
    # 3. Craft the Message
    slack_data = {
        "text": f"""
        *Critical Failure Detected* 
        *DAG:* {dag_id}
        *Task:* {task_id}
        *Time:* {execution_date}
        *Status:* Failed 
        _Check logs immediately._
        """
    }
    
    # 4. Sending it
    response = requests.post(webhook_url, json=slack_data)
    print(f"Slack Notification Sent. Status Code: {response.status_code}")

# Default settings
default_args = {
    'owner': 'himanshu',
    'retries': 0, 
    'retry_delay': timedelta(minutes=1),
    'on_failure_callback': send_slack_alert 
}

with DAG(
    dag_id='automated_sales_pipeline',
    default_args=default_args,
    start_date=datetime(2023, 11, 21),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task 1: Sensor 
    wait_for_file = FileSensor(
        task_id='wait_for_incoming_data',
        filepath='/opt/airflow/data/incoming/sales_data.csv',
        fs_conn_id='fs_default',
        poke_interval=30,
        timeout=60 * 60
    )

    # Task 2: Spark (BROKEN ON PURPOSE to test Slack)
    trigger_spark_etl = BashOperator(
        task_id='trigger_spark_job',
        bash_command='python /opt/airflow/dags/process_sales.py'
    )

    # Task 3: Archive
    archive_file = BashOperator(
        task_id='archive_processed_file',
        bash_command='mv /opt/airflow/data/incoming/sales_data.csv /opt/airflow/data/archive/sales_data_$(date +%Y%m%d%H%M%S).csv'
    )

    wait_for_file >> trigger_spark_etl >> archive_file