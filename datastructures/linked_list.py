# !/usr/bin/env python3.7
# -*- coding: UTF-8 -*-

class Node:
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return f"{self.item}"


class SllNode(Node):
    def __init__(self, item):
        super().__init__(item)
        self.next = None


class DllNode(Node):
    def __init__(self, item):
        super().__init__(item)
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.first = None

    def insert_at_first(self, node):
        pass

    def insert_at_last(self, node):
        pass

    def insert_at_position(self, pos, node):
        pass

    def length(self):
        count = 0
        iterator = self.first
        while iterator is not None:
            count += 1
            iterator = iterator.next
        return count

    def __str__(self):
        iterator = self.first
        string = None
        if iterator is not None:
            string = str(iterator)
            iterator = iterator.next

        while iterator is not None:
            string += "->"
            string += str(iterator)
            iterator = iterator.next

        return string


class SinglyLinkedList(LinkedList):
    def __init__(self):
        super().__init__()

    def insert_at_first(self, item):
        node = SllNode(item)
        temp = self.first
        self.first = node
        node.next = temp

    def __str__(self):
        return "SLL(" + super().__str__() + ")"


class DoublyLinkedList(LinkedList):
    def __init__(self):
        super().__init__()

    def insert_at_first(self, item):
        node = DllNode(item)
        temp = self.first
        self.first = node
        node.next = temp

    def __str__(self):
        return "DLL(" + super().__str__() + ")"


# Client Code
if __name__ == '__main__':
    sll_1 = SinglyLinkedList()
    sll_1.insert_at_first(1)
    sll_1.insert_at_first(2)
    print(sll_1)
    dll_1 = DoublyLinkedList()
    dll_1.insert_at_first(1)
    dll_1.insert_at_first(2)
    print(dll_1)
