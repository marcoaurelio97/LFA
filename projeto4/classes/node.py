class Node:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.edges = []
        self.visited = False
    
    def add_edge(self, edge):
        self.edges.append(edge)

    def verify_letter_exists(self, letter):
        for e in self.edges:
            if e.variable == letter:
                return e.tgt
        return False
