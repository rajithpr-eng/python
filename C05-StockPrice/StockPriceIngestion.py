import json
import boto3
import sys
import yfinance as yf

import time
import random
import datetime


# Your goal is to get per-hour stock price data for a time range for the ten stocks specified in the doc.
# Further, you should call the static info api for the stocks to get their current 52WeekHigh and 52WeekLow values.
# You should craft individual data records with information about the stockid, price, price timestamp, 52WeekHigh and 52WeekLow values and push them individually on the Kinesis stream

kinesis = boto3.client('kinesis', region_name = "us-east-2") #Modify this line of code according to your requirement.

dayfrom = "2022-07-01"
dayto   = "2022-07-31"

## Add code to pull the data for the stocks specified in the doc
companies = ["MSFT", "MVIS", "GOOG", "SPOT", "INO", "OCGN", "ABML", "RLLCF", "JNJ", "PSFE"]
company_stock_dict = dict()
for each in companies:
    df = yf.download(each, start = dayfrom, end= dayto, interval= "1h")
    json_string = df.to_json(orient='split')
    table = json.loads(json_string)
    record_len = len(table['index'])
    price_list = list()
    for i in range(0, record_len):
        price_dict = dict()
        timestamp = table['index'][i]
        dt_obj = datetime.datetime.fromtimestamp(timestamp/1000.0)
        price_dict['timestamp'] = dt_obj.strftime("%m/%d/%Y, %H:%M:%S")
        price_dict['date'] = dt_obj.strftime("%m/%d/%Y")
        price_dict['price'] = table['data'][i][3]
        price_list.append(price_dict)
    company_stock_dict[each] = price_list

## Add additional code to call 'info' API to get 52WeekHigh and 52WeekLow refering this this link - https://pypi.org/project/yfinance/
company_info_dict = dict()
for each in companies:
   info_dict = dict()
   dt = yf.Ticker(each)
   info_dict['52WeekLow']  = dt.info['fiftyTwoWeekLow']
   info_dict['52WeekHigh'] = dt.info['fiftyTwoWeekHigh']
   company_info_dict[each] = info_dict

## Add your code here to push data records to Kinesis stream.
for each in companies:
    stock_list = company_stock_dict[each]
    for stock in stock_list:
        record = dict()
        record['stockid'] = each
        record.update(company_info_dict[each])
        record.update(stock)
        print(record)
        kinesis.put_record(StreamName = "StockAlert", Data = json.dumps(record), PartitionKey = str(hash(record['stockid'])))
