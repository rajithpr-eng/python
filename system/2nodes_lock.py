#Simple key-value store with multiple replicas storing the same data
#Store also has a list of all replicas and a lock store for each key in the main store
class DataStore:
    def __init__(self, kv_dict):
        self._kv_dict = kv_dict
        self._replica_list = []
        self._lock_dict = {}

    @property
    def kv_dict(self):
        return self._kv_dict

    @property
    def replica_list(self):
        return self._replica_list

    @property
    def lock_dict(self):
        return self._lock_dict

    # Add replicas based on addition of new nodes
    def add_replicas(self, replica_list):
        self._replica_list.extend(replica_list)

    # A very simple example of a lock on all replicas of the same key
    # Doesn't handle concurrency or deadlocks
    # Exercise for the reader: Handle lock failures from replicas correctly and cleanup already taken locks
    def add_lock(self, key):
        if (self.lock_dict.get(key) and self.lock_dict.get(key) == 1):
            return -1

        self.lock_dict[key] = 1
        for replica in self._replica_list:
            replica.add_remote_lock(key)
        return 1

    def add_remote_lock(self, key):
        if (self.lock_dict.get(key) and self.lock_dict.get(key) == 1):
            return -1

        self.lock_dict[key] = 1
        return 1

    def remove_lock(self, key):
        self.lock_dict[key] = 0
        for replica in self._replica_list:
            replica.remove_remote_lock(key)

    def remove_remote_lock(self, key):
        self.lock_dict[key] = 0

    def get_data(self, key):
        return self.kv_dict.get(key)

    #Takes lock on all replicas, updates the value on local node and all replicase, and then releases locks
    def set_data(self, key, value):
        if self.add_lock(key) == -1:
            return -1

        self.kv_dict[key] = value
        for replica in self._replica_list:
            replica.set_remote_data(key, value)
        self.remove_lock(key)
        return 1

    def set_remote_data(self, key, value):
        self.kv_dict[key] = value

    #Simple add operation on a particular key's value
    def add(self, key, value):
        if self.get_data(key):
            result = self.set_data(key, self.get_data(key) + value)
        else:
            result = self.set_data(key, value)
        return result

    #Simple multiply operation on a particular key's value
    def multiply(self, key, value):
        if self.get_data(key):
            result = self.set_data(key, self.get_data(key) * value)
        else:
            result = self.set_data(key, 0)
        return result


#Client processing

#Setting up the stores
s1 = DataStore({})
s1.set_data('x', 5)
s2 = DataStore({})
s2.set_data('x', 5)
s1.add_replicas([s2])
s2.add_replicas([s1])

#In case of concurrent writes, the second one will not be able to lock the data to write to it
#It'll return failure. In normal cases, there is a wait mechanism on the lock, and failure after a wait timeout
add_result = s1.add('x', 2)
if add_result == -1:
    print('Failed to acquire locks, please retry')
mul_result = s2.multiply('x', 3)
if mul_result == -1:
    print('Failed to acquire locks, please retry')

s1_value = s1.get_data('x')
s2_value = s2.get_data('x')
#Everything would work fine in this case since all replicas receive the same update under lock
print(f'Correct Run: Value of x in s1 = {s1_value}, and in s2 = {s2_value}')
