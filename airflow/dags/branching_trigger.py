from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from datetime import datetime

# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,  
    "email_on_failure": True,
    "email_on_retry": False,
    "email": ["devanshiec1034@gmail.com"],
}

def check_file_exists():
    #Check if the sales data file exists in the S3 bucket.
    s3_hook = S3Hook(aws_conn_id="aws_s3_connection")
    bucket_name = "airflow-buckets"
    file_key = "booking_details_raw.csv"
    
    # Check if the file exists
    if s3_hook.check_for_key(file_key, bucket_name):
        return 'process_etl'
    else:
        return 'send_alert_email'

def process_etl():
    print("Processing the ETL for sales data.")
    
    
def send_alert_email(**kwargs):
    #Send an email alert if the file is missing.
    send_email = EmailOperator(
        task_id='send_email',
        to="devanshiec1034@gmail.com",
        subject="Booking Data Missing",
        html_content="The booking details file for today is missing from the S3 bucket.",
    )
    send_email.execute(context=kwargs)

with DAG(
    "branching_and_trigger",
    default_args=default_args,
    description="Monitor and process daily booking data",
    schedule_interval="@daily",  # Run every day
    start_date=days_ago(1),  # Start one day ago for testing
    catchup=False,  # Don't run for past days, only run for today's execution
) as dag:

    # Task A: Check if the file exists
    check_file_task = PythonOperator(
        task_id="check_file_exists",
        python_callable=check_file_exists,
        provide_context=True,  # Make sure to pass the context for XComs
    )

    # Branching: Process ETL or send email based on file existence
    branching_task = BranchPythonOperator(
        task_id="branching",
        python_callable=check_file_exists,
        provide_context=True,
    )

    # ETL processing task (only runs if file exists)
    process_etl_task = PythonOperator(
        task_id="process_etl",
        python_callable=process_etl,
        provide_context=True,
        trigger_rule="all_success",  # Ensure this task runs only if the branching task succeeds
    )

    # Email alert task (only runs if the file does not exist)
    send_alert_email_task = PythonOperator(
        task_id="send_alert_email",
        python_callable=send_alert_email,
        provide_context=True,
        trigger_rule="all_success",  # Ensure this task runs only if the branching task succeeds
    )

    # Setting up the workflow
    check_file_task >> branching_task
    branching_task >> process_etl_task
    branching_task >> send_alert_email_task
