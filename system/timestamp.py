#Simple key-value store with support for basic timestamping based transactions
class DataStore:

    # Initial data can be provided while creating the store
    # It'll automatically set the read and write timestamps of each key to 0
    # Timestamps are constantly increasing counters
    # Transaction counter is stored so that each transaction can be assigned a unique id
    def __init__(self, kv_dict):
        self._kv_dict = kv_dict
        self._data_timestamps = {}
        for key in self._kv_dict:
            self._data_timestamps[key] = {'read_ts': 0, 'write_ts': 0}
            
        self._transaction_counter = 0

    def __str__(self):
        return f'Data: {self._kv_dict}\nData Timestamps: {self._data_timestamps}'
    
    
    def get_data_read_ts(self, key):
        return self._data_timestamps[key]['read_ts']

    def get_data_write_ts(self, key):
        return self._data_timestamps[key]['write_ts']

    def set_data_read_ts(self, key, timestamp):
        self._data_timestamps[key]['read_ts'] = timestamp
            
    def set_data_write_ts(self, key, timestamp):
        self._data_timestamps[key]['write_ts'] = timestamp

    # Creates a new transaction with a unique and always increasing id
    def init_transaction(self, name):
        self._transaction_counter += 1
        transaction = Transaction(self._transaction_counter, self, name)
        return transaction
    
    # Read will update the read timestamp if the transaction reading it has a higher timestamp than the current value
    def get_data(self, key, timestamp):
        if (timestamp > self.get_data_read_ts(key)):
            self.set_data_read_ts(key, timestamp)
        
        return self._kv_dict.get(key)

    # Write will update the write timestamp if the transaction reading it has a higher timestamp than the current value
    def set_data(self, key, value, timestamp):
        if (timestamp > self.get_data_write_ts(key)):
            self.set_data_write_ts(key, timestamp)
        
        self._kv_dict[key] = value
        
    


class Transaction:

    # Transaction object will store a unique timestamp based on when it started
    # It'll also store a link to the datastore to issue read and write commands
    # And a name just to make it easy for us to map the print statements to specific transactions
    def __init__(self, timestamp, datastore, name):
        self._timestamp = timestamp
        self._datastore = datastore
        self._name = name
    
    def __str__(self):
        return f'Transaction {self._name} has timestamp {self._timestamp}'
    
    # As per the algorithm, a read is not allowed if the transaction's timestamp is less than the key's write timestamp
    # If it is, the transaction should be rolled back and aborted
    def get_data(self, key):
        if (self._timestamp < self._datastore.get_data_write_ts(key)):
            print(f'Read conflict in transaction {self._name} with timestamp {self._timestamp} for key {key}')
            self.abort()
        else:
            return self._datastore.get_data(key, self._timestamp)

    # As per the algorithm, a write is not allowed if the transaction's timestamp is less than any of the key's read and write timestamps
    # If it is, the transaction should be rolled back and aborted
    def set_data(self, key, value):
        if ((self._timestamp < self._datastore.get_data_read_ts(key)) or (self._timestamp < self._datastore.get_data_write_ts(key))):
            print(f'Write conflict in transaction {self._name} with timestamp {self._timestamp} for key {key}')
        else:
            self._datastore.set_data(key, value, self._timestamp)
        
    def commit(self):
        # Placholder for logic for committing the changed values
        pass
        
    def abort(self):
        # Placholder for logic for rolling back already made changes and aborting
        pass


# Initial setup where we create three data points and two transactions
print('Initial Data\n')
initial_dataset = {'x': 5, 'y': 6, 'z': 7}
data_store = DataStore(initial_dataset)
print(data_store)
tx_1 = data_store.init_transaction('tx_1')
tx_2 = data_store.init_transaction('tx_2')
print(tx_1)
print(tx_2)

# tx_1 reads and writes key 'y' before tx_2 reads or writes the same. There is no potential conflict.
# This can be made equivalent to the case where tx_1 completes and tx_2 starts afterwards
print('\n\nNormal run\n')
tx_1.get_data('x')
tx_1.set_data('x', 10)
tx_1.get_data('y')
tx_1.set_data('y', 11)

tx_2.get_data('y')
tx_2.set_data('y', 20)
tx_2.get_data('z')
tx_2.set_data('z', 21)
print(data_store)
print('------------------------------\n')

# Recreating the store and transactions for the next run from the start
print('Data Reset\n')
initial_dataset = {'x': 5, 'y': 6, 'z': 7}
data_store = DataStore(initial_dataset)
print(data_store)
tx_1 = data_store.init_transaction('tx_1')
tx_2 = data_store.init_transaction('tx_2')

# Here tx_2 has written 'y' before a read attempt from tx_1
# This is not allowed as tx_1 is an older transaction and hence should have read 'y' before tx_2 wrote to it
print('\n\nRead conflict run\n')
tx_1.get_data('x')
tx_1.set_data('x', 10)
tx_2.get_data('y')
tx_2.set_data('y', 20)
tx_1.get_data('y')
print(data_store)
print('------------------------------\n')

# Recreating the store and transactions for the next run from the start
print('Data Reset\n')
initial_dataset = {'x': 5, 'y': 6, 'z': 7}
data_store = DataStore(initial_dataset)
print(data_store)
tx_1 = data_store.init_transaction('tx_1')
tx_2 = data_store.init_transaction('tx_2')

# Here tx_2 has read and written 'y' before tx_1 can write to it
# Even though tx_1 has read 'y' before tx_2, it can't write to it after tx_2 as it's the older transaction
print('\n\nWrite conflict run - 1\n')
tx_1.get_data('x')
tx_1.set_data('x', 10)
tx_1.get_data('y')
tx_2.get_data('y')
tx_2.set_data('y', 20)
tx_1.set_data('y', 10)
print(data_store)
print('------------------------------\n')

# Recreating the store and transactions for the next run from the start
print('Data Reset\n')
initial_dataset = {'x': 5, 'y': 6, 'z': 7}
data_store = DataStore(initial_dataset)
print(data_store)
tx_1 = data_store.init_transaction('tx_1')
tx_2 = data_store.init_transaction('tx_2')

# Here tx_2 has just read 'y' before tx_1 can write to it
# tx_1 still can't write 'y' since tx_2 (a newer transaction) has already read it
print('\n\nWrite conflict run - 2\n')
tx_1.get_data('x')
tx_1.set_data('x', 10)
tx_1.get_data('y')
tx_2.get_data('y')
tx_1.set_data('y', 10)
print(data_store)
print('------------------------------\n')

