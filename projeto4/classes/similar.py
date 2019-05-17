class Similar:
    def __init__(self, name1, name2):
        self.name1 = name1
        self.name2 = name2
        self.marked = False
        self.dependencies = []
