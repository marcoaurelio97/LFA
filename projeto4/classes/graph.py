class Graph:
    def __init__(self):
        self.nodes = []
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def get_initial(self):
        for n in self.nodes:
            if n.category == 'initial':
                return n

    def get_final(self):
        for n in self.nodes:
            if n.category == 'final':
                return n

    def get_node_by_name(self, name):
        for n in self.nodes:
            if name == n.name:
                return n

    def verify_exist(self, name):
        for n in self.nodes:
            if name == n.name:
                return True
        return False

    def clear_visited(self):
        for n in self.nodes:
            n.visited = False
