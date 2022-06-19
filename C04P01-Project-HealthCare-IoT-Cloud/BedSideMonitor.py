'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

 * This  File is modified by GreatLearning.in for the educational purposes. 
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

'''

The Simulator program takes input from the user.
The user input includes the end point name, certificates, etc.
It also includes the topic name and number of device_id to simulate.
The program then goes ahead and publishes the messages from three differnet
sensors in the format:
{deviceid : <BSM_Gxxx>, datatype : <Temperature | Hear Rate | SPO2>, value: <>}
Sensors - Hear Rate, SPO2, Temperature  publish message at frequencies of 1, 10, 15
seconds respectively.

'''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishTimeoutException
from AWSIoTPythonSDK.core.protocol.internal.defaults import DEFAULT_OPERATION_TIMEOUT_SEC
import logging
import datetime
import argparse
import json
import random
import csv
import time
import sched


#Function to publish sensor data for a device at regular intervals
def publishBedSideMonitorData(loopCount, deviceid):
    message = {}
    message['deviceid'] = deviceid
    try:
        if loopCount % PublishFreqTemperature == 0:
            value = float(random.normalvariate(99, 1.5))
            value = round(value, 1)
            timestamp = str(datetime.datetime.now())
            message['timestamp'] = timestamp
            message['datatype'] = 'Temperature'
            message['value'] = value
            messageJson = json.dumps(message)
            myAWSIoTMQTTClient.publish(topic, messageJson, 1)
            #with open('bsm_data.txt', 'a') as f:
            #    print(messageJson, file=f)

        if loopCount % PublishFreqOxygen == 0:
            value = int(random.normalvariate(90,3.0))
            timestamp = str(datetime.datetime.now())
            message['timestamp'] = timestamp
            message['datatype'] = 'SPO2'
            message['value'] = value
            messageJson = json.dumps(message)
            myAWSIoTMQTTClient.publish(topic, messageJson, 1)
            #print('Published topic %s: %s\n' % (topic, messageJson))
            #with open('bsm_data.txt', 'a') as f:
            #    print(messageJson, file=f)

        if loopCount % PublishFreqHeartRate == 0:
            value = int(random.normalvariate(85,12))
            timestamp = str(datetime.datetime.now())
            message['timestamp'] = timestamp
            message['datatype'] = 'HeartRate'
            message['value'] = value
            messageJson = json.dumps(message)
            myAWSIoTMQTTClient.publish(topic, messageJson, 1)
            #with open('bsm_data.txt', 'a') as f:
            #    print(messageJson, file=f)


    except publishTimeoutException:
        print("Unstable connection detected. Wait for {} seconds. No data is pushed on IoT core from {} to {}.".format(DEFAULT_OPERATION_TIMEOUT_SEC, (datetime.datetime.now() - datetime.timedelta(seconds=DEFAULT_OPERATION_TIMEOUT_SEC)), datetime.datetime.now()))


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", required=True, dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", required=True, dest="privateKeyPath", help="Private key file path")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-d", "--device", action="store", dest="device", required=True, help="Device Id")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
clientId = args.clientId
topic = args.topic
device = args.device
port = 443

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
time.sleep(2)


# Publish to the same topic in a loop forever
loopCount = 0

PublishFreqHeartRate = 1
PublishFreqTemperature = 15
PublishFreqOxygen = 10
scheduler = sched.scheduler(time.time, time.sleep)

now = time.time()
while True:
    try :
        scheduler.enterabs(now+loopCount, 1, publishBedSideMonitorData, (loopCount,device))
        loopCount += 1
        scheduler.run()
    except KeyboardInterrupt:
        break

print("Intiate the connection closing process from AWS.")
myAWSIoTMQTTClient.disconnect()
print("Connection closed.")
