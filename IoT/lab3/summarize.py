import pymongo
import json

#Initializing connection to the database and fetching the list of devices
dbclient = pymongo.MongoClient("localhost", 27017)
db = dbclient["iot-db"]
db_devices_list = db["iot-devices-list"]
devices = db_devices_list.find()

# Initializing a *values* list to capture data from previous day's entries
values= {}
for device in devices:
    values[device["device_id"]] = {}
    values[device["device_id"]]["values"] = []
    
# Fetching the previous day iot-devices data
pde_flattened = db["iot-sensors-data-flattened"]
entries = pde_flattened.find()

# Adding the iot devices data to the appropriate device_id list
for entry in entries:
    values[entry["device_id"]]["values"].append(entry["value"])
    
# Fetch the list of devices
devices = db_devices_list.find()

# Iterate through devices list and calculate the min, max and aggregate
for device in devices:
    values[device["device_id"]]["min_value"] = min(values[device["device_id"]]["values"])
    values[device["device_id"]]["max_value"] = max(values[device["device_id"]]["values"])
    values[device["device_id"]]["count"] = len(values[device["device_id"]]["values"])
    values[device["device_id"]]["agg_value"] = round(sum(values[device["device_id"]]["values"])\
        /values[device["device_id"]]["count"],2)
    values[device["device_id"]]["device_type"] = device["device_type"]
    # Delete the raw values as we don't need it in the daily summary
    del values[device["device_id"]]["values"]
    
# Calculate previous day's day in YYYY-MM-DD format
import datetime
previousday = datetime.date.today() - datetime.timedelta(days=1)
previousday = previousday.strftime("%Y-%m-%d")

# Insert the summary into the *daily-summary* collection
dailysummary = db["daily-summary"]
dailysummary.insert_one({"date": previousday, "devices": values})
