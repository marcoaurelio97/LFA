class Node :
    def __init__(self, name, category) :
        self.name = name
        self.category = category
        self.edges = []
    
    def addEdge(self, edge) :
        self.edges.append(edge)
    
    def getEdges(self) :
        return self.edges
    
    def getName(self) :
        return self.name