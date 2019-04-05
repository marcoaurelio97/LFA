class Node :
    def __init__(self, parent, rule, word) :
        self.parent = parent
        self.rule = rule

        if (rule[0] in word) :
            self.word = word.replace(rule[0], rule[1], 1)
        else :
            self.word = -1