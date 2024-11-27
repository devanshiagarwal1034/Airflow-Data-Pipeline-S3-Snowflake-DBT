# airflow
This project is designed to help you get hands-on experience with Apache Airflow's core concepts. If you're exploring Airflow for the first time, this repository will guide you through the setup and introduce key features such as:

DAGs (Directed Acyclic Graphs)
Tasks and Operators
Connections
Hooks and Sensors
XComs (Cross-communication between tasks)
TaskFlow API

first Install the docker and visual studio 
.https://docs.docker.com/desktop/setup/install/windows-install/
https://code.visualstudio.com/download
create a folder in visual studio , 
add Dockerfile and Docker-Compose.yml
 These are essential for running Airflow in a containerized environment.
Right click on docketfile and click build Image , enter image name(you can give your project name as well) then click enter , after it completed , write click on Docker-Compose.yml and click compose up.
after it completed you can see airflow folder  is created in your folder , in localhost:/8080 you can see you airflow UI , you can login by giving username as admin and  password you can find in standalone_admin_password.txt folder.

To test your setup, I’ve included a simple DAG called welcome_dag. This DAG:
Runs basic tasks to ensure your Airflow environment is functioning correctly. In the airflow Ui , you can click on this dag then trigger it , to see it functioning.


Next I have created the connection of S3, for that you need to go to admin tab , then connection , add new record.
