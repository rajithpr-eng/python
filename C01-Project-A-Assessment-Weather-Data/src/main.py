# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

from model import *
from datetime import datetime, timedelta

device1 = 'DT001'
device2 = 'DT002'

#1.a Demonstration for admin
user    = 'admin'
print(f"Does {user} have admin access?")
user_coll = UserModel(user)
user_document = user_coll.find_by_username(user)
if ((user_document != -1) and (user_document['role'] == 'admin')):
    print("True")
else:
    print("False")
print("\n")

print(f"Is username based query possible for {user}?")
user_document = user_coll.find_by_username('user_2')
if (user_document != -1):
    print(user_document)
else:
    print(user_coll.latest_error)
print("\n")

print(f"Can {user} add a new user?")
user_document = user_coll.insert('user_3', 'user_3@example.com', 'default')
if (user_document != -1):
    print(user_document)
else:
    print(user_coll.latest_error)
print("\n")

print(f"Can {user} access device {device1}?")
device_coll = DeviceModel(user)
device_document = device_coll.find_by_device_id(device1)
if (device_document != -1):
    print(device_document)
else:
    print(device_coll.latest_error)
print("\n")

print(f"Can {user} create device DT201")
device_document = device_coll.insert('DT201', 'Temperature Sensor', 'Temperature', 'Acme')
if (device_document != -1):
    print(device_document)
else:
    print(device_coll.latest_error)
print("\n")

print(f"Can {user} read DT001 device data?")
wdata_coll = WeatherDataModel(user)
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document != -1):
    print(wdata_document)
else:
    print(wdata_coll.latest_error)
print("\n")

print(f"Can {user} create DT201 device data?")
wdata_document = wdata_coll.insert('DT201', 25, datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document != -1):
    print(wdata_document)
else:
    print(wdata_coll.latest_error)
print("\n")

#1.a Demonstration for default user
user    = 'user_1'
print(f"Does {user} have admin access?")
user_coll = UserModel(user)
user_document = user_coll.find_by_username(user)
if ((user_document != -1) and (user_document['role'] == 'admin')):
    print("True")
else:
    print("False")
print("\n")

print(f"Is username based query possible for {user}?")
user_document = user_coll.find_by_username('user_2')
if (user_document != -1):
    print(user_document)
else:
    print(user_coll.latest_error)
print("\n")

print(f"Can {user} add a new user?")
user_document = user_coll.insert('user_4', 'user_4@example.com', 'default')
if (user_document != -1):
    print(user_document)
else:
    print(user_coll.latest_error)
print("\n")

print(f"Can {user} access device {device1}?")
device_coll = DeviceModel(user)
device_document = device_coll.find_by_device_id(device1)
if (device_document != -1):
    print(device_document)
else:
    print(device_coll.latest_error)
print("\n")

print(f"Can {user} access device DT300?")
device_coll1 = DeviceModel(user)
device_document = device_coll.find_by_device_id('DT300')
if (device_document != -1):
    print(device_document)
else:
    print(device_coll.latest_error)
print("\n")

print(f"Can {user} create device DT202")
device_document = device_coll.insert('DT202', 'Temperature Sensor', 'Temperature', 'Acme')
if (device_document != -1):
    print(device_document)
else:
    print(device_coll.latest_error)
print("\n")

print(f"Can {user} create device DT203")
device_document = device_coll.insert('DT203', 'Temperature Sensor', 'Temperature', 'Acme')
if (device_document != -1):
    print(device_document)
else:
    print(device_coll.latest_error)
print("\n")

print(f"Can {user} read DT001 device data?")
wdata_coll = WeatherDataModel(user)
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document != -1):
    print(wdata_document)
else:
    print(wdata_coll.latest_error)
print("\n")

print(f"Can {user} read DT300 device data?")
wdata_coll = WeatherDataModel(user)
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT300', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document != -1):
    print(wdata_document)
else:
    print(wdata_coll.latest_error)
print("\n")

print(f"Can {user} create DT202 device data?")
wdata_document = wdata_coll.insert('DT202', 25, datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document != -1):
    print(wdata_document)
else:
    print(wdata_coll.latest_error)
print("\n")

print(f"Can {user} create DT203 device data?")
wdata_document = wdata_coll.insert('DT203', 25, datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document != -1):
    print(wdata_document)
else:
    print(wdata_coll.latest_error)
print("\n")

#2.b Demonstration of daily report generation
print("Generating daily report from WeatherData Collection");
data_aggregator(wdata_coll)

#2.c Demonstration of data retrieval function from daily report collection
start = datetime.strptime("2020-12-01", "%Y-%m-%d")
end = datetime.strptime("2020-12-05", "%Y-%m-%d")
sd = start.date()
ed = end.date()
date_generated = [sd + timedelta(days=x) for x in range(0, (ed-sd).days)]
dr_list = data_retrieve(device1, date_generated)
print(f"Reported generated from {sd} to {ed} for device{device1} is:")
for each in dr_list:
    print(each)
