import pymongo
import json

# Initializing connection to the database
dbclient = pymongo.MongoClient("localhost", 27017)
db = dbclient["iot-db"]
pde_flattened = db["iot-sensors-data-flattened"]

entries = pde_flattened.find()

# Loading the devices list from collection
db_devices_list = db["iot-devices-list"]
devices = db_devices_list.find()

# Extracting the device_ids in a list
existing_devices = []
for device in devices:
    existing_devices.append(device["device_id"])
    
# Iterate through each entry from previous day's objects and add new devices to the collection
for entry in entries:
    if entry["device_id"] not in existing_devices:
        db_devices_list.insert_one({"device_id":entry["device_id"], "device_type":entry["device_type"]})
        existing_devices.append(entry["device_id"])

