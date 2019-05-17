class Similar:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.marked = False
        self.dependencies = []
