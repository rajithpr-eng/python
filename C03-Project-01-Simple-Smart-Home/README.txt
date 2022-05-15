The project can be run by simply running the main.py.
Before running ensure the MQTT service is running on localhost and default port.
The code does the following:-
1) 5 Lights and 3 Ac devices are created.
2) The devices are assigned to 5 rooms - Kitchen, BR1, BR2, Garrange and Living
3) The devices and Edge server connect to MQTT server
4) The server listens on a single topic - server
5) The devices listens to dedicated topic - device_id and also common topics
6) The common topics include - devices, device_type - AC or LIGHT, room_type - Kitche, BR1, BR2, Garrage or Living based on the attributes passed in the device's constructor.
7) The MQTT Message payload is encoded in json format
   {
     "type": <value>
     "device_id": <value>
     "payload": <value>
   }
8) The payload attribute itself is a dictionary and encoded based on the type attribute. Detains on commented in the source code.
9) The test cases include:
9.1) Device Registration
9.2) Getting Status of devices by device_id, device_type, room_type, all
9.3) Setting switch ON by device_id, device_type, room_type, all
9.4) Setting lights to different intensity by device_id, device_type, room_type, all
9.5) Setting AC to different temperature by device_id, device_type, room_type, all
9.6) Setting AC to temperature below MIN and above MAX 
9.7) Setting lights to invalid intensity
