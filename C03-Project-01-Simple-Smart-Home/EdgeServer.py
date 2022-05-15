
import json
import time
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883
WAIT_TIME = 0.25

class Edge_Server:

    def __init__(self, instance_name):
        # Connect with MQTT Server running on localhost and default port
        # Register the MQTT callbacks and start the loop
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
        # The server listens on a specific topic - server
        self.client.subscribe("server")

    def _on_disconnect(self, client, userdata, result_code):
        self.client.disconnect()
        self.client.loop_stop()

    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        # Call the corresponding message handler
        message = json.loads(msg.payload)
        if message["type"] == "REGISTER" :
           self.handle_msg_registration(message)
        elif message["type"] == "GET_STATUS_ACK" :
           self.handle_msg_get_status_ack(message)
        elif message["type"] == "SET_STATUS_ACK" :
           self.handle_msg_set_status_ack(message)

    # Returning the current registered list
    def get_registered_device_list(self):
        return self._registered_list

    # Getting the status for the connected devices
    def get_status(self, query_type):
        print("\nCommand to get status for", query_type, "is intiated")

        # 2a) (i) The MQTT Message encoding for gettins STATUS from device
        #     Format {
        #        "type"      : "GET_STATUS",
        #        "device_id" : "server",
        #      }

        # Prepare message
        message = {}
        message["type"]        = "GET_STATUS"
        message["device_id"]   = "server"

        #Publish the message to the channel passed by user
        self.client.publish(query_type, json.dumps(message))

    # Controlling and performing the operations on the devices
    # based on the request received
    def set_status(self, query_type, switch_state = None, intensity = None, temperature = None):
        print("\nCommand to set status for", query_type, "is intiated")
        # 2b) (i) or 3b) (i) The MQTT Message encoding for setting STATUS
        #     Format {
        #        "type"      : "SET_STATUS",
        #        "device_id" : "server",
        #        "payload"   : {
        #            "switch_state": <value>,
        #            "intensity"   : <value>,
        #            "temperature" : <value>,
        #        }
        #      }


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

        #Publish the message on the channel passed by user
        self.client.publish(query_type, json.dumps(message))

    def handle_msg_registration(self, message):
        # 1a) (ii) On receiving registration message
        #          store the information in the device list and repond with a
        #          conformation message.
        #Acknowledge the receipt
        payload = message["payload"]
        print("\nRegistration request is acknowledged for device","'", payload["device_id"],"' in", payload["room_type"])

        # Record the registration in the list
        self._registered_list.append(message["device_id"])
        print("Request is processed for" , message["device_id"])

        # 1a) (ii) The MQTT Message encoding for sending confirmation message
        #     Format {
        #        "type"      : "REGISTRATION_ACK",
        #        "device_id" : <device_id>,
        #        "payload"   : {
        #            "status"      : True,
        #        }
        #      }

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
        # 2a) (ii) or 2b) (ii)
        # 3a) (ii) or 3b) (ii)
        # Notify the status collected from device
        print("Here is the current device-status for", message["device_id"], ":", message["payload"])

    def handle_msg_set_status_ack(self, message):
        # 2a) (ii) or 2b) (ii)
        # 3a) (ii) or 3b) (ii)
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

