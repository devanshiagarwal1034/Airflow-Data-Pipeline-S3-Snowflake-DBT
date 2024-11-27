# airflow
Overview
This project is designed to provide hands-on experience with Apache Airflow's core concepts, showcasing its flexibility and power in orchestrating workflows. Whether you're new to Airflow or aiming to enhance your skills, this repository offers a practical starting point by exploring concepts like:

DAGs (Directed Acyclic Graphs)
Tasks and Operators
Connections
Hooks and Sensors
XComs (Cross-communication between tasks)
TaskFlow API

The project also integrates with AWS S3 and Snowflake, demonstrating real-world applications of Airflow in managing and orchestrating workflows between cloud platforms and databases.


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
Open your browser and navigate to http://localhost:8080 to access the Airflow UI.
Log in with the following credentials:
Username: admin
Password: (found in standalone_admin_password.txt in the project folder)



First DAG: welcome_dag
The repository includes a sample DAG called welcome_dag to test your setup
DAG Details:

Schedule Interval: Runs daily at 11:00 PM (0 23 * * *)
Start Date: Yesterday (using days_ago(1))
Tasks:
Print Welcome Messag
Print Current Date
Fetch Random Quote: Retrieves a motivational quote from the Quotable API and displays it as the "Quote of the Day".

In the Airflow UI,Trigger the DAG to observe task execution.
This DAG runs basic tasks to confirm your Airflow environment is functioning correctly.



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
I have added all the required smtp configuration in airflow.cfg ,  go to the  smtp section of airflow.cfg, wrtie your email id , for password , you need to genrate the app password for airflow if your using gmail , then go to the manage your google account , then search app passwords, give the app name as airflow and create the password . add that password in the airflow.cfg.

operators_sensors_s3_snowflake_dag
This DAG demonstrates a real-world use case by orchestrating data transfer from AWS S3 to Snowflake. It leverages advanced Airflow concepts like sensors, operators, and email notifications.

DAG Details:

Schedule Interval: Runs daily at 11:00 PM (0 23 * * *)
Start Date: Yesterday (days_ago(1))
Tasks:
S3 Key Sensor: Waits for a specific file (customer_details_raw.csv) in an S3 bucket.
Truncate Table: Clears the customer_details_raw table in Snowflake to avoid duplicate data.
Load Data to Snowflake: Copies the CSV file from S3 to the Snowflake table using an external stage.
Email Notification: Sends an email upon successful data loading.
