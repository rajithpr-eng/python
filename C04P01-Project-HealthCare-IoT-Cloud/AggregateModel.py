# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-
import boto3
from DataBase import DataBase

class AggregateModel:

       TABLE = "bsm_agg_data"

       def __init__(self):
           self._db = DataBase()

       def summarize_data_by_device(self, dataset, deviceid, ts):
           values= {}
           # Adding the iot devices data to the appropriate sensor list
           for each in dataset:
               values.setdefault(each["datatype"], {})
               values[each["datatype"]].setdefault("values",[])
               values[each["datatype"]]["values"].append(each["value"])

           # Iterate through devices list and calculate the min, max and aggregate
           for each in dataset:
               values[each["datatype"]]["min_value"] = min(values[each["datatype"]]["values"])
               values[each["datatype"]]["max_value"] = max(values[each["datatype"]]["values"])
               values[each["datatype"]]["count"]     = len(values[each["datatype"]]["values"])
               values[each["datatype"]]["agg_value"] = round(sum(values[each["datatype"]]["values"]) / values[each["datatype"]]["count"],2)


           # Insert the summary into the table
           for k, v in values.items():
               if v:
                   self._db.insert_single_data(AggregateModel.TABLE,
                    { 
                      "sensorid": deviceid + "-" + k,
                      "deviceid": deviceid,
                      "timestamp": ts,
                      "datatype": k,
                      "min_value": v["min_value"],
                      "max_value" : v["max_value"],
                      "agg_value" : v["agg_value"] ,
                      "count" : v["count"]
                    })

       def summarize_data(self, dataset, ts):
           for k, v in dataset.items():
               print("Aggregating the data for device - ", k, "at time - ", ts)
               if v:
                   self.summarize_data_by_device(v, k, ts)
