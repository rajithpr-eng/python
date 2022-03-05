# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

'''
This file has wrapper functions to access SQL database
1. Connect to Server
2. Create a DB
3. Create table
4. Insert records one or many
5. Search table

The sample uses the wrappers to create an AirQuality DB with many tables.
It populates the tables with records.
It uses a random data generation mechanims to prepare a list of items (until keyboard interrupt) to be inserted into
table.
It runs several queries and prints the results.
'''

import mysql.connector
import random
import time
import datetime

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    except Error as err:
        print(f"Error: '{err}'")

    print("MySQL Database connection successful")

    return connection


def create_switch_database(connection, db_name, switch_db):
	cursor = connection.cursor()
	try:
		drop_query = "DROP DATABASE IF EXISTS " + db_name
		db_query = "CREATE DATABASE " + db_name
		switch_query = "USE " + switch_db
		cursor.execute(drop_query)
		cursor.execute(db_query)
		cursor.execute(switch_query)
		print("Database created successfully")
	except Error as err:
		print(f"Error: '{err}'")


def create_insert_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


# performing the execute many query over the table,
# this method will help us to inert multiple records using a single instance
def insert_many_data(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


# retrieving the data from the table based on the given query
def select_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


# Configuring the tables that will hold the data
# here we are creating the table named as area
create_area_table = """
CREATE TABLE area (
	area_id varchar(45) PRIMARY KEY,
	area_description varchar(45) NOT NULL
)
"""


# creating the devices table
create_devices_table = """
CREATE TABLE devices (
	device_id varchar(45) PRIMARY KEY,
	mfr varchar(160) NOT NULL,
	type varchar(45) NOT NULL,
	serial_no varchar(45) NOT NULL,
	yom varchar(45) NOT NULL
)
"""


# creating the location table
create_rep_location = """
CREATE TABLE replocation (
	location_id varchar(45) PRIMARY KEY,
	lattiude varchar(25) NOT NULL,
	longitude varchar(250) NOT NULL,
	location_name varchar(120) NOT NULL,
	description varchar(240) NOT NULL,
	location_type varchar(100)
)
"""


# creating the users table to hold the user basic information
create_user_table = """
CREATE TABLE users (
	user_id varchar(20) PRIMARY KEY,
	user_name varchar(45) NOT NULL,
	email varchar(45) NOT NULL,
	phone_no varchar(45) NOT NULL,
	address varchar(160) NOT NULL
)
"""


# table to map the location of each area with the map
create_area_location_table = """
CREATE TABLE area_location (
	id INT NOT NULL PRIMARY KEY,
	fk_areaid varchar(45) NOT NULL,
	fk_locationid_area varchar(45) NOT NULL,
	CONSTRAINT `fk_areaid` FOREIGN KEY (`fk_areaid`) REFERENCES `area` (`area_id`),
	CONSTRAINT `fk_locationid_area_location` FOREIGN KEY (`fk_locationid_area`) REFERENCES `replocation` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE
)
"""


# table to map the devices and locations asscoitaed with that device
create_installation_table = """
CREATE TABLE installation (
	installation_id int NOT NULL PRIMARY KEY,
	fk_locationid_installation varchar(45) NOT NULL,
	fk_deviceid_installation varchar(45) NOT NULL,
	installation_timestamp timestamp(2) NOT NULL,
	is_active varchar(10) NOT NULL,
	CONSTRAINT `fk_deviceid_installation` FOREIGN KEY (`fk_deviceid_installation`) REFERENCES `devices` (`device_id`),
	CONSTRAINT `fk_locationid_installation` FOREIGN KEY (`fk_locationid_installation`) REFERENCES `replocation` (`location_id`)
)
"""


# creating a table to map the access control of each type od entity
# location, device, area in a single table
# this reduces the need to introdice foreign key concept in this table
create_user_access_control_table = """
CREATE TABLE user_access_control (
	id int NOT NULL PRIMARY KEY,
	user_id varchar(45) NOT NULL,
	access_entity_type varchar(45) NOT NULL,
	entity_id varchar(45) NOT NULL,
	access_type varchar(20) NOT NULL,
	CONSTRAINT `fk_user_id_access` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
)
"""


# creating individual table to map the access control for user for each of the location
# drawback is that we need to create table for each entity indvidually to maintain the user access relationship
create_user_location_access = """
CREATE TABLE users_location_access (
	user_id varchar(45) NOT NULL,
	users_location_access varchar(45) NOT NULL,
	access_type varchar(45) NOT NULL,
	PRIMARY KEY (user_id, users_location_access),
	CONSTRAINT `fk_userid` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
	CONSTRAINT `user_location_access` FOREIGN KEY (`users_location_access`) REFERENCES `replocation` (`location_id`) ON DELETE CASCADE ON UPDATE CASCADE
)
"""

# creating the raw data table that will hold the necessary information related to the table
create_aq_data_table = """
CREATE TABLE aq_data (
	aqdata_id  INT PRIMARY KEY,
	fk_device_id varchar(45) ,
	fk_location_id varchar(45) ,
	pm25 FLOAT DEFAULT NULL,
	pm10 FLOAT DEFAULT NULL,
	co FLOAT DEFAULT NULL,
	so2 FLOAT DEFAULT NULL,
	o3 FLOAT DEFAULT NULL,
	collection_time varchar(40) NOT NULL,
	CONSTRAINT fk_deviceid FOREIGN KEY (`fk_device_id`) REFERENCES `devices` (`device_id`),
	CONSTRAINT fk_locationid FOREIGN KEY (`fk_location_id`) REFERENCES `replocation` (`location_id`)
)
"""

# creating another raw data table that can mimic in key:value format
create_aq_data_flex = """
CREATE TABLE aq_data_flex (
	aqdata_id INT PRIMARY KEY NOT NULL,
	fk_device_id_flex varchar(45),
	fk_location_id_flex varchar(45),
	aq_data_type varchar(45) NOT NULL,
	aq_data_value double NOT NULL,
	collection_time varchar(40) NOT NULL,
	CONSTRAINT fk_deviceid_flex FOREIGN KEY (`fk_device_id_flex`) REFERENCES `devices` (`device_id`),
	CONSTRAINT fk_locationid_flex FOREIGN KEY (`fk_location_id_flex`) REFERENCES `replocation` (`location_id`)
)
"""

insert_area = """
INSERT INTO area VALUES
('area101',  'Gotham')
"""


insert_device = """
INSERT INTO devices VALUES
('device101',  'PLC Group', 'PM Sensor', '1234876', '23-06-2018'),
('device102',  'Innovative Solutions', 'Green House Gas', '4287667', '22-09-2018'),
('device103',  'AirThings', 'PM Sensor, Green House Gas', '3452891', '24-12-2018')
"""


insert_location = """
INSERT INTO replocation VALUES
('PSBG101',  '75.93', '134.84', 'Primary School Backyard Gotham', 'District Primary School', 'School'),
('CIHG101',  '81.67', '154.17', 'City Hospital Gotham', 'District Hospital', 'Hospital'),
('PSFG102',  '79.67', '140.39', 'Primary School Frontgate Gotham', 'District Primary School', 'School')
"""


insert_user = """
INSERT INTO users VALUES
('user101',  'John Doe', 'john@example.com', '665-877-8852', '790 Kozey Meadow Apt. 175 Kozeyside, WA 99871-1865'),
('user102',  'Alice cooper', 'alice@example.com', '134-345-5430', '8589 Miller Centers Leannonmouth, OR 18781-6843'),
('user103',  'Bob Willis', 'bob@example.com', '300-052-5450', '958 Gerry Estate New Eudora, MT 89349-0462')
"""


insert_users_location_access = """
INSERT INTO users_location_access VALUES
('user101',  'PSBG101', 'Normal'),
('user101',  'PSFG102', 'Admin'),
('user102',  'CIHG101', 'Admin')
"""


user_access_control_table = """
INSERT INTO user_access_control VALUES
(1, 'user101', 'location', 'PSBG101', 'Normal'),
(2, 'user101', 'location', 'PSFG102', 'Admin'),
(3, 'user102', 'location', 'CIHG101', 'Admin'),
(4, 'user101', 'device', 'device101', 'Normal'),
(5, 'user101', 'device', 'device102', 'Admin'),
(6, 'user102', 'area', 'area101', 'Admin')

"""

sql = '''
INSERT INTO aq_data (aqdata_id, fk_device_id, fk_location_id, pm25, pm10, co, so2, o3, collection_time) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

q1 = """
SELECT *
FROM devices;
"""

q2 = """
SELECT *
FROM replocation;
"""


if __name__ == "__main__":
    connection = create_server_connection("localhost", "root", "pass") # Connect to the Database
    create_switch_database(connection, "AirQuality", "AirQuality")
    create_insert_query(connection, create_area_table) # Execute our defined query
    create_insert_query(connection, create_devices_table) # Execute our defined query
    create_insert_query(connection, create_rep_location) # Execute our defined query
    create_insert_query(connection, create_user_table) # Execute our defined query
    create_insert_query(connection, create_aq_data_table) # Execute our defined query
    create_insert_query(connection, create_aq_data_flex) # Execute our defined query
    create_insert_query(connection, create_area_location_table) # Execute our defined query
    create_insert_query(connection, create_installation_table) # Execute our defined query
    create_insert_query(connection, create_user_access_control_table) # Execute our defined query
    create_insert_query(connection, create_user_location_access) # Execute our defined query
    create_insert_query(connection, insert_area)
    create_insert_query(connection, insert_device)
    create_insert_query(connection, insert_location)
    create_insert_query(connection, insert_user)
    create_insert_query(connection, insert_users_location_access)
    create_insert_query(connection, user_access_control_table)
    result_device = select_query(connection, q1)
    device_config = []
    for result in result_device:
        print(result)
        device_config.append(result[0])
    location_config = []
    result_location = select_query(connection, q2)
    for result in result_location:
        print(result)
        location_config.append(result[0])
    val = []
    clock = 0
    while True:
        try:
            time.sleep(1)
            for i in range(len(device_config)):
                clock = clock+1
                data = [clock, device_config[i], location_config[i], random.uniform(95.5, 105.5), random.uniform(190, 210), random.uniform(70.5, 85.5), random.uniform(60, 90), random.uniform(0.5, 3.5), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                val.append(tuple(data))

        except KeyboardInterrupt:
            break
    insert_many_data(connection, sql, val)
