import pandas as pd
from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import io

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "email": ["<your_email_id>"],
}

@task()
def extract_from_s3(bucket_name: str, key: str):
    #Extract data from S3 (CSV file)
    s3 = S3Hook(aws_conn_id="aws_s3_connection")
    file_content = s3.read_key(key, bucket_name)
    
    # Read CSV from the S3 file content into a pandas DataFrame
    csv_data = io.StringIO(file_content)  # Convert byte content to a string buffer
    df = pd.read_csv(csv_data)
    
    return df

@task()
def transform_data(df):
    #Transform the extracted data
    # Example transformation: Convert all column names to uppercase
    df.columns = [col.upper() for col in df.columns]
    
    # Example transformation: Perform data transformation, such as capitalizing all string values
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
    
    return df

@task()
def load_to_snowflake(df):
    #Load the transformed data into Snowflake
    snowflake = SnowflakeHook(snowflake_conn_id='airflow_snowflake_conn')
    conn = snowflake.get_conn()
    cursor = conn.cursor()
    
    # Iterate over the DataFrame rows and insert them into Snowflake
    for index, row in df.iterrows():
        cursor.execute(
           """
            INSERT INTO travel_db.airflow.bookings_details_raw 
            (BOOKING_ID, CUSTOMER_ID, BOOKING_DATE, BOOKING_TIME, DESTINATION_TYPE, AMOUNT_SPENT, CURRENCY_CODE, STATUS) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [row['BOOKING_ID'], row['CUSTOMER_ID'], row['BOOKING_DATE'], row['BOOKING_TIME'],row['DESTINATION_TYPE'], row['AMOUNT_SPENT'], row['CURRENCY_CODE'], row['STATUS']]
        )
    print("Data loaded into Snowflake.")

with DAG(
    "taskflow_etl_project",
    default_args=default_args,
    description="A simple ETL process using TaskFlow API with CSV",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task Definitions
    bucket_name = "airflow-buckets"
    key = "booking_details_raw.csv"

    # Extract
    extracted_data = extract_from_s3(bucket_name, key)

    # Transform
    transformed_data = transform_data(extracted_data)

    # Load
    load_to_snowflake(transformed_data)
