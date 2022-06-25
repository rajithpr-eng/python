# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-
import boto3
from DataBase import DataBase
import datetime

class RawDataModel:

       # Class attribute for the RawDataModel
       TABLE = "bsm_raw_data"

       # Contructor to initialize RawDataModel instance
       def __init__(self, deviceids):
           self._db = DataBase()
           self._deviceids = deviceids

      # Method to get records between a range of timestamps
       def get_data_by_ts_range(self, lowts, hights):
           result = {}
           for each in self._deviceids:
               rec = self._db.query_table_by_pk_n_range(RawDataModel.TABLE, "deviceid", each, lowts, hights)
               result.setdefault(each, {})
               result[each] = rec['Items']
           return result

# A utility function to get the next minutue for a given timestamp
def get_next_minute_time(t):
    return t + datetime.timedelta(minutes=1)
