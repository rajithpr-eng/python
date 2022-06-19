# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-
import boto3
from boto3.dynamodb.conditions import Key

class DataBase:

    _dynamodb = None

    def __init__(self):
        if DataBase._dynamodb is None:
            DataBase._dynamodb = boto3.resource('dynamodb')

    def insert_single_data(self, table, data):
        hdl = DataBase._dynamodb.Table(table)
        hdl.put_item(Item=data)

    def query_table_by_pk_n_range(self, table, pk, low, high):
        hdl = DataBase._dynamodb.Table(table)
        response = hdl.query(KeyConditionExpression=Key('deviceid').eq(pk) & Key('timestamp').between(low, high))
        return response
