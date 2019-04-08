from functions import *


def main():
    operators = ['(', ')', '+', '*', '|', '.']

    while True:
        reg_exp = input("Digite a expressão regular: ")

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

    str_posfixa = convert(reg_exp)
    print("Posfixa: {}".format(str_posfixa))
    graph = calculate(str_posfixa)
    afe_to_afd(graph, reg_exp)


def afe_to_afd(graph, reg_exp):
    afd_graph = Graph()
    initial_node = Node(graph.get_initial().name, 'initial')
    afd_graph.add_node(initial_node)

    do_afd(afd_graph, graph, graph.get_initial(), afd_graph.get_initial())

    print_graph(graph, 'AFE')
    print_graph(afd_graph, 'AFD')

    plot(afd_graph, reg_exp)


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


if __name__ == "__main__":
    main()
