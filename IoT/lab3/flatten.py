import datetime
import pymongo
import json

today = datetime.date.today()                        # datetime.date(2021, 1, 15)
prevday = today-datetime.timedelta(days=1)           #datetime.date(2021, 1, 14)
prevday = prevday.strftime("%Y-%m-%dT00:00:00Z")   #'2021-01-14T00:00:00Z'
today = today.strftime("%Y-%m-%dT00:00:00Z")         #'2021-01-15T00:00:00Z'

#Initializing connection to the database
dbclient = pymongo.MongoClient("localhost", 27017)
db = dbclient["iot-db"]
dbt = db["iot-sensors-data-timestamped"]

#Querying for the messages that were published the previous day
prevday_entries = dbt.find({"timestamp":  {"$gte": prevday, "$lt" : today}})

# Define the collection to store previous day entries
pde_flattened = db["iot-sensors-data-flattened"]

# Iterate through every datapoint
for entry in prevday_entries:
    # Load the value of payload field as json
    payload = json.loads(entry["payload"])
    
    #Iterate through every field in the payload and add it to the datapoint
    for field in payload:
        entry[field] = payload[field]
    
    # Delete the payload field since it has been flattened
    del entry["payload"]
    
    # Insert the flattened datapoint to collection
    pde_flattened.insert_one(entry)
