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
      
    def tree_depth(self):
        if self.left:
            l = self.left.tree_depth()
        else:
            l = 0
        if self.right:
            r = self.right.tree_depth()
        else:
            r = 0
        if l > r:
            return l + 1
        else:
            return r + 1



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

    def min(self):
        if not self.left:
            return self
        return self.left.min()

    def max(self):
        if not self.right:
            return self
        return self.right.max()
    
    def delete(self, value):
        if not self:
            return self
        if value < self.value:
            self.left = self.left.delete(value)
        elif value > self.value:
            self.right = self.right.delete(value)
        else:
            if not self.left:
                temp = self.right
                self = None
                return temp
            elif not self.right:
                temp = self.left
                self = None
                return temp
            temp = self.right.min()
            self.value = temp.value
            self.parent = temp.parent
            self.right = self.right.delete(temp.value)
        return self

            

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
        self.root.delete(value)

    def show(self):
        if self.root:
            self.root.show()

    def min(self):
       return self.root.min()

    def max(self):
        return self.root.max()

    def tree_depth(self):
        return self.root.tree_depth()
    
    def show_depth(self):
        i = 0
        j = self.tree_depth()
        while i < j:
            self.root.print_depth(i)
            i += 1
