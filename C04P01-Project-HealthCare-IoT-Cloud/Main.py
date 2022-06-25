# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-
from RawDataModel import *
from AggregateModel import AggregateModel
from AlertDataModel import AlertDataModel
import time
from datetime import datetime, date, time, timedelta

'''
This is the driver code for the similator.
Before running the code make sure on AWS bsm_raw_data table is populated.
The deviceids contain the list of deviced ids
The low and high contain the lower and higher timestamps for which aggregation
and alert generation needs to be computed.
'''

deviceids = ['BSM_G000', 'BSM_G001']
low       = '2022-06-25 00:11:00'
high      = '2022-06-25 01:11:00'

#Instantiate all the three DataModels
rd_ml = RawDataModel(deviceids)
ag_ml = AggregateModel()
ad_ml = AlertDataModel(deviceids, ag_ml)

#For every minute from low to high get the date raw data, compute and store the aggregated data
low_time  = datetime.strptime(low, '%Y-%m-%d %H:%M:%S')
high_time = datetime.strptime(high, '%Y-%m-%d %H:%M:%S')
cur_time = low_time
while cur_time < high_time:
    nt  = get_next_minute_time(cur_time)
    cur = cur_time.strftime('%Y-%m-%d %H:%M:%S')
    n   = nt.strftime('%Y-%m-%d %H:%M:%S')
    dataset = rd_ml.get_data_by_ts_range(cur, n)
    ag_ml.summarize_data(dataset, cur)
    cur_time = nt

#Generate alerts for the aggregated data between low and high timestamps
ad_ml.generate_alerts(low, high)
