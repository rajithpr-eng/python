import pymongo
import json

#Initializing connection to the database
dbclient = pymongo.MongoClient("localhost", 27017)
db = dbclient["iot-db"]
dailysummary = db["daily-summary"]

# Fetch the daily Summary and print it
summaries = dailysummary.find()
for day in summaries:
    print("Date: " + day["date"])
    print ("Device\t\t Device Type\t Min Val\t Max Val\t Count\t Aggregate")
    for device in day["devices"]:
        print(device, "\t", \
            day["devices"][device]["device_type"], "\t", \
            day["devices"][device]["min_value"], "\t", \
            day["devices"][device]["max_value"], "\t", \
            day["devices"][device]["count"], "\t", \
            day["devices"][device]["agg_value"]
        )
