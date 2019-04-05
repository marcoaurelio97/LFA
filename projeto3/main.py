from functions import *

count = 0


def main():
    operators = ['+', '*', '|', '.']

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
    # plot(graph)
    afe_to_afd(graph)


def afe_to_afd(graph):
    a = 1


if __name__ == "__main__":
    main()
