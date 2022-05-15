import json
import paho.mqtt.client as mqtt

HOST = "localhost"
PORT = 1883


class Light_Device():

    # setting up the intensity choices for Smart Light Bulb
    _INTENSITY = ["LOW", "HIGH", "MEDIUM", "OFF"]

    _SWITCH_STATE = ["ON", "OFF"]

    def __init__(self, device_id, room):
        # Assigning device level information for each of the devices.
        self._device_id = device_id
        self._room_type = room
        self._light_intensity = self._INTENSITY[0]
        self._device_type = "LIGHT"
        self._device_registration_flag = False
        self.client = mqtt.Client(self._device_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(HOST, PORT, keepalive=60)
        self.client.loop_start()
        self._register_device(self._device_id, self._room_type, self._device_type)
        self._switch_status = "OFF"

    def _register_device(self, device_id, room_type, device_type):
        message = {}
        payload = {}
        message["type"]        = "REGISTER"
        message["device_id"]   = device_id
        payload["device_id"]   = device_id
        payload["device_type"] = device_type
        payload["room_type"]   = room_type
        message["payload"]     = payload
        #Publish the message
        self.client.publish("server", json.dumps(message))

    # Connect method to subscribe to various topics.
    def _on_connect(self, client, userdata, flags, result_code):
        self.client.subscribe("devices")
        self.client.subscribe(self._device_type)
        self.client.subscribe(self._room_type)
        self.client.subscribe(self._device_id)

    def _on_disconnect(self, client, userdata, result_code):
        self.client.disconnect()
        self.client.loop_stop()

    # method to process the recieved messages and publish them on relevant topics
    # this method can also be used to take the action based on received commands
    def _on_message(self, client, userdata, msg):
        message = json.loads(msg.payload)
        if message["type"] == "REGISTER_ACK" :
            self.handle_msg_registration_ack(message)
        elif message["type"] == "GET_STATUS" :
            self.handle_msg_get_status(message)
        elif message["type"] == "SET_STATUS" :
            self.handle_msg_set_status(message)


    # Getting the current switch status of devices
    def _get_switch_status(self):
        return self._switch_status

    # Setting the the switch of devices
    def _set_switch_status(self, switch_state):
        if switch_state in self._SWITCH_STATE :
            self._switch_status = switch_state
            return True
        else:
            return False

    # Getting the light intensity for the devices
    def _get_light_intensity(self):
        return self._light_intensity

    # Setting the light intensity for devices
    def _set_light_intensity(self, light_intensity):
        if light_intensity in self._INTENSITY :
            self._light_intensity = light_intensity
            return True
        else:
            return False

    def handle_msg_registration_ack(self, message) :
        payload = message["payload"]
        print("LIGHT-DEVICE registered! - Registration status is available for '", message["device_id"], "' : ", payload["status"])
        self._device_registration_flag = True

    def handle_msg_get_status(self, message) :
        #Prepare the message
        message_ack = {}
        payload_ack = {}
        message_ack["type"]           = "GET_STATUS_ACK"
        message_ack["device_id"]      = self._device_id
        payload_ack["status"]         = "True"
        payload_ack["device_id"]      = self._device_id
        payload_ack["switch_state"]   = self._switch_status
        payload_ack["intensity"]      = self._light_intensity
        message_ack["payload"]        = payload_ack

        #Publish the message
        self.client.publish("server", json.dumps(message_ack))

    def handle_msg_set_status(self, message) :
        to_be_ignored = True
        payload = message["payload"]
        error   = []

        #Set switch state
        if "switch_state" in payload.keys() :
            if self._set_switch_status(payload["switch_state"]) is False:
                error.append("Invalid switch state: " + payload["switch_state"])
            to_be_ignored = False

        #Set intensity
        if "intensity" in payload.keys() :
            if self._set_light_intensity(payload["intensity"]) is False :
                error.append("Invalid intensity: " + payload["intensity"])
            to_be_ignored = False

        if to_be_ignored is True:
            return

        #Prepare the message
        message_ack = {}
        payload_ack = {}
        message_ack["type"]           = "SET_STATUS_ACK"
        message_ack["device_id"]      = self._device_id
        if len(error) > 0 :
            payload_ack["status"]     = "False"
            payload_ack["errors"]     =  error
        else :
            payload_ack["status"]     = "True"
        message_ack["payload"]        = payload_ack

        #Publish the message
        self.client.publish("server", json.dumps(message_ack))

