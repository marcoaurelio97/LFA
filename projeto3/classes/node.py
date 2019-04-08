class Node:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.edges = []
        self.visited = False
    
    def add_edge(self, edge):
        self.edges.append(edge)
