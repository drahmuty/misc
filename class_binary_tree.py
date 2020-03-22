# Binary tree node class
class TreeNode():
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    def info(self):
        y = 'D: ' + str(self.depth()) + '\t'
        y += 'V: ' + str(self.value) + '\t'
        if self.parent:
            y += 'P: ' + str(self.parent.value) + '\t'
        else:
            y += 'ROOT\t'
        if self.left:
            y += 'L: ' + str(self.left.value) + '\t'
        else:
            y += 'L: None\t'
        if self.right:
            y += 'R: ' + str(self.right.value)
        else:
            y += 'R: None'
        print(y)

    def show(self):
        if self:
            if self.left:
                self.left.show()
            self.info()
            if self.right:
                self.right.show()

    def depth(self):
        d = 0
        p = self.parent
        while p:
            d += 1
            p = p.parent
        return d
    
    def print_depth(self, d):
        c = self
        if c:
            if c.depth() == d:
                c.info()
                return
            if c.left:
                c.left.print_depth(d)
            if c.right:
                c.right.print_depth(d)    
            

# Binary tree class
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
        p = None
        while c:
            if value == c.value:
                return
            elif value < c.value:
                p = c
                if c.left:
                    c = c.left
                else:
                    c.left = TreeNode(value, p)
                    return
            else:
                p = c
                if c.right:
                    c = c.right
                else:
                    c.right = TreeNode(value, p)
                    return
        self.root = TreeNode(value, p)

    def delete(self, value):
        prev = None
        c = self.root
        while c:
            if value == c.value:
                if c.left and not c.right:
                    return
            elif value < c.value:
                prev = c
                c = c.left
            else:
                prev = c
                c = c.right

    def show(self):
        if self.root:
            self.root.show()

    def min(self):
        c = self.root
        while c:
            if c.left:
                c = c.left
            else:
                return c

    def max(self):
        c = self.root
        while c:
            if c.right:
                c = c.right
            else:
                return c

    def tree_depth(self):
        mind = self.min().depth()
        maxd = self.max().depth()
        if mind > maxd:
            return mind
        else:
            return maxd
    
    def show_depth(self):
        i = 0
        j = self.tree_depth() + 1
        while i < j:
            self.root.print_depth(i)
            i += 1
        
