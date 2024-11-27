# Airflow Project

### Overview

In this project, I’ve explored the powerful capabilities of Apache Airflow, gaining hands-on experience in workflow orchestration and integrating it with cloud platforms like **AWS and Snowflake**. As a data enthusiast, I’ve created this project to understand how Airflow can automate complex tasks, manage dependencies, and integrate various systems—making it an invaluable tool for anyone working with data pipelines.

### Concepts Covered

- DAGs (Directed Acyclic Graphs)
- Tasks and Operators
- Connections (using AWS S3, Snowflake, DBT)
- Hooks and Sensors
- XComs (Cross-communication between tasks)
- TaskFlow API

### Prerequisites

Before starting, ensure the following are installed:

- [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Visual Studio Code](https://code.visualstudio.com/download)

### Project Setup

#### Step 1: Setting Up Docker and Visual Studio Code

1. Create a new folder in Visual Studio Code for your project.
2. Add the following files to the folder:
   - `Dockerfile` ([airflow/dockerfile](airflow/dockerfile))
   - `docker-compose.yml` ([airflow/docker-compose.yml](airflow/docker-compose.yml))

These are critical for running Airflow in a containerized environment.

#### Step 2: Build and Start Docker Containers

1. Right-click on the `Dockerfile` in Visual Studio Code and select "Build Image".
2. Provide a name for your image (example: `airflow_project`).
3. Press Enter to start building the image.
4. Once the build is complete, right-click on `docker-compose.yml` and select "Compose Up".

#### Step 3: Verify Airflow Installation

After successful execution, an Airflow folder will be generated in your project directory. Open your browser and navigate to [http://localhost:8080](http://localhost:8080/) to access the Airflow UI. Log in with the following credentials:
- Username: `admin`
- Password: (found in `standalone_admin_password.txt` in the project folder)

### `welcome_dag`

[airflow/dags/welcome_dag.py](airflow/dags/welcome_dag.py)

This simple DAG is created to verify that Airflow setup is working correctly. It runs daily at 11:00 PM and performs the following tasks:
- Prints a friendly "Welcome" message.
- Displays the current date.
- Fetches a motivational quote from the Quotable API.

### Integrations

#### AWS S3 Connection

To integrate with AWS S3:

1. **Create an IAM User:**
   - Log in to your AWS root account and create a user named `airflow_user`.
   - Assign the required permissions for accessing S3.
   - Download the Access Key ID and Secret Access Key.

2. **Set Up Airflow Connection:**
   - In the Airflow UI, go to `Admin > Connections` and add a new record:
     - **Connection ID:** `aws_s3_connection`
     - **Connection Type:** `Amazon Web Services`
     - Provide the Access Key ID and Secret Access Key.

#### Snowflake Connection

To integrate with Snowflake:

1. In the Airflow UI, add another connection:
   - **Connection ID:** `airflow_snowflake_conn`
   - **Connection Type:** `Snowflake`
   - Fill in details for schema, database, warehouse, account ID, login, and password.

#### Email Setup


I’ve configured the necessary SMTP settings in the airflow.cfg file.
[airflow/airflow.cfg](airflow/airflow.cfg) 

To set it up, go to the SMTP section of the file and enter your email ID. For the password, if you're using Gmail, you’ll need to generate an app password. To do this, go to "Manage your Google account," search for "App passwords," set the app name as "Airflow," and create the password. Then, add this generated password into the airflow.cfg file.

### `operators_sensors_s3_snowflake_dag`

[airflow/dags/operators_sensors_s3_snowflake_dag.py](airflow/dags/operators_sensors_s3_snowflake_dag.py)

This DAG demonstrates a real-world use case by orchestrating data transfer from AWS S3 to Snowflake. It leverages advanced Airflow concepts like sensors, operators, and email notifications.

**DAG Details:**
- **Schedule Interval:** Runs daily at 11:00 PM (`0 23 * * *`)
- **Start Date:** Yesterday (`days_ago(1)`)

**Tasks:**
- **S3 Key Sensor:** Waits for the file `customer_details_raw.csv` to be available in S3.
- **Truncate Snowflake Table:** Clears the old data.
- **Load Data to Snowflake:** Copies the new data from S3 to Snowflake.
- **Email Notification:** Sends an email when the process is complete.

### `hooks_xcom_s3_snowflake`

[airflow/dags/hooks_s3_snowflake.py](airflow/dags/hooks_s3_snowflake.py)

In this DAG, I use Airflow’s hooks, XCom for inter-task communication, and task groups to make the ETL process more organized.

**Tasks:**
- **Extract Task (`extract_from_s3`)**: Uses `S3Hook` to read content of a file from S3 and pushes it to XCom.
- **Transform Task (`transform_data`)**: Processes the CSV data and pushes the transformed data to XCom.
- **Load Task (`load_to_snowflake`)**: Inserts the transformed data into Snowflake using `SnowflakeHook`.
- **Email Notification Task:** Sends a success notification email after completion.

### `branching_trigger`

[airflow/dags/branching_trigger.py](airflow/dags/branching_trigger.py)

This DAG monitors a file in an S3 bucket and performs branching logic based on its presence. If the file exists, it processes the ETL; if not, it sends an alert email.

**Tasks:**
- **Check File Task (`check_file_exists`)**: Verifies if `booking_details_raw.csv` exists in the bucket `airflow-buckets`.
- **Branching Task (`branching`)**: Directs workflow based on file presence (process ETL or send alert email).
- **ETL Processing Task (`process_etl`)**: Placeholder for actual ETL logic.
- **Email Alert Task (`send_alert_email`)**: Sends an email if the file is missing.

### `taskflow_api`

[airflow/dags/taskflow_api.py](airflow/dags/taskflow_api.py)

This DAG demonstrates an ETL pipeline using Airflow's TaskFlow API. Each step is defined as a Python function decorated with `@task()`:
- **Extract**: Reads a file from S3 and converts it into a Pandas DataFrame.
- **Transform**: Processes the data (e.g., making all text uppercase).
- **Load**: Inserts the processed data into Snowflake.

### `dbt_dag`

[airflow/dags/dbt_dag.py](airflow/dags/dbt_dag.py)

This DAG integrates DBT Cloud with Airflow. It triggers a DBT job using the DBT Cloud connection set in the Airflow UI. The job executes `dbt build` on a previously created DBT project.

### Conclusion

This project helped me gain hands-on experience in using Apache Airflow to automate and orchestrate data workflows. I learned how to build efficient, scalable DAGs and integrate them with cloud platforms like AWS and Snowflake. By streamlining data pipelines, I enhanced my ability to manage complex workflows effectively.
