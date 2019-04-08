from classes.graph import Graph
from classes.node import Node
from classes.edge import Edge
from classes.stack import Stack
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

count = 1
EMPTY_STATE = 'ε'


def convert(exp):
    s = Stack(len(exp))
    posfixa = ''

    for c in exp:
        if ('A' <= c <= 'Z') or ('a' <= c <= 'z'):
            posfixa += c

        if c == '+' or c == '.' or c == '*' or c == '|':
            pr = priority(c)

            while (not s.empty()) and (priority(s.top()) >= pr):
                posfixa += s.pop()

            s.push(c)

        if c == '(':
            s.push(c)

        if c == ')':
            x = s.pop()

            while x != '(':
                posfixa += x
                x = s.pop()

    while not s.empty():
        x = s.pop()
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
            s.push(x)
        else:
            if c == '+':
                x = s.pop()
                s.push(get_plus(x))
            elif c == '.':
                y = s.pop()
                x = s.pop()
                s.push(get_point(x, y))
            elif c == '*':
                x = s.pop()
                s.push(get_cline(x))
            elif c == '|':
                y = s.pop()
                x = s.pop()
                s.push(get_or(x, y))

    return x


def get_initial_final(graph):
    global count

    initial = graph.get_initial()
    initial.category = 'incremental'

    final = graph.get_final()
    final.category = 'incremental'

    node_initial = Node(count, 'initial')
    count += 1
    node_initial.add_edge(Edge(node_initial, initial, EMPTY_STATE))
    node_final = Node(count, 'final')
    count += 1
    final.add_edge(Edge(final, node_final, EMPTY_STATE))

    graph.add_node(node_initial)
    graph.add_node(node_final)

    return graph


def plot(graph, title='figura1'):
    g = nx.DiGraph()
    edge_labels = dict()
    color_map = []

    for n in graph.nodes:
        if n.category == 'initial':
            color_map.append('g')
        elif n.category == 'final':
            color_map.append('r')
        else:
            color_map.append('b')
        g.add_node(n.name)

    for n in graph.nodes:
        for e in n.edges:
            g.add_edge(e.src.name, e.tgt.name)
            edge_labels[(e.src.name, e.tgt.name)] = e.variable

    pos = nx.shell_layout(g)
    nx.draw(g, pos, with_labels=True, arrows=True, arrowsize=5, node_color=color_map, node_size=400, font_size=10)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    green = mpatches.Patch(color='g', label='Initial State')
    red = mpatches.Patch(color='r', label='Final State')
    blue = mpatches.Patch(color='b', label='Incremental')
    plt.legend(handles=[green, red, blue])
    plt.title(title)
    plt.show()


def get_plus(x):
    node_xinitial = x.get_initial()
    node_xfinal = x.get_final()

    node_xfinal.add_edge(Edge(node_xfinal, node_xinitial, EMPTY_STATE))

    return get_initial_final(x)


def get_point(x, y):
    node_xfinal = x.get_final()
    node_yinitial = y.get_initial()

    node_xfinal.category = 'incremental'
    node_xfinal.add_edge(Edge(node_xfinal, node_yinitial, EMPTY_STATE))
    node_yinitial.category = 'incremental'

    for yn in y.nodes:
        x.add_node(yn)

    return get_initial_final(x)


def get_cline(x):
    global count
    node_xinitial = x.get_initial()
    node_xinitial.category = 'incremental'
    node_xfinal = x.get_final()
    node_xfinal.category = 'incremental'

    node_xfinal.add_edge(Edge(node_xfinal, node_xinitial, EMPTY_STATE))

    node_initial = Node(count, 'initial')
    count += 1
    node_final = Node(count, 'final')
    count += 1

    node_initial.add_edge(Edge(node_initial, node_xinitial, EMPTY_STATE))
    node_initial.add_edge(Edge(node_initial, node_final, EMPTY_STATE))
    node_xfinal.add_edge(Edge(node_xfinal, node_final, EMPTY_STATE))

    x.add_node(node_initial)
    x.add_node(node_final)

    return x


def get_or(x, y):
    global count
    node_xinitial = x.get_initial()
    node_xfinal = x.get_final()

    node_yinitial = y.get_initial()
    node_yfinal = y.get_final()

    node_xinitial.category = 'incremental'
    node_xfinal.category = 'incremental'
    node_yinitial.category = 'incremental'
    node_yfinal.category = 'incremental'

    for y in y.nodes:
        x.add_node(y)

    node_initial = Node(count, 'initial')
    count += 1
    node_final = Node(count, 'final')
    count += 1

    node_initial.add_edge(Edge(node_initial, node_xinitial, EMPTY_STATE))
    node_initial.add_edge(Edge(node_initial, node_yinitial, EMPTY_STATE))

    node_xfinal.add_edge(Edge(node_xfinal, node_final, EMPTY_STATE))
    node_yfinal.add_edge(Edge(node_yfinal, node_final, EMPTY_STATE))

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

    node1.add_edge(Edge(node1, node2, letter))

    graph.add_node(node1)
    graph.add_node(node2)

    return get_initial_final(graph)


def get_copy_graph(graph):
    copy = Graph()

    for n in graph.nodes:
        node = Node(n.name, n.category)
        copy.add_node(node)


def print_graph(graph, name):
    print('--- {} ---'.format(name))

    for n in graph.nodes:
        for e in n.edges:
            print("{}({}) -> {} -> {}({})".format(e.src.name, e.src.category, e.variable, e.tgt.name, e.tgt.category))
    print('')
