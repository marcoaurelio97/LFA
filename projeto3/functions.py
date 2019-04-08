from classes.graph import Graph
from classes.node import Node
from classes.edge import Edge
from classes.stack import Stack
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

count = 1


def convert(exp):
    s = Stack(len(exp))
    posfixa = ''

    for c in exp:
        if ('A' <= c <= 'Z') or ('a' <= c <= 'z'):
            posfixa += c

        if c == '+' or c == '.' or c == '*' or c == '|':
            pr = priority(c)

            while (not s.Empty()) and (priority(s.Top()) >= pr):
                posfixa += s.Pop()

            s.Push(c)

        if c == '(':
            s.Push(c)

        if c == ')':
            x = s.Pop()

            while x != '(':
                posfixa += x
                x = s.Pop()

    while not s.Empty():
        x = s.Pop()
        posfixa += x

    return posfixa


def priority(op):
    if op == '(':
        return 1
    elif op == '.' or op == '|':
        return 2
    elif op == '*' or op == '+':
        return 3
    return 0


def calculate(posfixa):
    x = Graph()
    s = Stack(len(posfixa))

    for c in posfixa:
        if ('A' <= c <= 'Z') or ('a' <= c <= 'z'):
            x = get_graph_letter(c)
            s.Push(x)
        else:
            if c == '+':
                x = s.Pop()
                s.Push(get_plus(x))
            elif c == '.':
                y = s.Pop()
                x = s.Pop()
                s.Push(get_point(x, y))
            elif c == '*':
                x = s.Pop()
                s.Push(get_cline(x))
            elif c == '|':
                y = s.Pop()
                x = s.Pop()
                s.Push(get_or(x, y))

    return x


def get_initial_final(graph):
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
    final.addEdge(Edge(final, node_final, 'ε'))

    graph.add_node(node_initial)
    graph.add_node(node_final)

    return graph


def plot(graph, title='figura1'):
    g = nx.DiGraph()
    edge_labels = dict()
    color_map = []

    for n in graph.getNodes():
        if n.category == 'initial':
            color_map.append('g')
        elif n.category == 'final':
            color_map.append('r')
        else:
            color_map.append('b')
        g.add_node(n.name)

    for n in graph.getNodes():
        for e in n.getEdges():
            g.add_edge(e.src.name, e.tgt.name)
            edge_labels[(e.src.name, e.tgt.name)] = e.variable

    pos = nx.shell_layout(g)
    nx.draw(g, pos, with_labels=True, arrows=True, arrowsize=5, node_color=color_map, node_size=400, font_size=10)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    blue = mpatches.Patch(color='g', label='Initial State')
    red = mpatches.Patch(color='r', label='Final State')
    plt.legend(handles=[blue, red])
    plt.title(title)
    plt.show()


def get_plus(x):
    node_xinitial = x.getInitial()
    node_xfinal = x.getFinal()

    node_xfinal.addEdge(Edge(node_xfinal, node_xinitial, 'ε'))

    return get_initial_final(x)


def get_point(x, y):
    node_xfinal = x.getFinal()
    node_yinitial = y.getInitial()

    node_xfinal.category = 'incremental'
    node_xfinal.addEdge(Edge(node_xfinal, node_yinitial, 'ε'))
    node_yinitial.category = 'incremental'

    for yn in y.getNodes():
        x.add_node(yn)

    return get_initial_final(x)


def get_cline(x):
    global count
    node_xinitial = x.getInitial()
    node_xinitial.category = 'incremental'
    node_xfinal = x.getFinal()
    node_xfinal.category = 'incremental'

    node_xfinal.addEdge(Edge(node_xfinal, node_xinitial, 'ε'))

    node_initial = Node(count, 'initial')
    count += 1
    node_final = Node(count, 'final')
    count += 1

    node_initial.addEdge(Edge(node_initial, node_xinitial, 'ε'))
    node_initial.addEdge(Edge(node_initial, node_final, 'ε'))
    node_xfinal.addEdge(Edge(node_xfinal, node_final, 'ε'))

    x.add_node(node_initial)
    x.add_node(node_final)

    return x


def get_or(x, y):
    global count
    node_xinitial = x.getInitial()
    node_xfinal = x.getFinal()

    node_yinitial = y.getInitial()
    node_yfinal = y.getFinal()

    node_xinitial.category = 'incremental'
    node_xfinal.category = 'incremental'
    node_yinitial.category = 'incremental'
    node_yfinal.category = 'incremental'

    for y in y.getNodes():
        x.add_node(y)

    node_initial = Node(count, 'initial')
    count += 1
    node_final = Node(count, 'final')
    count += 1

    node_initial.addEdge(Edge(node_initial, node_xinitial, 'ε'))
    node_initial.addEdge(Edge(node_initial, node_yinitial, 'ε'))

    node_xfinal.addEdge(Edge(node_xfinal, node_final, 'ε'))
    node_yfinal.addEdge(Edge(node_yfinal, node_final, 'ε'))

    x.add_node(node_initial)
    x.add_node(node_final)

    return x


def get_graph_letter(letter):
    global count
    graph = Graph()

    node1 = Node(count, 'initial')
    count += 1
    node2 = Node(count, 'final')
    count += 1

    node1.addEdge(Edge(node1, node2, letter))

    graph.add_node(node1)
    graph.add_node(node2)

    return get_initial_final(graph)


def get_copy_graph(graph):
    copy = Graph()

    for n in graph.getNodes():
        node = Node(n.name, n.category)
        copy.add_node(node)


def print_graph(graph, name):
    print('--- {} ---'.format(name))

    for n in graph.getNodes():
        for e in n.getEdges():
            print("{}({}) -> {} -> {}({})".format(e.src.name, e.src.category, e.variable, e.tgt.name, e.tgt.category))
    print('')
