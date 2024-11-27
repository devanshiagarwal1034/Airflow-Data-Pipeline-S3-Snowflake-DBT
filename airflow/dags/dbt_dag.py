from airflow import DAG
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='dbt_cloud_trigger_job',
    default_args=default_args,
    description='Trigger a DBT Cloud job from Airflow',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # DBT Cloud Operator to trigger the job
    run_dbt_job = DbtCloudRunJobOperator(
        task_id='trigger_dbt_cloud_job',
        dbt_cloud_conn_id='dbt_cloud_default',  # Airflow connection ID for DBT Cloud
        job_id=70471823399300,  
        check_interval=10,  # Time interval (in seconds) between status checks
        timeout=300,  # Maximum wait time (in seconds) for the job to complete
    )

    run_dbt_job
