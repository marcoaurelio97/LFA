from classes.similar import Similar
from functions import *


def main():
    operators = ['(', ')', '+', '*', '|', '.']

    while True:
        # reg_exp = input("Digite a expressão regular: ")
        reg_exp = "(a|b).c"

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
    afd_graph = afe_to_afd(graph, reg_exp)
    minimize_afd(afd_graph, alphabet)


def get_alphabet(reg_exp):
    alphabet = []
    for c in reg_exp:
        if ('A' <= c <= 'Z') or ('a' <= c <= 'z'):
            alphabet.append(c)
    return alphabet


def afe_to_afd(graph, reg_exp):
    afd_graph = Graph()
    initial_node = Node(graph.get_initial().name, 'initial')
    afd_graph.add_node(initial_node)

    do_afd(afd_graph, graph, graph.get_initial(), afd_graph.get_initial())

    print_graph(graph, 'AFE')
    print_graph(afd_graph, 'AFD')

    plot(afd_graph, reg_exp)

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
    print_graph(afd_graph, 'aasdfasdf')
    similars = get_similars(afd_graph)

    # print(similars)
    for s in similars:
        print("[" + str(s.node1.name) + "," + str(s.node2.name) + "]")

    # plot(afd_graph, 'teste')

    # analysis = []
    #
    # for s in similars:
    #     node_from_1 = afd_graph.get_node_by_name(s[0])
    #     node_from_2 = afd_graph.get_node_by_name(s[1])
    #
    #     for a in alphabet:
    #         node_to_1 = node_from_1.verify_letter_exists(a)
    #         node_to_2 = node_from_2.verify_letter_exists(a)
    #
    #         if node_to_1 and node_to_2:
    #             # if [node_to_1.name, node_to_2.name] not in similars \
    #             #         and [node_to_2.name, node_to_1.name] not in similars\
    #             #         and s in similars:
    #             #     similars.remove(s)
    #             if node_to_1 != node_to_2 and ([node_to_1, node_to_2] in similars\
    #                     or [node_to_2, node_to_1] in similars):
    #                 analysis = []
    #
    # print(similars)


def complete_graph(afd_graph, alphabet):
    node_name = 100
    for a in alphabet:
        for n in afd_graph.nodes:
            if not n.verify_letter_exists(a) and n.category not in ["final", "extra"] and not n.visited:
                new_node = Node(node_name, "extra")
                n.add_edge(Edge(n, new_node, a))
                afd_graph.add_node(new_node)
                node_name += 1
                new_node.visited = True

                for letter in alphabet:
                    new_node.add_edge(Edge(new_node, new_node, letter))
            n.visited = True
        afd_graph.clear_visited()


def get_similars(afd_graph):
    similars = []
    for n1 in afd_graph.nodes:
        for n2 in afd_graph.nodes:
            if n1.name is not n2.name:
                if n1.category != "final"\
                        and n2.category != "final"\
                        and Similar(n1, n2) not in similars\
                        and Similar(n2, n1) not in similars:
                    similars.append(Similar(n1, n2))
    return similars


if __name__ == "__main__":
    main()
