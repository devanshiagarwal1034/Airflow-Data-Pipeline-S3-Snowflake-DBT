from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

# DAG definition
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "email": ["<your_email_id>"],
}

def extract_from_s3(**kwargs):
    s3 = S3Hook(aws_conn_id='aws_s3_connection')
    # Replace with your bucket and key
    bucket_name = "airflow-buckets"
    key = "booking_details_raw.csv"
    
    file_content = s3.read_key(key, bucket_name)
    kwargs['ti'].xcom_push(key='file_content', value=file_content)

def transform_data(**kwargs):
    file_content = kwargs['ti'].xcom_pull(key='file_content')
    # Example: Split the file content into columns. Assuming file_content is CSV data.
    # Here, we'll mock the data transformation and split it for demonstration.
    rows = file_content.split('\n')
    # For simplicity, assuming the first row has the column names, and the second row has the data.
    transformed_data = []
    for row in rows[1:]:
        columns = row.split(',')  # Assuming CSV format
        # Insert each column as a separate value (8 values for 8 columns)
        if len(columns) == 8:  # Ensure there are 8 columns
            transformed_data.append([
                int(columns[0]),  # BOOKING_ID as integer
                int(columns[1]),  # CUSTOMER_ID as integer
                columns[2],       # BOOKING_DATE as string
                columns[3],       # BOOKING_TIME as string
                columns[4],       # DESTINATION_TYPE as string
                float(columns[5]), # AMOUNT_SPENT as float
                columns[6],       # CURRENCY_CODE as string
                columns[7],       # STATUS as string
            ])

    kwargs['ti'].xcom_push(key='transformed_data', value=transformed_data)

def load_to_snowflake(**kwargs):
    transformed_data = kwargs['ti'].xcom_pull(key='transformed_data')
    snowflake = SnowflakeHook(snowflake_conn_id='airflow_snowflake_conn')
    conn = snowflake.get_conn()
    cursor = conn.cursor()
    for row in transformed_data:
        cursor.execute("""
            INSERT INTO travel_db.airflow.bookings_details_raw 
            (BOOKING_ID, CUSTOMER_ID, BOOKING_DATE, BOOKING_TIME, DESTINATION_TYPE, AMOUNT_SPENT, CURRENCY_CODE, STATUS) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, row)

with DAG(
    "hooks_s3_snowflake",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2024, 11, 26),
) as dag:

    with TaskGroup("extract_and_transform") as extract_and_transform:
        extract_task = PythonOperator(
            task_id="extract_from_s3",
            python_callable=extract_from_s3,
        )

        transform_task = PythonOperator(
            task_id="transform_data",
            python_callable=transform_data,
        )

        extract_task >> transform_task

    load_task = PythonOperator(
        task_id="load_to_snowflake",
        python_callable=load_to_snowflake,
    )

    email_task = EmailOperator(
        task_id="send_email",
        to="<your_email_id>",
        subject="ETL Workflow Completed",
        html_content="The ETL workflow has completed successfully.",
    )

    extract_and_transform >> load_task >> email_task
