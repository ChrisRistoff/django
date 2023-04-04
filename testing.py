# linked list database

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, data):
        node = Node(data)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def print(self):
        node = self.head
        while node is not None:
            print(node.data)
            node = node.next

    def delete(self, data):
        node = self.head
        if node.data == data:
            self.head = node.next
            return
        while node.next is not None:
            if node.next.data == data:
                node.next = node.next.next
                return
            node = node.next

    def search(self, data):

        node = self.head
        while node is not None:
            if node.data == data:
                return True
            node = node.next
        return False

    def reverse(self):
        node = self.head
        prev = None
        while node is not None:
            next = node.next
            node.next = prev
            prev = node
            node = next
        self.head = prev

    def reverse_recursive(self, node, prev):
        if node is None:
            self.head = prev
            return
        next = node.next
        node.next = prev
        self.reverse_recursive(next, node)

def main():
    linked_list = LinkedList()
    linked_list.add(1)
    linked_list.add(2)
    linked_list.add(3)
    linked_list.add(4)
    linked_list.add(5)
    linked_list.add(6)
    linked_list.add(7)
    linked_list.add(8)
    linked_list.add(9)
    linked_list.add(10)
    linked_list.print()
    print(linked_list.search(5))
    print(linked_list.search(11))
    linked_list.delete(5)
    linked_list.print()
    linked_list.reverse()
    linked_list.print()
    linked_list.reverse_recursive(linked_list.head, None)
    linked_list.print()
main()
