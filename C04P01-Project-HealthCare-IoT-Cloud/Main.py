# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-
from RawDataModel import *
from AggregateModel import AggregateModel
import time
from datetime import datetime, date, time, timedelta


deviceids = ['BSM_G000', 'BSM_G001']
low       = '2022-06-19 17:34:01'
high      = '2022-06-19 19:34:01'

rd_ml = RawDataModel(deviceids)
ag_ml = AggregateModel()

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


