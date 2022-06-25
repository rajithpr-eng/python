# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-
import boto3
from DataBase import DataBase

class AggregateModel:

       # Class variable to store the table name for the AggregateModel
       TABLE = "bsm_agg_data"

       #Constructor to initialize an AggregateModel object
       def __init__(self):
           self._db = DataBase()

       #Method to summarize data in the dataset for a device
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

       # Method to summarize records in the dataset
       def summarize_data(self, dataset, ts):
           for k, v in dataset.items():
               print("Aggregating the data for device - ", k, "at time - ", ts)
               if v:
                   self.summarize_data_by_device(v, k, ts)

       #Method to get data for a sensor within a given range
       def get_data_by_sensorid_n_ts_range(self, sensorid, lowts, hights):
           rec = self._db.query_table_by_pk_n_range(AggregateModel.TABLE, "sensorid", sensorid, lowts, hights)
           return rec['Items']

