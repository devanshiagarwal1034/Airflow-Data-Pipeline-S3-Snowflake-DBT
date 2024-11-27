from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.transfers.copy_into_snowflake import CopyFromExternalStageToSnowflakeOperator
from airflow.operators.email import EmailOperator

dag = DAG(
    's3_to_snowflake_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',
    catchup=False
)

# Wait for the file in S3
wait_for_file = S3KeySensor(
    task_id='wait_for_s3_file',
    bucket_name='airflow-buckets',
    bucket_key='customer_details_raw.csv',
    aws_conn_id='aws_s3_connection',
    poke_interval=10,
    timeout= 60 * 60 * 5,
    soft_fail=True,
    deferrable = True,
    dag=dag
)

#Truncate the table to ensure existing data is removed
truncate_table = SnowflakeOperator(
    task_id='truncate_customer_details_raw',
    sql="TRUNCATE TABLE travel_db.airflow.customer_details_raw;",
    snowflake_conn_id="airflow_snowflake_conn",
    autocommit=True,
    dag=dag
)
# Load the file from S3 to Snowflake
load_table = CopyFromExternalStageToSnowflakeOperator(
    task_id="load_s3_file_to_table",
    snowflake_conn_id="airflow_snowflake_conn",
    files=["customer_details_raw.csv"],
    table="travel_db.airflow.customer_details_raw",
    stage='my_s3_stage',
    file_format="(type = 'CSV',field_delimiter = ',', skip_header = 1)",
    dag=dag
)

#  Send email notification after loading data
send_email = EmailOperator(
    task_id='send_email_notification',
    to='<your_email_id>',  # Replace with the recipient's email
    subject='Snowflake Data Load Completed',
    html_content="""<h3>The data from S3 has been successfully loaded into Snowflake!</h3>
                    <p>Table: travel_db.airflow.customer_details_raw</p>
                    <p>File: customer_details_raw.csv</p>""",
    dag=dag
)
# Set the dependencies

wait_for_file >> truncate_table >> load_table >> send_email
