class Graph :
    def __init__(self) :
        self.nodes = []
    
    def add_node(self, node) :
        self.nodes.append(node)
    
    def getNodes(self) :
        return self.nodes
    
    def getInitial(self) :
        for n in self.nodes :
            if n.category == 'initial':
                return n

    def getFinal(self) :
        for n in self.nodes :
            if n.category == 'final':
                return n

    def get_node_by_name(self, name):
        for n in self.nodes:
            if name == n.name:
                return n
