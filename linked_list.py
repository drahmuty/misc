class Node():
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList():
    def __init__(self):
        self.head = None
        
    def array(self):
        arr = []
        c = self.head
        while c:
            out.append(c.value)
            c = c.next
        print(arr)
            
    def search(self, value):
        c = self.head
        while c:
            if c.value == value:
                return True
            c = c.next
        return False            

    def insert(self, value):
        temp = self.head
        self.head = Node(value)
        self.head.next = temp
    
    def delete(self, value):
        prev = None
        c = self.head
        while c:
            if c.value == value:
                if prev == None:
                    self.head = c.next
                else:
                    prev.next = c.next
                return
            prev = c
            c = c.next
