
import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883
WAIT_TIME = 0.25

class Edge_Server:

    def __init__(self, instance_name):
        self._instance_id = instance_name
        self.client = mqtt.Client(self._instance_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._registered_list = []

    # Terminating the MQTT broker and stopping the execution
    def terminate(self):
        self.client.disconnect()
        self.client.loop_stop()

    # Connect method to subscribe to various topics.
    def _on_connect(self, client, userdata, flags, result_code):
        self.client.subscribe("server")

    def _on_disconnect(self, client, userdata, result_code):
        pass

    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self, query_type):
        print("\nCommand to get status for", query_type, "is intiated")

        # Prepare message
        message = {}
        message["type"]        = "GET_STATUS"
        message["device_id"]   = "server"

        #Publish the message
        self.client.publish(query_type, json.dumps(message))

    # Controlling and performing the operations on the devices
    # based on the request received
    def set_status(self, query_type, switch_state = None, intensity = None, temperature = None):
        print("\nCommand to set status for", query_type, "is intiated")

       #Prepare message
        message = {}
        payload = {}
        message["type"]         = "SET_STATUS"
        message["device_id"]    = "server"
        if switch_state is not None:
            payload["switch_state"] = switch_state
        if intensity is not None:
            payload["intensity"] = intensity
        if temperature is not None:
            payload["temperature"] = temperature
        message["payload"]      = payload

        #Publish the message
        self.client.publish(query_type, json.dumps(message))

    def handle_msg_registration(self, message):
        #Acknowledge the receipt
        payload = message["payload"]
        print("\nRegistration request is acknowledged for device","'", payload["device_id"],"' in", payload["room_type"])

        # Record the registration in the list
        self._registered_list.append(message["device_id"])
        print("Request is processed for" , message["device_id"])

        # Prepare message to ACK
        message_ack = {}
        payload_ack = {}
        message_ack["type"]        = "REGISTER_ACK"
        message_ack["device_id"]   = message["device_id"]
        payload_ack["status"]      = "True"
        message_ack["payload"]     = payload_ack

        #Publish the message
        self.client.publish(message["device_id"], json.dumps(message_ack))

    def handle_msg_get_status_ack(self, message):
        print("Here is the current device-status for", message["device_id"], ":", message["payload"])

    def handle_msg_set_status_ack(self, message):
        payload = message["payload"]

        if payload["status"] == "False":
          print("Set failed for device", message["device_id"], ":", payload)
          return

        # Prepare message
        message_ack = {}
        message_ack["type"]        = "GET_STATUS"
        message_ack["device_id"]   = "server"

        #Publish the message
        self.client.publish(message["device_id"], json.dumps(message_ack))

    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        message = json.loads(msg.payload)
        if message["type"] == "REGISTER" :
           self.handle_msg_registration(message)
        elif message["type"] == "GET_STATUS_ACK" :
           self.handle_msg_get_status_ack(message)
        elif message["type"] == "SET_STATUS_ACK" :
           self.handle_msg_set_status_ack(message)
