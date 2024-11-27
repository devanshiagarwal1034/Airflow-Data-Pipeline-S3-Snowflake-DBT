create database travel_db;

create schema airflow;


CREATE OR REPLACE STAGE my_s3_stage
  URL = 's3://airflow-buckets/'
  CREDENTIALS = (AWS_KEY_ID = '<enter your AWS_KEY_ID>'
                 AWS_SECRET_KEY = '<enter your AWS_SECRET_KEY> ');


CREATE TABLE customer_details_raw (
    CUSTOMER_ID INT,
    FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(50),
    EMAIL VARCHAR(100),
    PHONE_NUMBER VARCHAR(20),
    ADDRESS VARCHAR(255),
    COUNTRY_CODE VARCHAR(10),
    SEGMENT_ID INT
);






CREATE or replace TABLE bookings_details_raw (
    BOOKING_ID INT PRIMARY KEY,        
    CUSTOMER_ID INT NOT NULL,           
    BOOKING_DATE VARCHAR(100),         
    BOOKING_TIME VARCHAR(100) ,         
    DESTINATION_TYPE VARCHAR(50) NOT NULL, 
    AMOUNT_SPENT DECIMAL(10, 2) NOT NULL, 
    CURRENCY_CODE CHAR(3) NOT NULL,   
    STATUS VARCHAR(50) NOT NULL         
);

