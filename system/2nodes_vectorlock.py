#Simple key-value store with multiple replicas storing the same data
class DataStore:
    def __init__(self, kv_dict, name):
        self._kv_dict = kv_dict
        self._name = name
        self._replica_list = []
        self._vector_clock = {name: 0}

    @property
    def kv_dict(self):
        return self._kv_dict

    @property
    def name(self):
        return self._name

    @property
    def vector_clock(self):
        return self._vector_clock

    #Add replicas based on addition of new nodes
    #This will also update the vector clock dict
    def add_replicas(self, replica_list):
        self._replica_list.extend(replica_list)
        for replica in replica_list:
            self._vector_clock[replica.name] = 0

    def reset_vector_clock(self):
        for replica in self._replica_list:
            self._vector_clock[replica.name] = 0
        self._vector_clock[self.name] = 0

    def get_data(self, key):
        return self.kv_dict.get(key)

    def set_data(self, key, value):
        self.kv_dict[key] = value
        self._vector_clock[self.name] += 1

    #Simple add operation on a particular key's value
    def add(self, key, value):
        if self.get_data(key):
            self.set_data(key, self.get_data(key) + value)
        else:
            self.set_data(key, value)

    #Simple multiply operation on a particular key's value
    def multiply(self, key, value):
        if self.get_data(key):
            self.set_data(key, self.get_data(key) * value)
        else:
            self.set_data(key, 0)

    #Event receiver from another replica to update value based on a change done on the caller
    #Normally, this would be called internally from the update on the other store
    def receive_event(self, key, value, caller_vector_clock):
        #compare clocks
        self_clock_ahead = True
        caller_clock_ahead = True
        for node in self.vector_clock:
            if (self.vector_clock[node] < caller_vector_clock[node]):
                self_clock_ahead = False

            if (caller_vector_clock[node] < self.vector_clock[node]):
                caller_clock_ahead = False

        if (self_clock_ahead == False and caller_clock_ahead == False):
            print(f'No clock is strictly coming later than others - CONCURRENT WRITES DETECTED for key {key} and values {value} and {self.get_data(key)} in receive_event of self.name')

        self.set_data(key, value)
        for replica in self._replica_list:
            self.vector_clock[replica.name] = max(self.vector_clock[replica.name], caller_vector_clock[replica.name])


# Client processing

# Setting up the stores
s1 = DataStore({}, 's1')
s1.set_data('x', 5)
s2 = DataStore({}, 's2')
s2.set_data('x', 5)
s1.add_replicas([s2])
s2.add_replicas([s1])
s1.reset_vector_clock()
s2.reset_vector_clock()




# Run without overlap
print(f'Initial: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s1.add('x', 2)
print(f'After add in s1: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s2.receive_event('x', s1.get_data('x'), s1.vector_clock)
print(f'After update in s2 for the add event: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s2.multiply('x', 3)
print(f'After multiply in s2: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s1.receive_event('x', s2.get_data('x'), s2.vector_clock)
print(f'After update in s1 for the multiply event: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s1_value = s1.get_data('x')
s2_value = s2.get_data('x')
# Everything would work fine in this case since all replicas received an update before a new write
print(f'Correct Run: Value of x in s1 = {s1_value}, and in s2 = {s2_value}\n')



# Resetting the value of 'x' key to 5 and resetting the clocks
s1.set_data('x', 5)
s2.set_data('x', 5)
s1.reset_vector_clock()
s2.reset_vector_clock()

# Run with overlap
print(f'Initial: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s1.add('x', 2)
print(f'After add in s1: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s2.multiply('x', 3)
print(f'After multiply in s2: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s2.receive_event('x', s1.get_data('x'), s1.vector_clock)
print(f'After update in s2 for the add event: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s1.receive_event('x', s2.get_data('x'), s2.vector_clock)
print(f'After update in s1 for the multiply event: s1 vector clock: {s1.vector_clock} and s2 vector clock: {s2.vector_clock}')
s1_value = s1.get_data('x')
s2_value = s2.get_data('x')
# One of the writes would be lost in this case as there are concurrent writes.
# However due to clash in vector clocks, the system can flag this to the application or take a predefined decision
# In this case, it chose to implement the write based on the first receiver event
# The final value would also depend on the order of events received after the concurrent writes
print(f'Incorrect Run: Value of x in s1 = {s1_value}, and in s2 = {s2_value}')
