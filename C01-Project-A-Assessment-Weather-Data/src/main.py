# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

from model import UserModel, DeviceModel, WeatherDataModel
from datetime import datetime

user    = 'admin'
device1 = 'DT001'
device2 = 'DT002'
print(f"Does {user} have admin access?")
user_coll = UserModel(user)
user_document = user_coll.find_by_username(user)
if (user_document and user_document['role'] == 'admin'):
    print("True")
else:
    print("False")

print(f"Is username based query possible for {user}?")
user_document = user_coll.find_by_username('user_2')
if (user_document):
    print(user_document)
else:
    print(user_coll.latest_error)

print(f"Can {user} add a new user?")
user_document = user_coll.insert('user_3', 'user_3@example.com', 'default')
if (user_document):
    print(user_document)
else:
    print(user_coll.latest_error)

print(f"Can {user} access device {device1}?")
device_coll = DeviceModel('admin')
device_document = device_coll.find_by_device_id(device1)
if (device_document):
    print(device_document)
else:
    print(device_coll.latest_error)

print(f"Can {user} create device DT201")
device_document = device_coll.insert('DT201', 'Temperature Sensor', 'Temperature', 'Acme')
if (device_document):
    print(device_document)
else:
    print(device_coll.latest_error)

print(f"Can {user} read DT001 device data?")
wdata_coll = WeatherDataModel('admin')
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document):
    print(wdata_document)
else:
    print(wdata_coll.latest_error)

'''
user    = 'user_1'
print(f"Does {user} have admin access?")
user_coll = UserModel(user)
user_document = user_coll.find_by_username(user)
print(user_document)
if (user_document and user_document['role'] == 'admin'):
    print("True")
else:
    print("False")

print(f"Is username based query possible for {user}?")
user_document = user_coll.find_by_username('user_2')
if (user_document):
    print(user_document)
else:
    print(user_coll.latest_error)

print(f"Can {user} add a new user?")
user_document = user_coll.insert('user_3', 'user_3@example.com', 'default')
if (user_document):
    print(user_document)
else:
    print(user_coll.latest_error)

print(f"Can {user} access device {device1}?")
device_coll = DeviceModel(user)
device_document = device_coll.find_by_device_id(device1)
if (device_document):
    print(device_document)
else:
    print(device_coll.latest_error)

print(f"Can {user} create device DT202")?
device_document = device_coll.insert('DT202', 'Temperature Sensor', 'Temperature', 'Acme')
if (device_document):
    print(device_document)
else:
    print(device_coll.latest_error)

print(f"Can {user} read DT001 device data?")?
wdata_coll = WeatherDataModel('admin')
wdata_document = wdata_coll.find_by_device_id_and_timestamp('DT002', datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document):
    print(wdata_document)
else:
    print(wdata_coll.latest_error)


# Shows a failed attempt on how to insert a new data point
wdata_document = wdata_coll.insert('DT002', 12, datetime(2020, 12, 2, 13, 30, 0))
if (wdata_document == -1):
    print(wdata_coll.latest_error)
else:
    print(wdata_document)
'''
