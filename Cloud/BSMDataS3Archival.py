import csv
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import os
import json

# Here we assign our aws clients/resources to use
iot_client = boto3.client('iot',region_name ='us-east-1')
s3 = boto3.resource(service_name = 's3')
dynamodb_resource = boto3.resource('dynamodb',region_name='us-east-1')
table = dynamodb_resource.Table('bsmcloudtest')

# Getting current date and previous date
current_date = datetime.date.today()
previous_date = current_date - datetime.timedelta(days=1)
prevDay = previous_date.day
prevMonth = previous_date.month
prevYear = previous_date.year


# retrive unique device ids from the IOT Core 
response = iot_client.list_things(maxResults=100, thingTypeName='HealthCare')
devices = response["things"]

device_ids = []
for y in devices:
	    device_id = y["thingName"]
	    device_ids.append(device_id)

for device_id in device_ids:
        #condition = Key('deviceid').eq(device_id)& Key('timestamp').between('2021-03-19','2021-03-20')
        condition = Key('deviceid').eq(device_id)& Key('timestamp').between(str(previous_date),str(current_date))
        responsevalues = table.query(KeyConditionExpression=condition)
        if len(responsevalues['Items']) != 0:
                items = responsevalues['Items']
                columns = items[0].keys()
                key = "HealthCareDataArchive/"+ device_id + "/" + str(prevYear) + "/" + str(prevMonth) + "/"
                filename = device_id + "-" + str(prevYear) + "-" + str(prevMonth) + "-" + str(prevDay) + ".csv"
                with open(filename,'a') as f:
                        dict_writer = csv.DictWriter(f, columns)
                        dict_writer.writeheader()
                        for i in items:
                                dict_writer.writerow(i)
                s3.meta.client.upload_file(Filename = filename,Bucket="healthdata",Key=key+filename)

