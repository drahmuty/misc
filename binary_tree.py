# Binary tree node class
class TreeNode():
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree():
    def __init__(self):
        self.root = None

    def search(self, value):
        c = self.root
        while c:
            if value == c.value:
                return True
            elif value < c.value:
                c = c.left
            else:
                c = c.right
        return False
    
    def insert(self, value):
        c = self.root
        while c:
            if value == c.value:
                return
            elif value < c.value:
                if c.left:
                    c = c.left
                else:
                    c.left = TreeNode(value)
                    return
            else:
                if c.right:
                    c = c.right
                else:
                    c.right = TreeNode(value)
                    return
        self.root = TreeNode(value)
    
    def show(self):
        c = self.root
        while c:
            c.left.show()
            print(c.value)
            c.right.show()
