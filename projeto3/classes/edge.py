class Edge :
    def __init__(self, src, tgt, variable):
        self.src = src
        self.tgt = tgt
        self.variable = variable

    def printcu(self):
        return "{} -> {} -> {}".format(self.src.name, self.variable, self.tgt.name)
