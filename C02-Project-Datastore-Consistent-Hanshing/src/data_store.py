import random


from InfoGenerator import InfoGenerator
from User import UserInfo, UserData
from Node import Node

TOTAL_VIRTUAL_NODES = 200
DEFAULT_NUM_NODES = 4
INITIAL_NUM_KEYS = 10000
RANDOM_STRING_LENGTH = 8
PASSWORD_LENGTH = 32


# Client Context
node_names = []
node_dict = {}

with open('initial_config.txt', 'w') as f:
    print('###############  INITIAL CONFIGURATION ###############\n', file=f)
    print(f'Total Virtual Nodes     : {TOTAL_VIRTUAL_NODES}', file=f)
    print(f'Number of Physical Nodes: {DEFAULT_NUM_NODES}\n', file=f)
    print('Problem 1) Demonstration of implementation of population map', file=f)
    print('           Each Physical Node to have equal distribution of virtual nodes...', file=f)

# Generates random node names for the initial default nodes
node_names = [InfoGenerator.generate_node_name(RANDOM_STRING_LENGTH) for i in range(DEFAULT_NUM_NODES)]

# Creates the first node and initializes the vnode mapping
# Also keeps a copy of the vnode map instance in the client for later use
first_name = node_names[0]
first_node = Node(first_name, TOTAL_VIRTUAL_NODES)
node_dict[first_name] = first_node
first_node.initialize_vnode_map(node_names)
vnode_map = first_node.clone_vnode_map()

with open('initial_config.txt', 'a') as f:
    print('Vnode To Physical Node Mapping:', file=f)
    vnode_map.print_map(f);

with open('initial_config.txt', 'a') as f:
    print('\nVnode To Physical Node Distribution:', file=f)
    vnode_map.print_dist(f);

# Creates other nodes, intializing them with the same vnode mapping
# Also updates the complete node mapping in all nodes
for i in range(1, len(node_names)):
    node_dict[node_names[i]] = Node(node_names[i], TOTAL_VIRTUAL_NODES, first_node.clone_vnode_map())

for name in node_names:
    node_dict[name].populate_nodes(node_dict)

with open('ds_operation.txt', 'w') as f:
    print('###############  INITIAL CONFIGURATION ###############\n', file=f)
    print(f'Total Virtual Nodes     : {TOTAL_VIRTUAL_NODES}', file=f)
    print(f'Number of Physical Nodes: {DEFAULT_NUM_NODES}', file=f)
    print(f'Number of Key Insertions: {INITIAL_NUM_KEYS}\n', file=f)
    print('Problem 2)a Demonstration of implementation of get_data in masterless architecture', file=f)
    print(f'           Initially all stores are empty', file=f)
    print(f'           After set_data is done key stores are distributed across the different Physical nodes', file=f)
    print(f'           Then First Node is selected as orchestrator and get_data operations are carried out for few random keys', file=f)
    print('Problem 2)b Demonstration of implementation of set_data in masterless architecture', file=f)
    print(f'           First Node is selected as orchestrator and set_data operations are carried out for all the {INITIAL_NUM_KEYS} keys', file=f)
    print(f'           The keys should get distributed across the different Physical nodes\n', file=f)

# List node names and key counts
with open('ds_operation.txt', 'a') as f:
    print(f'Key Count Before Insertion', file=f)
    for node in node_dict.values():
        print(node, file=f)
    print('\n\n', file=f)

# Populates the distributed data store
for i in range(INITIAL_NUM_KEYS):
    user_info = UserInfo(InfoGenerator.generate_user_id(),
                             UserData(InfoGenerator.generate_email(RANDOM_STRING_LENGTH),
                                        InfoGenerator.generate_password(PASSWORD_LENGTH)))
    node_dict[first_name].set_data(user_info.user_id, user_info.user_data)

# List node names and key counts
with open('ds_operation.txt', 'a') as f:
    print(f'Key Count After Insertion', file=f)
    for node in node_dict.values():
        print(node, file=f)
    print('\n\n', file=f)

# List random keys by calling any node
with open('ds_operation.txt', 'a') as f:
    print('Random pickup of various keys(10) on any node(first_node)', file=f)
    for i in range(10):
        user_id = random.randint(0, INITIAL_NUM_KEYS - 1)
        print(first_node.get_data(user_id), file=f)
    print('\n\n', file=f)

# Add a new node to the Data Store
with open('node_operation.txt', 'w') as f:
    print('###############  INITIAL CONFIGURATION ###############\n', file=f)
    print(f'Total Virtual Nodes     : {TOTAL_VIRTUAL_NODES}', file=f)
    print(f'Number of Physical Nodes: {DEFAULT_NUM_NODES}', file=f)
    print(f'Number of Key Insertions: {INITIAL_NUM_KEYS}\n', file=f)
    print('Problem 3)  Demonstration of implementation of add_new_node in masterless architecture', file=f)
    print(f'           Initially all {INITIAL_NUM_KEYS} keys are present in {DEFAULT_NUM_NODES} of Physical Nodes', file=f)
    print(f'           After add_new_data is done keys from every Virtual Node mapped to Physical Node are transferred ', file=f)
    print(f'           The keys should get distributed across the different Physical nodes without any data loss or duplication', file=f)
    print('Problem 4)  Demonstration of implementation of remove_node in masterless architecture', file=f)
    print(f'           Initially all {INITIAL_NUM_KEYS} keys are present in {DEFAULT_NUM_NODES} + 1 of Physical Nodes', file=f)
    print(f'           After remove_node is done keys from every Virtual Node mapped to the Removed Physical Node are transferred to all the other Node uniformly', file=f)
    print(f'           The above operations should not corrupt the datastore. Get/Set should continue to work as before the node add/del \n', file=f)
    print('###############  ADDING A NODE ###############\n', file=f)

# List node names and key counts
with open('node_operation.txt', 'a') as f:
    print(f'Key Count Before Node Insertion', file=f)
    for node in node_dict.values():
        print(node, file=f)
    print('\n\n', file=f)

new_node_name = InfoGenerator.generate_node_name(RANDOM_STRING_LENGTH)
node_names.append(new_node_name)

# New node creation similar to the other existing nodes
new_node = Node(new_node_name, TOTAL_VIRTUAL_NODES, first_node.clone_vnode_map())
node_dict[new_node_name] = new_node
new_node.populate_nodes(node_dict)

# Updates node mapping of other nodes to add this new node
for node_name, node in node_dict.items():
    if node_name == new_node_name:
        continue
    node.add_new_node(new_node_name, new_node)

# List node names and key counts
with open('node_operation.txt', 'a') as f:
    print(f'Key Count After Node Insertion', file=f)
    for node in node_dict.values():
        print(node, file=f)
    print('\n\n', file=f)

# List random keys by calling any node
with open('node_operation.txt', 'a') as f:
    print('Random pickup of various keys(10) on any node(first_node)', file=f)
    for i in range(10):
        user_id = random.randint(0, INITIAL_NUM_KEYS - 1)
        print(first_node.get_data(user_id), file=f)
    print('\n\n', file=f)

# Planned removal of a node from Data Store and reassignment of its vnodes
with open('node_operation.txt', 'a') as f:
    print('###############  REMOVING A NODE ###############\n', file=f)

# Remove any random node
# remove_current_node is only called on the to-be removed node
random.shuffle(node_names)
del_node_name = node_names.pop(0)
del_node = node_dict.pop(del_node_name, 'key not found')
del_node.remove_current_node(node_dict)

# List node names and key counts
with open('node_operation.txt', 'a') as f:
    print(f'Key Count After Random Node Removal', file=f)
    for node in node_dict.values():
        print(node, file=f)
    print('\n\n', file=f)

# Pick any node from the remaining ones
node_iter = iter(node_dict.values())
any_node = next(node_iter)
any_other_node = next(node_iter)


# List random keys by calling any node
with open('node_operation.txt', 'a') as f:
    print('Random pickup of various keys(10) on any node(Random)', file=f)
    for i in range(10):
        user_id = random.randint(0, INITIAL_NUM_KEYS - 1)
        print(any_node.get_data(user_id), file=f)
    print('\n\n', file=f)

# Test read/write on a new key
with open('node_operation.txt', 'a') as f:
    print('###############  READ/WRITE TEST AFTER NODE ADD/DEL  ###############\n', file=f)

user_info = UserInfo(InfoGenerator.generate_user_id(),
                             UserData(InfoGenerator.generate_email(RANDOM_STRING_LENGTH),
                                        InfoGenerator.generate_password(PASSWORD_LENGTH)))

with open('node_operation.txt', 'a') as f:
    print(f'Generated user data: {user_info.user_data}', file=f)

any_node.set_data(user_info.user_id, user_info.user_data)
fetched_user_data = any_other_node.get_data(user_info.user_id)

with open('node_operation.txt', 'a') as f:
    print(f'Fetched user data: {fetched_user_data}', file=f)
