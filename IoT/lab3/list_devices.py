import pymongo
import json

#Initializing connection to the database
dbclient = pymongo.MongoClient("localhost", 27017)
db = dbclient["iot-db"]
db_devices_list = db["iot-devices-list"]

#Loading the devices list
entries = db_devices_list.find()

for entry in entries:
    print("Device ID: " + entry["device_id"] + " | Device Type: " + entry["device_type"])

