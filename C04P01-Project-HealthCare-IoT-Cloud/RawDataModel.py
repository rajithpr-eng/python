# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-
import boto3
from DataBase import DataBase
import datetime

class RawDataModel:

       TABLE = "bsm_raw_data"

       def __init__(self, deviceids):
           self._db = DataBase()
           self._deviceids = deviceids

       def get_data_by_ts_range(self, lowts, hights):
           result = {}
           for each in self._deviceids:
               rec = self._db.query_table_by_pk_n_range(RawDataModel.TABLE, each, lowts, hights)
               result.setdefault(each, {})
               result[each] = rec['Items']
           return result

def get_next_minute_time(t):
    return t + datetime.timedelta(minutes=1)
