# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-
import boto3
from boto3.dynamodb.conditions import Key

class DataBase:

    # Class variable to store handle to AWS dynamodb resource
    _dynamodb = None

    # Constructor to initialize the Database object
    def __init__(self):
        if DataBase._dynamodb is None:
            DataBase._dynamodb = boto3.resource('dynamodb')

    # Method to insert a record into a table
    # Caller has to takecare of inserting data with the right partition and sort
    # ket attributes for the table
    def insert_single_data(self, table, data):
        hdl = DataBase._dynamodb.Table(table)
        hdl.put_item(Item=data)

    # Method to get all the records that match a partion key and range of timestamp/sort
    # key. Caller to takecare of passing the right parition and sort key
    # attributes for the table
    def query_table_by_pk_n_range(self, table, pk, pkv, low, high):
        hdl = DataBase._dynamodb.Table(table)
        response = hdl.query(KeyConditionExpression=Key(pk).eq(pkv) & Key('timestamp').between(low, high))
        return response
