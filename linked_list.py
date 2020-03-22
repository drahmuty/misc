class Node():
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList():
    def __init__(self):
        self.head = None
            
    def search(self, value):
        c = self.head
        while c:
            if c.value == value:
                return True
            c = c.next
        return False            

    def insert(self, value):
        if self.search(value):      # option to prevent duplicate entries 
            return
        temp = self.head
        self.head = Node(value)
        self.head.next = temp
    
    def delete(self, value):
        prev = None
        c = self.head
        while c:
            if c.value == value:
                if prev:
                    prev.next = c.next
                else:
                    self.head = c.next
                return
            prev = c
            c = c.next

    def show(self):
        c = self.head
        while c:
            print(c.value)
            c = c.next
        
    def array(self):
        arr = []
        c = self.head
        while c:
            arr.append(c.value)
            c = c.next
        print(arr)
