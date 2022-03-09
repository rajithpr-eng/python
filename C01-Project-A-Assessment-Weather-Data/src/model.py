# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

# Imports Database class from the project to provide basic functionality for database access
from database import Database
# Imports ObjectId to convert to the correct format before querying in the db
from bson.objectid import ObjectId

class AbstractCollectionModel:

    def __init__(self, username):
        self._db = Database()
        self._latest_error = ''
        self.username = username
        self.user_access_client_obj = UserAccessClient();

    # Latest error is used to store the error string in case an issue. It's reset at the beginning of a new function call
    @property
    def latest_error(self):
        return self._latest_error

    # Private function (starting with __) to be used as the base for all find functions
    def find(self, collection, key):
        document = self._db.get_single_data(collection, key)
        return document

    # Finds a document based on the unique auto-generated MongoDB object id
    def find_by_object_id(self, collection, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.find(collection, key)

    def insert(self, collection, data):
        obj_id = self._db.insert_single_data(collection, data)
        return self.find_by_object_id(collection, obj_id)


# User document contains username (String), email (String), and role (String) fields
class UserModel(AbstractCollectionModel):
    USER_COLLECTION = 'users'

    def __init__(self, username):
        super().__init__(username);

    # Since username should be unique in users collection, this provides a way to fetch the user document based on the username
    def find_by_username(self, username):
        key = {'username': username}
        return self.find(UserModel.USER_COLLECTION, key)

    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, username, email, role):
        self._latest_error = ''
        user_document = self.find_by_username(username)
        if (user_document):
            self._latest_error = f'Username {username} already exists'
            return -1

        user_data = {'username': username, 'email': email, 'role': role}
        return super().insert(UserModel.USER_COLLECTION, user_data);

    def update(self, username, device_id, access_rights):
        pass


# Device document contains device_id (String), desc (String), type (String - temperature/humidity) and manufacturer (String) fields
class DeviceModel(AbstractCollectionModel):
    DEVICE_COLLECTION = 'devices'

    def __init__(self, username):
        super().__init__(username);

    def find_by_device_id(self, device_id):
        data = {'device_id': device_id}
        return self.user_access_client_obj.handle_db_access(self.username, 'r', self, data)

    # Since device id should be unique in devices collection, this provides a way to fetch the device document based on the device id
    def read(self, data):
        return self.find(DeviceModel.DEVICE_COLLECTION, data)

    def read_denied(self, data):
        self._latest_error = ''
        self._latest_error = f'Read access denied to User {self.username}'
        return -1

    def insert(self, device_id, desc, type, manufacturer):
        data = {'device_id': device_id, 'desc': desc, 'type': type, 'manufacturer': manufacturer}
        self.user_access_client_obj.handle_db_access(self.username, 'w', self, data)

    # This first checks if a device already exists with that device id. If it does, it populates latest_error and returns -1
    # If a device doesn't already exist, it'll insert a new document and return the same to the caller
    def write(self, data):
        self._latest_error = ''
        device_id = data['device_id']
        device_document = self.read(data)
        if (device_document):
            self._latest_error = f'Device id {device_id} already exists'
            return -1

        return super().insert(DeviceModel.DEVICE_COLLECTION, data);

    def write_denied(self, data):
        self._latest_error = ''
        self._latest_error = f'Write access denied to User {self.username}'
        return -1


# Weather data document contains device_id (String), value (Integer), and timestamp (Date) fields
class WeatherDataModel(AbstractCollectionModel):
    WEATHER_DATA_COLLECTION = 'weather_data'

    def __init__(self, username):
        super().__init__(username);

    # Since device id and timestamp should be unique in weather_data collection, this provides a way to fetch the data document based on the device id and timestamp
    def find_by_device_id_and_timestamp(self, device_id, timestamp):
        data = {'device_id': device_id, 'timestamp': timestamp}
        return self.user_access_client_obj.handle_db_access(self.username, 'r', self, data)

    def read(self, data):
        return self.find(WeatherDataModel.WEATHER_DATA_COLLECTION, data)

    def read_denied(self, data):
        self._latest_error = ''
        self._latest_error = f'Read access denied to User {self.username}'
        return -1

    # This first checks if a data item already exists at a particular timestamp for a device id. If it does, it populates latest_error and returns -1.
    # If it doesn't already exist, it'll insert a new document and return the same to the caller
    def insert(self, device_id, value, timestamp):
        data = {'device_id': device_id, 'value': value, 'timestamp': timestamp}
        self.user_access_client_obj.handle_db_access(self.username, 'w', self, data)

    def write(self, data):
        self._latest_error = ''
        device_id = data['device_id']
        timestamp = data['timestamp']
        wdata_document = self.read(data)
        if (wdata_document):
            self._latest_error = f'Data for timestamp {timestamp} for device id {device_id} already exists'
            return -1

        return super().insert(WeatherDataModel.WEATHER_DATA_COLLECTION, data);

    def write_denied(self, data):
        self._latest_error = ''
        self._latest_error = f'Write access denied to User {self.username}'
        return -1


class UserAccessClient:

    def handle_db_access(self, username, access_mode, model_obj, data):
        user_model = UserModel(username)
        user_dict = user_model.find_by_username(username)
        if (user_dict) :
            if user_dict['role'] == 'admin':
                user_access_obj = AdminUserAccess()
            else:
                user_access_obj = DefaultUserAccess()
        else:
            return -1
        if access_mode == 'r':
            return user_access_obj.handle_read(user_dict, model_obj, data)
        else:
            return user_access_obj.handle_write(user_dict, model_obj, data)


class UserAccess:
    pass

class DefaultUserAccess(UserAccess):

    def handle_read(self, user_dict, model_obj, data):
        if user_dict['access']['device'] == ('r' or 'rw'):
            return model_obj.read(data)
        else:
            return model_obj.read_denied(data)

    def handle_write(self, user_dict, model_obj, data):
        if user_dict['access']['device'] == ('w' or 'rw'):
            return model_obj.write(data)
        else:
            return model_obj.write_denied(data)

class AdminUserAccess(UserAccess):

    def handle_read(self, user_dict, model_obj, data):
        return model_obj.read(data)

    def handle_write(self, user_dict, model_obj, data):
        return model_obj.write(data)
