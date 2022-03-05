# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

'''
This file has wrapper functions to access Mongo database
1. Connect to Server
2. Insert documents/records one or many
3. Get documents one or many
4. Update document
5. Delete documents one or many
6. Aggregate documents

The sample uses the wrappers to create an AirQuality DB with many tables.
It populates the tables with records.
It uses a random data generation mechanims to prepare a list of items (until keyboard interrupt) to be inserted into
table.
It runs several queries and prints the results.
'''


from pymongo import MongoClient
from bson.objectid import ObjectId
import math
import random
import time
import datetime


def connect_mongo(host, port):

    mongo_client = None
    try:
        mongo_client =  MongoClient(f'mongodb://{host}:{port}')
        print("Connection successful")
        return mongo_client
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def insert_single(collection, data):
    try:
        if data is None:
            print("No data is available.")
        else:
            result = collection.insert_one(data)
            print(result.inserted_id)
            print("Query successful")
            return True
    except Exception as e:
        print("An exception occurred ::", e)
        return False


# performing the execute many query over the table,
# this method will help us to inert multiple records using a single instance

def insert_multiple(collection, data):
	try:
		if data is None:
			print("No data is available.")
		else:
			result = collection.insert_many(data)
			print(result.inserted_ids)
			print("Query successful")
			return True
	except Exception as e:
		print("An exception occurred ::", e)
		return False


# retrieving the data from the table based on the given query
def find_single(collection, data):
	try:
		if data is None:
			print("No data is available. Please provide the data.")
		else:
			result = collection.find_one(data)
			print("Query successful")
			return result
	except Exception as e:
		print("An exception occurred ::", e)
		return False


def find_multiple(collection, data):
	try:
		if data is None:
			print("No data is available. Please provide the data.")
		else:
			result = collection.find(data)
			print("Query successful")
			return result
	except Exception as e:
		print("An exception occurred ::", e)
		return False


def delete_single(collection, data):
	try:
		if data is None:
			print("No data is available. Please provide the data.")
		else:
			result = collection.delete_one(data)
			print("Query successful")
			return result
	except Exception as e:
		print("An exception occurred ::", e)
		return False


def delete_multiple(collection, data):
	try:
		if data is None:
			print("No data is available. Please provide the data.")
		else:
			result = collection.delete_many(data)
			print("Query successful")
			return result
	except Exception as e:
		print("An exception occurred ::", e)
		return False


def single_update(collection, query_data, update_data):
	try:
		if data is None:
			print("No data is available. Please provide the data.")
		else:
			result = collection.update_one(query_data, update_data)
			print("Query successful")
			return result
	except Exception as e:
		print("An exception occurred ::", e)


def aggregate_data(collection, query):

	try:
		if data is None:
			print("No data is available. Please provide the data.")
		else:
			result = collection.aggregate(query)
			print("Query successful")
			return result
	except Exception as e:
		print("An exception occurred ::", e)
		return False


if __name__ == "__main__":

    HOST = '127.0.0.1'
    PORT = '27017'
    DB_NAME = 'air_quality_db'
    DEVICE_COLLECTION = 'devices'
    USERS_COLLECTION = 'users'
    REPLOCATION_COLLECTION = 'replocation'
    AREA_COLLECTION = 'area'
    AQ_DATA_COLLECTION = 'aq_data'
    USERS_ACCESS_COLLECTION = "users_location"
    USERS_ACCESS_ENTITY_COLLECTION = "users_entity"

    db_conn = connect_mongo(HOST, PORT)
    db_conn.drop_database(DB_NAME)
    db = db_conn[DB_NAME]
    device_collection = db[DEVICE_COLLECTION]
    users_collection = db[USERS_COLLECTION]
    replocation_collection = db[REPLOCATION_COLLECTION]
    area_collection = db[AREA_COLLECTION]
    aq_data_collection = db[AQ_DATA_COLLECTION]
    users_access_collection = db[USERS_ACCESS_COLLECTION]
    users_access_entity_collection = db[USERS_ACCESS_ENTITY_COLLECTION]

# inserting data in User collection
    print(f"Inserting data in: '{users_collection}'")
    user_1 = {"_id":"U101","user_name": "john", "email": "john@office.com","phone_no": "1872681", "address": "newyork"}
    user_2 = {"_id":"U102","user_name":"bob","email":"bob@office.com","phone_no":"1872661","address":"nashua"}
    user_3 = {"_id":"U103","user_name":"micheal","email":"micheal@office.com","phone_no":"9816221","address":"scranton"}
    user_4 = {"_id":"U104","user_name":"dwight","email":"dwight@office.com","phone_no":"9876121","address":"scranton"}
    user_5 = {"_id":"U105","user_name":"jim","email":"jim@office.com","phone_no":"8897122","address":"scranton"}

    insert_single(users_collection, user_1)
    insert_single(users_collection, user_2)
    insert_single(users_collection, user_3)
    insert_single(users_collection, user_4)
    insert_single(users_collection, user_5)
    print('\n')

    # Inserting data in area table
    # this table is intertwined with the location collection. Each area can have multiple location under it.
    # This information is also saved in the collection.
    print(f"Inserting data in: '{area_collection}'")

    area_1 = {"_id":"A12901","area_description":"Hospital area","locations":["L1201A","L1202B"]}
    area_2 = {"_id":"A12903","area_description":"School area","locations":["L1202B","L1203A"]}
    area_3 = {"_id":"A12904","area_description":"Secondary school area","locations":["L1208A"]}
    area_4 = {"_id":"A12973","area_description":"Cantonment area","locations":["L1238B"]}
    area_5 = {"_id":"A12341","area_description":"Traffic area","locations":["L1238B"]}

    insert_single(area_collection, area_1)
    insert_single(area_collection, area_2)
    insert_single(area_collection, area_3)
    insert_single(area_collection, area_4)
    insert_single(area_collection, area_5)
    print('\n')

    # inserting data in device collection. This table will have basic device realted information.
    # Every document in the collection will also contain the information related to the installation and location of each device.

    print(f"Inserting data in: '{device_collection}'")
    device_1 = {"_id":"1001","device_type":"pm sensor","mfr":"PLC group","serial_no":"A1231","yom":"2018","location_id":"L1201A","installation_timestamp":{"timestamp": datetime.datetime.now().strftime("%Y-%m-%d")},"is_active":"yes"}
    device_2 = {"_id":"1002","device_type":"pm sensor","mfr":"sensenext","serial_no":"B1231","yom":"2019","location_id":" L1202B","installation_timestamp":{"timestamp":datetime.datetime.now().strftime("%Y-%m-%d")},"is_active":"yes"}
    device_3 = {"_id":"1003","device_type":"pm sensor","mfr":"PLC group","serial_no":"A1232","yom":"2019","location_id":"L1203A","installation_timestamp":{"timestamp":datetime.datetime.now().strftime("%Y-%m-%d")},"is_active":"yes"}
    device_4 = {"_id":"1004","device_type":"pm sensor","mfr":"sensenext","serial_no":"B1232","yom":"2019","location_id":"L1208A","installation_timestamp":{"timestamp":datetime.datetime.now().strftime("%Y-%m-%d")},"is_active":"yes"}
    device_5 = {"_id":"1005","device_type":"pm sensor","mfr":"PLC group","serial_no":"A1233","yom":"2020","location_id":" L1238B","installation_timestamp":{"timestamp":datetime.datetime.now().strftime("%Y-%m-%d")},"is_active":"yes"}

    insert_single(device_collection, device_1)
    insert_single(device_collection, device_2)
    insert_single(device_collection, device_3)
    insert_single(device_collection, device_4)
    insert_single(device_collection, device_5)
    print('\n')

    # This collection will hold the information about the collection. Each document will hold the data of device id as well.
    # Here _id will represent the location id for each of the document.

    print(f"Inserting data in: '{replocation_collection}'")
    location_1 = {"_id":"L1201A","lat":78.32,"long":87.32,"location_name":"District Police station","description":"Public place","location_type":"Public space","device_id":"1001","areas":["A12901","A12903 "]}
    location_2 = {"_id":"L1202B","lat":79.3,"long":88.4,"location_name":"District Hospital ","description":"Public place for medically cared people","location_type":"public place","device_id":"1002","areas":["A12904"]}
    location_3 = {"_id":"L1203A","lat":81.34,"long":90.5,"location_name":"District school","description":"Primary school","location_type":"primary school for children's","device_id":"1003","areas":["A12973","A12341"]}
    location_4 = {"_id":"L1208A","lat":89.45,"long":132.45,"location_name":"District secondary school","description":"District school","location_type":"Secondary school","device_id":"1004","areas":["A12973"]}
    location_5 = {"_id":"L1238B","lat":109.34,"long":129.8,"location_name":"Ring road - 1","description":"cross road","location_type":"cross road","device_id":"1005","areas":["A12341"]}

    insert_single(replocation_collection, location_1)
    insert_single(replocation_collection, location_2)
    insert_single(replocation_collection, location_3)
    insert_single(replocation_collection, location_4)
    insert_single(replocation_collection, location_5)
    print('\n')

    # This collection will hold the information of user access for different type of collection.
    # The collection is designed to hold the arrray of location access permission for location id in each of the document.
    # Similar array will be there for other resources such as device and area.

    print(f"Inserting data in: '{users_access_collection}'")
    user_access_1 = {"_id":"U101","email":"john@office.com","location_access":[{"location_id":"L1201A","access_type":"Normal"},{"location_id":"L1202B","access_type":"Admin"}],"area_access":[{"area_id":"A12901","access_type":"Normal"},{"area_id":"A12903","access_type":"Normal"}],"device_access":[{"device_id":"1001","access_type":"Normal"}]}
    user_access_2 = {"_id":"U102","email":"bob@office.com","location_access":[{"location_id":"L1208A","access_type":"Admin"}],"area_access":[{"area_id":"A12904","access_type":"Admin"}],"device_access":[{"device_id":"1003","access_type":"Admin"}]}
    user_access_3 = {"_id":"U103","email":"micheal@office.com","location_access":[{"location_id":"L1202B","access_type":"Admin"}],"area_access":[{"area_id":"A12341","access_type":"Admin"}],"device_access":[{"device_id":"1004","access_type":"Normal"}]}
    user_access_4 = {"_id":"U104","email":"dwight@office.com","location_access":[{"location_id":"L1201B","access_type":"Normal"},{"location_id":"L1203A","access_type":"Admin"}],"area_access":[{"area_id":"A12973","access_type":"Normal"}],"device_access":[{"device_id":"1005","access_type":"Normal"}]}
    user_access_5 = {"_id":"U105","email":"jim@office.com","location_access":[{"location_id":"L1208A","access_type":"Admin"},{"location_id":"L1238B","access_type":"Admin"}],"area_access":[{"area_id":"A12341","access_type":"Admin"}],"device_access":[{"device_id":"1005","access_type":"Admin"}]}

    insert_single(users_access_collection, user_access_1)
    insert_single(users_access_collection, user_access_2)
    insert_single(users_access_collection, user_access_3)
    insert_single(users_access_collection, user_access_4)
    insert_single(users_access_collection, user_access_5)
    print('\n')

    # This collection is designed to hold the information of user access.
    # The data available here will be in form of an object. Here array will be designed to hold the data of every entity type.
    # It will help in improving the overall performance.

    print(f"Inserting data in: '{users_access_entity_collection}'")
    user_entity_access_1 = {"_id":"U101","email":"john@office.com","entity_list":[{"entity_id":"1001","entity_type":"device","access_type":"Admin"},{"entity_id":"L1201A","entity_type":"location","access_type":"Admin"}]}
    user_entity_access_2 = {"_id":"U102","email":"bob@office.com","entity_list":[{"entity_id":"1002","entity_type":"device","access_type":"Normal"},{"entity_id":"L1202B","entity_type":"location","access_type":"Normal"}]}

    insert_single(users_access_entity_collection, user_entity_access_1)
    insert_single(users_access_entity_collection, user_entity_access_2)
    print('\n')

	# Query to find a single data from the Database
    query_data = {'serial_no':'A1231'}
    data = find_single(device_collection, query_data)
    print(data)

    query_data = {'_id':'U102'}
    data = find_single(users_access_entity_collection, query_data)
    print(data)

    query_data = {'_id':'U102'}
    data = find_single(users_access_collection, query_data)
    print(data)


    # Query to find multiple records from the Database
    print("Performing multiple find operation in the database. ")
    query_data = {'device_type':'pm sensor'}
    result = find_multiple(device_collection, query_data)
    device_config = []
    location_config = []
    for doc in result:
        print(doc)
        device_config.append(doc['serial_no'])
        location_config.append(doc['location_id'])
    print('\n')

    query_data = {'_id':'A12341'}
    data = delete_single(area_collection, query_data)
    print(data)

    # Deleting multiple records from the device collection
    # Uncommenting this will delete all the dicuments from the collection
    # Hence it would ultimately result in not ineserting anything in the database.

    #query_data = {"device_type":"pm sensor"}
    #data = delete_multiple(device_collection, query_data)
    #print(data)

    print("Performing Update operation on the database")
    filter = {'serial_no':'A1231', 'mfr' : 'PLC group'}
    data = {'$set': {'is_active': 'No'}}
    result = single_update(device_collection, filter, data)
    print(result.acknowledged)
    print('\n')

    # Creating the data
    print("Data creation is in progress: ")
    print("Type Ctrl + C to exit data creation.")
    aq_data = []
    clock = 0
    while True:
        try:
            time.sleep(1)
            for i in range(len(device_config)):
                clock = clock + 1
                data = {
                    '_id' : clock,
                    'serial_no': device_config[i],
                    'location_id': location_config[i],
                    'pm25': int(random.uniform(95.5, 105.5)),
                    'pm10': int(random.uniform(190, 210)),
                    'co': int(random.uniform(70.5, 85.5)),
                    'so2':int(random.uniform(60, 90)),
                    'o3': int(random.uniform(0.5, 3.5)),
                    'collection_time' : datetime.datetime.now()
                }
                aq_data.append(data)
        except KeyboardInterrupt:
            break
    print("Data insertion is in progress: ")
    insert_multiple(aq_data_collection, aq_data)
    print("Data Inserted")

    pipeline1 = [
        {
            '$match': {'serial_no':'A1231'}
        }
    ]

    pipeline2 = [
        {
            '$match': {'serial_no':'A1231', 'pm10': {'$gte': 100}}
        }
    ]

    pipeline3 = [
        {
            '$match': {'pm10': {'$gte': 100}}
        },
        {
            '$group': {'_id': '$serial_no', 'total_value': {"$sum": "$pm10"}}
        }
    ]

    pipeline4 = [
        {
            '$match': {'serial_no':'A1231'}
        },
        {
            '$group': {'_id': {
                                'serial_no': '$serial_no',
                                'day': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$collection_time'}},
                              },
                        'total_value': {"$sum": "$pm10"},
                        'total_count': {"$sum": 1}
                    }
        }
    ]

    pipeline5 = [
        {
            '$match': {'serial_no':'A1231'}
        },
        {
            '$group': {'_id': {
							'serial_no': '$serial_no',
							'day': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$collection_time'}},
							},
						'total_value': {"$sum": "$pm10"},
						'total_count': {"$sum": 1}
					}
        },
        {
            '$project': {
			'serial_no': '$_id.serial_no',
			'date': '$_id.day',
			'sum': '$total_value',
			'count': '$total_count',
			'_id': 0
			}
		},
        {
            '$sort': {'serial_no': 1, 'date': 1}
        }
    ]

