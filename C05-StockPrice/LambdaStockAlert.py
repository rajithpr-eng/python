from pprint import pprint
import boto3
import json
import csv
import datetime
import os
import random
import base64
from decimal import *

def lambda_handler(event, context):
    dynamodb_res = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb_res.Table('StockAlert')
    client = boto3.client('sns', region_name='us-east-2')
    topic_arn = "arn:aws:sns:us-east-2:883410434182:StockAlert"
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        payload = str(payload, 'utf-8')
        payload_rec = json.loads(payload, parse_float=Decimal)
        print(payload_rec)
        dbkey = dict()
        dbkey['stockid'] = payload_rec['stockid']
        dbkey['date'] = payload_rec['date']       
        if (payload_rec['price'] * Decimal(0.2)) >= payload_rec['52WeekHigh']:
            response = table.get_item(Key=dbkey)
            if 'Item' not in response:
                table.put_item(Item=payload_rec)
                message = payload_rec['stockid'] + "at" + payload_rec['timestamp'] + "reahing close to 52WeekHigh"
                client.publish(TopicArn=topic_arn, Message=message, Subject="Stock Alert")
        if (payload_rec['price'] * Decimal(0.8)) <= payload_rec['52WeekLow']:
            response = table.get_item(Key=dbkey)
            if 'Item' not in response:
                table.put_item(Item=payload_rec)
                message = payload_rec['stockid'] + "at" + payload_rec['timestamp'] + "reaching close to 52WeekLow"
                client.publish(TopicArn=topic_arn, Message=message, Subject="Stock Alert")
    return 0
