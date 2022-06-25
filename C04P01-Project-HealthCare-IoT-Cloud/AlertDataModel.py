# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-
import boto3
import json
from DataBase import DataBase

class AlertDataModel:

       #Class variables to store the table name and rule file name
       TABLE = "bsm_alerts"
       FILE  = "rules.json"

       #Constructor to initialize the AlerDataModel object
       def __init__(self, dev_ids, agm_obj):
           self._db      = DataBase()
           # Open and store the json file into a dictionary
           hdl           = open(AlertDataModel.FILE)
           self._rdict   = json.load(hdl)
           hdl.close()
           self._agm_obj = agm_obj
           self._devids  = dev_ids

       #Method to generate alerts for a device and sensor within a timerange
       def generate_alerts_by_deviceid_n_srule(self, deviceid, rule, lowts, hights):
           #Derivive composite key for the aggr table and get the records withing the time range
           sensorid = deviceid + "-" + rule["type"]
           items = self._agm_obj.get_data_by_sensorid_n_ts_range(sensorid, lowts, hights)

           #Init the breach counters and breate start flag
           bc = {"min": 0, "max": 0}
           bc_started  = 0
           for each in items:
               bc_detected = 0
               #Detect min/max breach
               if each["agg_value"] < rule["avg_min"]:
                   bc["min"] = bc["min"] + 1
                   bc_detected = 1
               if each["agg_value"] > rule["avg_max"]:
                   bc["max"] = bc["max"] + 1
                   bc_detected = 1

               #If breach has started and there was no breach in current iteration reset the counters and flag so that we start a fresh.
               #If breach was not started and current iteration we detected breach then record the timestamp where it begins and set the brech started flag.
               if bc_started:
                   if bc_detected == 0:
                       bc["min"]  = 0
                       bc["max"]  = 0
                       bc_started = 0
               else:
                   if bc_detected == 1:
                       bc_started = 1
                       timestamp = each["timestamp"]

               #If breach detected contiguosly for trigger times then raise alert
               if bc["min"] + bc["max"] >= rule["trigger_count"]:
                   if bc["min"] == 0:
                       print("Alert for device_id ", deviceid, " on ", rule["id"], "starting at ", timestamp, "with breach type max")
                   elif bc["max"] == 0:
                       print("Alert for device_id ", deviceid, " on ", rule["id"], "starting at ", timestamp, "with breach type min")
                   else:
                       print("Alert for device_id ", deviceid, " on ", rule["id"], "starting at ", timestamp, "with breach type min/max")
                   self._db.insert_single_data(AlertDataModel.TABLE,
                    {
                      "sensorid" : sensorid,
                      "deviceid" : deviceid,
                      "datatype" : rule["type"],
                      "timestamp": timestamp,
                      "rule"     : rule["id"],
                    })
                   bc["min"] = 0
                   bc["max"] = 0
                   bc_started = 0


       #Method to generate alerts for agg data within a timerange
       def generate_alerts(self, lowts, hights):
           for each in self._devids:
               print("Processing the data for device - ", each)
               for rule in self._rdict["rules"]:
                   self.generate_alerts_by_deviceid_n_srule(each, rule, lowts, hights)
