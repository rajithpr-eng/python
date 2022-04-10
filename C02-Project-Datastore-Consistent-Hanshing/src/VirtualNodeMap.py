import random
import math

# Stores the vnode to node mapping
# Composed within a node so that every node has its own vnode mapping
class VirtualNodeMap:
    def __init__(self, node_names, TOTAL_VIRTUAL_NODES):
        self._vnode_map = {}
        self._node_names = node_names
        self._TOTAL_VIRTUAL_NODES = TOTAL_VIRTUAL_NODES

    @property
    def vnode_map(self):
        return self._vnode_map

    @property
    def node_names(self):
        return self._node_names

    # Populates the Virtual Node Nap, given the set of Node names.
    # Creates a mapping of Virtual Node to corresponding assigned physical Node
    def populate_map(self):

        # Problem statement 1
        # Generate a dict of vnode ids (0 to (TOTAL_VIRTUAL_NODES - 1) mapped randomly
        # but equally (as far as maths permits) to node names

        #Prepare a vnode_list
        vnode_list = [i for i in range(0, self._TOTAL_VIRTUAL_NODES)]

        #Randomize the elements in the list
        random.shuffle(vnode_list)

        #Assign vnode to node in round robin
        #The assigment would ensure all the vnodes are assigned equally
        #wherever possible
        cur = 0
        for vnode_id in vnode_list :
            self._vnode_map[vnode_id] = self._node_names[cur]
            cur += 1
            cur = cur % len(self._node_names)

    # Return the vnode name mapped to a particular vnode
    def get_node_for_vnode(self, vnode):
        return self._vnode_map[vnode]

    # Returns the vnode name where a particular key is stored
    # It finds the vnode for the key through modulo mapping, and then looks up the physical node
    def get_assigned_node(self, key):
        vnode = key % self._TOTAL_VIRTUAL_NODES
        return self._vnode_map[vnode]

    # Assign a new node name as mapping for a particular vnode
    # This is useful when vnodes are remapped during node addition or removal
    def set_new_assigned_node(self, vnode, new_node_name):
        self._vnode_map[vnode] = new_node_name

    def print_map(self, f):
       for each in self._vnode_map :
           print(each, ":", self._vnode_map[each], file=f)

    def print_dist(self, f):
       dist_dict = {}
       for each in self._vnode_map :
           dist_dict[self._vnode_map[each]] = dist_dict.setdefault(self._vnode_map[each], 0) + 1
       for each in dist_dict :
           print(each, ":", dist_dict[each], file=f)

    # Return the vnodes mapped to a particular named node
    def get_vnodes_for_node(self, name):
       lst = []
       for each in self._vnode_map :
           if (self._vnode_map[each] == name) :
               lst.append(each)
       return lst

    def get_assigned_vnode(self, key):
        vnode = key % self._TOTAL_VIRTUAL_NODES
        return vnode


