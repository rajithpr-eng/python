import pymongo
import datetime
import json

# Initializing connection to the database
dbclient = pymongo.MongoClient("localhost", 27017)
db = dbclient["iot-db"]
dailysummary = db["daily-summary"]


previousday = datetime.date.today() - datetime.timedelta(days=1)
previousday = previousday.strftime("%Y-%m-%d")

# Querying for the objects that were published on the previous day
entries = dailysummary.find({"date": previousday})

# Extract the devices summary from the object
devices = entries[0]["devices"]

# Read the alert rules
alerts_config_file=open('alerts_config.json')
alerts_config = json.loads(alerts_config_file.read())
alerts_config_file.close()

# Iterating through each rule and printing an alert when devices value is over the threshold
for rule in alerts_config:
    for device in devices:
        if(devices[device]["device_type"]==rule):
            if(devices[device]["max_value"]>alerts_config[rule]):
                print(device + " has its max value beyond the threshold value on " + previousday)
