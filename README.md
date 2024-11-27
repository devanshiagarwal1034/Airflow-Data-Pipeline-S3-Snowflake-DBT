# airflow

Overview -


In this project, I’ve explored the powerful capabilities of Apache Airflow, gaining hands-on experience in workflow orchestration and integrating it with cloud platforms like **AWS and Snowflake**. As a data enthusiast , I’ve created this project to understand how Airflow can automate complex tasks, manage dependencies, and integrate various systems—making it an invaluable tool for anyone working with data pipeline

Concepts Covered -

DAGs (Directed Acyclic Graphs)
Tasks and Operators
Connections ( using AWS S3, Snowflake , DBT)
Hooks and Sensors
XComs (Cross-communication between tasks)
TaskFlow API

Prerequisites
Before starting, ensure the following are installed:

Docker Desktop (https://docs.docker.com/desktop/setup/install/windows-install/)
Visual Studio Code (https://code.visualstudio.com/download)

Project Setup

Step 1: Setting Up Docker and Visual Studio Code
Create a new folder in Visual Studio Code for your project.
Add the following files to the folder:
Dockerfile
docker-compose.yml
These are critical for running Airflow in a containerized environment.

Step 2: Build and Start Docker Containers

Right-click on the Dockerfile in Visual Studio Code and select "Build Image".
Provide a name for your image (example- airflow_project).
Press Enter to start building the image.
Once the build is complete, right-click on docker-compose.yml and select "Compose Up".

Step 3: Verify Airflow Installation
After successful execution, an Airflow folder will be generated in your project directory.
Open your browser and navigate to [http://localhost:8080](http://localhost:8080/) to access the Airflow UI.
Log in with the following credentials:
Username: admin
Password: (found in standalone_admin_password.txt in the project folder)

welcome_dag

 It is a simple DAG I’ve created to verify that  Airflow setup is working correctly. It runs daily at 11:00 PM and performs the following tasks:

Prints a friendly "Welcome" message.
Displays the current date.
Fetches a motivational quote from the Quotable API.

Integrations

AWS S3 Connection

To integrate with AWS S3:

Create an IAM User:
Log in to your AWS root account and create a user named airflow_user.
Assign the required permissions for accessing S3.
Download the Access Key ID and Secret Access Key.

Set Up Airflow Connection:
In the Airflow UI, go to Admin > Connections and add a new record:
Connection ID: aws_s3_connection
Connection Type: Amazon Web Services
Provide the Access Key ID and Secret Access Key.

Snowflake Connection
To integrate with Snowflake:

In the Airflow UI, add another connection:
Connection ID: airflow_snowflake_conn
Connection Type: Snowflake
Fill in details for schema, database, warehouse, account ID, login, and password.

for Email Setup -
I’ve configured the necessary SMTP settings in the airflow.cfg file. To set it up, go to the SMTP section of the file and enter your email ID. For the password, if you're using Gmail, you’ll need to generate an app password. To do this, go to "Manage your Google account," search for "App passwords," set the app name as "Airflow," and create the password. Then, add this generated password into the airflow.cfg file.

operators_sensors_s3_snowflake_dag
This DAG demonstrates a real-world use case by orchestrating data transfer from AWS S3 to Snowflake. It leverages advanced Airflow concepts like sensors, operators, and email notifications.

DAG Details:

Schedule Interval: Runs daily at 11:00 PM (0 23 * * *)
Start Date: Yesterday (days_ago(1))

Tasks:
S3 Key Sensor: Waits for the file customer_details_raw.csv to be available in S3.
Truncate Snowflake Table: Clears the old data.
Load Data to Snowflake: Copies the new data from S3 to Snowflake.
Email Notification: Sends an email when the process is complete.

hooks_xcom_s3_snowflake
In this DAG, I use Airflow’s hooks, XCom for inter-task communication, and task groups to make the ETL process more organized:

1. DAG Definition
Schedule: Runs daily starting from November 26, 2024.
Default Arguments: Sets common properties like the owner, failure notifications, and email configurations.
2. Tasks
a. Extract Task (extract_from_s3)
Uses S3Hook to read the content of a file (booking_details_raw.csv) from an S3 bucket.
Pushes the file content into XCom for downstream tasks using kwargs['ti'].xcom_push.

b. Transform Task (transform_data)
Pulls the file content from XCom.
Processes the CSV data:
Splits the content into rows and columns.
Parses and validates each row to ensure it has the required 8 columns.
Pushes the transformed data (as a list of lists) into XCom for the load task.

c. Load Task (load_to_snowflake)
Pulls the transformed data from XCom.
Uses SnowflakeHook to connect to Snowflake.
Inserts the transformed data into the bookings_details_raw table using the INSERT INTO statement.
d. Email Notification Task
Sends a success notification email after the ETL workflow is completed.
5. Task Group
The TaskGroup organizes extract_from_s3 and transform_data under a logical group (extract_and_transform). This improves DAG readability in the Airflow UI.



branching_trigger

The Dag  monitors a file in an S3 bucket and performs branching logic based on its presence. If the file exists, it processes the ETL; if not, it sends an alert email.
2. Tasks
a. Check File Task
Task ID: check_file_exists
Logic:
Uses S3Hook.check_for_key() to verify if booking_details_raw.csv exists in the bucket airflow-buckets.
Returns a branching decision (process_etl or send_alert_email) to the next task.
b. Branching Task
Task ID: branching
Purpose: Directs the workflow to either process_etl_task or send_alert_email_task based on the result from check_file_exists.
c. ETL Processing Task
Task ID: process_etl
Logic:
Placeholder for actual ETL logic. You can integrate your extraction, transformation, and loading steps here.
Currently, it only logs a message.
d. Email Alert Task
Task ID: send_alert_email
Logic:
Sends an email if the file does not exist in the bucket.
Uses the EmailOperator within a Python callable.
3. Workflow
Task Dependencies:
check_file_exists → branching
branching → process_etl_task (if file exists)
branching → send_alert_email_task (if file does not exist)
BranchPythonOperator ensures only one path (branch) executes, preventing unnecessary task executions.


taskflow_api

This Dag demonstrates an ETL pipeline implemented using Airflow's TaskFlow API,Each step is defined as a Python function decorated with @task().
Extract: Reads a file from S3 and converts it into a Pandas DataFrame.
Transform: Processes the data (e.g., making all text uppercase).
Load: Inserts the processed data into Snowflake.

dbt_dag
I created this DAG to explore how to connect DBT Cloud with Airflow. For this, I used one of my previous DBT projects. First, I went to the DBT Cloud UI, navigated to the "Deploy" section, and created a job named "Job for Airflow," adding the dbt build command. 
Then, I generated a personal API token by going to my profile, selecting "API Token," and creating a new personal access token (e.g., "Airflow Service Token"). After copying the token, I added the DBT Cloud connection in the Airflow UI.

In the DAG, I included the job ID of the DBT job I created in DBT Cloud and triggered the DAG to run it.

Conclusion -
This project helped me gain hands-on experience in using Apache Airflow to automate and orchestrate data workflows. I learned how to build efficient, scalable DAGs and integrate them with cloud platforms like AWS and Snowflake. By streamlining data pipelines, I enhanced my ability to manage complex workflows effectively.
