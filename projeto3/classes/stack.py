class Stack:
    def __init__(self, size):
        self.size = size
        self.elements = []
    
    def push(self, elem):
        self.elements.append(elem)

    def pop(self):
        return self.elements.pop()

    def full(self):
        if self.size == len(self.elements):
            return True
        return False
    
    def empty(self):
        if len(self.elements) == 0:
            return True
        return False
    
    def top(self):
        return self.elements[len(self.elements) - 1]
