class Stack :
    def __init__(self, size) :
        self.size = size
        self.elements = []
    
    def Push(self, elem) :
        self.elements.append(elem)

    def Pop(self) :
        return self.elements.pop()

    def Full(self) :
        if self.size == len(self.elements) :
            return True
        return False
    
    def Empty(self) :
        if len(self.elements) == 0 :
            return True
        return False
    
    def Top(self) :
        return self.elements[len(self.elements) - 1]