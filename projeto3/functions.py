from classes.graph import Graph
from classes.node import Node
from classes.edge import Edge
from classes.stack import Stack
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

count = 0

def convert(exp) :
    s = Stack(len(exp))
    posfixa = ''

    for c in exp :
        if ((c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z')) :
            posfixa += c
        
        if (c == '+' or c == '.' or c == '*' or c == '|') :
            pr = priority(c)

            while ((s.Empty() == False) and (priority(s.Top()) >= pr)) :
                posfixa += s.Pop()
            
            s.Push(c)
        
        if (c == '(') :
            s.Push(c)
        
        if (c == ')') :
            x = s.Pop()

            while (x != '(') :
                posfixa += x
                x = s.Pop()
    
    while (s.Empty() == False) :
        x = s.Pop()
        posfixa += x
    
    return posfixa

def priority(op) :
    if (op == '(') :
        return 1
    elif (op == '.' or op == '|') :
        return 2
    elif (op == '*' or op == '+') :
        return 3
    return 0

def calculate(posfixa) :
    x = Graph()
    s = Stack(len(posfixa))

    for c in posfixa :
        if ((c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z')) :
            x = getGraphLetter(c)
            s.Push(x)
        else :
            if (c == '+') :
                x = s.Pop()
                s.Push(getPlus(x))
            elif (c == '.') :
                y = s.Pop()
                x = s.Pop()
                s.Push(getPoint(x, y))
            elif (c == '*') :
                x = s.Pop()
                s.Push(getCline(x))
            elif (c == '|') :
                y = s.Pop()
                x = s.Pop()
                s.Push(getOr(x, y))

    return x
    
def getInitialFinal(graph) :
    global count

    initial = graph.getInitial()
    initial.category = 'incremental'

    final = graph.getFinal()
    final.category = 'incremental'

    node_initial = Node(count, 'initial')
    count += 1
    node_initial.addEdge(Edge(node_initial, initial, 'ε'))
    node_final = Node(count, 'final')
    count += 1
    node_final.addEdge(Edge(final, node_final, 'ε'))

    graph.addNode(node_initial)
    graph.addNode(node_final)

    return graph

def plot(graph) :
    g = nx.DiGraph()
    edge_labels = dict()
    color_map = []

    for n in graph.getNodes():
        if (n.category == 'initial') :
            color_map.append('g')
        elif (n.category == 'final') :
            color_map.append('r')
        else :
            color_map.append('b')
        g.add_node(n.name)
    
    for n in graph.getNodes() :
        for e in n.getEdges() :
            print("{} -> {} -> {}".format(e.src.name, e.variable, e.tgt.name))
            g.add_edge(e.src.name, e.tgt.name)
            edge_labels[(e.src.name, e.tgt.name)] = e.variable

    pos = nx.shell_layout(g)
    nx.draw(g, pos, with_labels=True, arrows=True, arrowsize=5, node_color=color_map, node_size=400, font_size=10)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    blue = mpatches.Patch(color='g', label='Initial State')
    red = mpatches.Patch(color='r', label='Final State')
    plt.legend(handles=[blue, red])
    plt.show()

def getPlus(x) :
    nodeXinitial = x.getInitial()
    nodeXfinal = x.getFinal()

    nodeXfinal.addEdge(Edge(nodeXfinal, nodeXinitial, 'ε'))
    
    return getInitialFinal(x)

def getPoint(x, y) :
    nodeXfinal = x.getFinal()
    nodeYinitial = y.getInitial()

    nodeXfinal.category = 'incremental'
    nodeXfinal.addEdge(Edge(nodeXfinal, nodeYinitial, 'ε'))
    nodeYinitial.category = 'incremental'

    for yn in y.getNodes() :
        x.addNode(yn)

    return getInitialFinal(x)

def getCline(x) :
    global count
    nodeXinitial = x.getInitial()
    nodeXinitial.category = 'incremental'
    nodeXfinal = x.getFinal()
    nodeXfinal.category = 'incremental'

    nodeXfinal.addEdge(Edge(nodeXfinal, nodeXinitial, 'ε'))

    node_initial = Node(count, 'initial')
    count += 1
    node_final = Node(count, 'final')
    count += 1

    node_initial.addEdge(Edge(node_initial, nodeXinitial, 'ε'))
    node_initial.addEdge(Edge(node_initial, node_final, 'ε'))
    nodeXfinal.addEdge(Edge(nodeXfinal, node_final, 'ε'))

    x.addNode(node_initial)
    x.addNode(node_final)

    return x

def getOr(x, y) :
    global count
    nodeXinitial = x.getInitial()
    nodeXfinal = x.getFinal()

    nodeYinitial = y.getInitial()
    nodeYfinal = y.getFinal()

    nodeXinitial.category = 'incremental'
    nodeXfinal.category = 'incremental'
    nodeYinitial.category = 'incremental'
    nodeYfinal.category = 'incremental'

    for y in y.getNodes() :
        x.addNode(y)

    node_initial = Node(count, 'initial')
    count += 1
    node_final = Node(count, 'final')
    count += 1

    node_initial.addEdge(Edge(node_initial, nodeXinitial, 'ε'))
    node_initial.addEdge(Edge(node_initial, nodeYinitial, 'ε'))

    nodeXfinal.addEdge(Edge(nodeXfinal, node_final, 'ε'))
    nodeYfinal.addEdge(Edge(nodeYfinal, node_final, 'ε'))

    x.addNode(node_initial)
    x.addNode(node_final)

    return x

def getGraphLetter(letter) :
    global count
    graph = Graph()

    node1 = Node(count, 'initial')
    count += 1
    node2 = Node(count, 'final')
    count += 1

    node1.addEdge(Edge(node1, node2, letter))

    graph.addNode(node1)
    graph.addNode(node2)

    return getInitialFinal(graph)

def getCopyGraph(graph) :
    copy = Graph()

    for n in graph.getNodes() :
        node = Node(n.name, n.category)
        copy.addNode(node)