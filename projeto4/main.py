from classes.similar import Similar
from functions import *


def main():
    operators = ['(', ')', '+', '*', '|', '.']

    while True:
        # reg_exp = input("Digite a expressão regular: ")
        reg_exp = "a.b"

        if reg_exp == "":
            print("Digite uma expressão regular válida!")
            continue

        exp_invalida = False

        for c in reg_exp:
            if ('A' <= c <= 'Z') or ('a' <= c <= 'z'):
                continue
            else:
                if c not in operators:
                    exp_invalida = True

        if exp_invalida:
            print("Operador inválido!")
            continue

        break

    alphabet = get_alphabet(reg_exp)
    str_posfixa = convert(reg_exp)
    print("Posfixa: {}".format(str_posfixa))
    graph = calculate(str_posfixa)
    afd_graph = afe_to_afd(graph)
    minimize_afd(afd_graph, alphabet)


def get_alphabet(reg_exp):
    alphabet = []
    for c in reg_exp:
        if ('A' <= c <= 'Z') or ('a' <= c <= 'z'):
            alphabet.append(c)
    return alphabet


def afe_to_afd(graph):
    afd_graph = Graph()
    initial_node = Node(graph.get_initial().name, 'initial')
    afd_graph.add_node(initial_node)

    do_afd(afd_graph, graph, graph.get_initial(), afd_graph.get_initial())

    print_graph(graph, 'AFE')
    print_graph(afd_graph, 'AFD')

    plot(afd_graph)

    return afd_graph


def do_afd(afd_graph, original_graph, node_from_original, node_from_afd):
    if not node_from_original.edges:
        node_from_afd.category = 'final'

    for e in node_from_original.edges:
        if e.variable == EMPTY_STATE:
            do_afd(afd_graph, original_graph, e.tgt, node_from_afd)
        else:
            if afd_graph.verify_exist(e.tgt.name):
                node_from_afd.add_edge(Edge(node_from_afd, e.tgt, e.variable))
            else:
                n = Node(e.tgt.name, 'incremental')
                node_from_afd.add_edge(Edge(node_from_afd, n, e.variable))
                afd_graph.add_node(n)

                do_afd(afd_graph, original_graph, e.tgt, n)


def minimize_afd(afd_graph, alphabet):
    complete_graph(afd_graph, alphabet)
    print_graph(afd_graph, 'PRE MINIMIZED')
    similars = get_similars(afd_graph)

    print_similars(similars, "COMPLETO")

    for s in similars:
        node_from_1 = afd_graph.get_node_by_name(s.name1)
        node_from_2 = afd_graph.get_node_by_name(s.name2)

        for a in alphabet:
            node_to_1 = node_from_1.verify_letter_exists(a)
            node_to_2 = node_from_2.verify_letter_exists(a)

            similar_pair = find_similar(similars, node_to_1.name, node_to_2.name)

            if node_to_1.name == node_to_2.name:
                continue
            elif similar_pair:
                s.dependencies.append(Similar(similar_pair.name1, similar_pair.name2))
            else:
                s.marked = True
                verify_dependencies(similars)

    print_similars(similars, "VALIDS")

    build_minimized_graph(afd_graph, similars)
    plot(afd_graph)


def complete_graph(afd_graph, alphabet):
    new_node = Node("D", "extra")

    add_node = False

    for letter in alphabet:
        new_node.add_edge(Edge(new_node, new_node, letter))

    for a in alphabet:
        for n in afd_graph.nodes:
            if not n.verify_letter_exists(a) and n.category not in ["final", "extra"] and not n.visited:
                add_node = True
                n.add_edge(Edge(n, new_node, a))
                new_node.visited = True
            n.visited = True
        afd_graph.clear_visited()

    if add_node:
        afd_graph.add_node(new_node)


def get_similars(afd_graph):
    similars = []
    for n1 in afd_graph.nodes:
        for n2 in afd_graph.nodes:
            if n1.name is not n2.name:
                if n1.category != "final"\
                        and n2.category != "final"\
                        and not find_similar(similars, n1.name, n2.name):
                    similars.append(Similar(n1.name, n2.name))
    return similars


def find_similar(similars, name1, name2):
    for s in similars:
        if (s.name1 == name1 and s.name2 == name2) or (s.name1 == name2 and s.name2 == name1):
            return s
    return False


def print_similars(similars, name):
    print(name + ": " + str(len(similars)))
    for s in similars:
        print("[" + str(s.name1) + "," + str(s.name2) + "]")
    print("\n")


def verify_dependencies(similars):
    for s in similars:
        if s.marked:
            for x in similars:
                if s.name1 == x.name1 and s.name2 == x.name2:
                    continue
                else:
                    for d in x.dependencies:
                        if d.name1 == s.name1 and d.name2 == s.name2:
                            x.marked = True

    for s in similars:
        if s.marked:
            similars.remove(s)


def build_minimized_graph(afd_graph, similars):
    graph = Graph()

    for s in similars:
        node1 = afd_graph.get_node_by_name(s.name1)
        node2 = afd_graph.get_node_by_name(s.name2)

        if node1.category == "final" and node2.category == "final":
            new_node = Node(s.name1 + "-" + s.name2)


if __name__ == "__main__":
    main()
