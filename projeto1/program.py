from classes.node import Node
from classes.graph import Graph

while (True) :
    variaveis = input('Digite as variáveis: ')

    if (variaveis == '') :
        print('Digite no mínimo uma variável!')
        continue

    variaveis = variaveis.split(' ')

    if (len(variaveis) >= 1) :
        break

while (True) :
    alfabeto = input('Digite as letras do alfabeto: ')

    if (alfabeto == '') :
        print('Digite no mínimo uma letra do alfabeto!')
        continue

    alfabeto = alfabeto.split(' ')

    if (len(alfabeto) >= 1) :
        break

regras = []

while (True) :
    regra = input('Digite uma regra de produção separada por espaço ou FIM para continuar: ')

    if (regra == 'FIM' and len(regras) > 0) :
        break
    elif (regra == 'FIM') :
        print('Digite no mínimo uma regra!')
        continue

    regra_valida = True

    for r in list(regra) :
        if (r != " ") :
            if (r not in variaveis and r not in alfabeto) :
                print('Regra inválida!')
                regra_valida = False
                break
    
    if (not regra_valida) :
        continue

    regra = regra.split(' ')

    if (len(regra) != 2) :
        print('Uma regra deve ter 2 parâmetros!')
        continue

    regras.append([regra[0], regra[1]])

while (True) :
    var_inicial = input('Digite a variável inicial: ')
    
    if (var_inicial in variaveis) :
        break
    
    print('Variável não existe!')

op = input('1 - Palavra\n2 - Ordem\n')

if (op == '1') :
    found = False
    palavra = input('Digite a palavra: ')
    graph = Graph([])

    for reg in regras :
        if(reg[0] == var_inicial) :
            idx = regras.index(reg)

    node = Node(None, regras[idx], var_inicial)

    if node.word == palavra :
        found = True

    graph.nodes.append(node)
    fila = [node]

    while (len(fila) > 0 and not found) :
        refer = fila.pop(0)
        for r in regras :
            if (refer.word != -1) :
                n = Node(refer, r, refer.word)
                graph.nodes.append(n)
                fila.append(n)

                if (n.word == palavra) :
                    found = True
                    node = n
                    break

        if (found) :
            break

    resposta = node.word
    substituicoes = []
    
    while (node.parent != None) :
        substituicoes.insert(0,'({} -> {})'.format(node.rule[0],node.rule[1]))
        node = node.parent
    
    substituicoes.insert(0,'({} -> {})'.format(node.rule[0],node.rule[1]))

    print('\nVariável Inicial -> ' + var_inicial)
    print()
    for i in range(len(substituicoes)) :
        print(substituicoes[i])

elif (op == '2') :
    print('\n')
    for r in regras :
        print('Regra #{0}: {1}'.format(regras.index(r), r))
    print('\n')

    while (True) :
        ordem = input('Digite a ordem das regras separadas por espaço: ')

        if (ordem == '') :
            print('Digite no mínimo uma regra a ser executada!')
            continue

        ordem = ordem.split(' ')
        valida_ordem = True

        for o in ordem :
            try :
                o = int(o)
            except ValueError :
                print('Ordem inválida!')
                valida_ordem = False
                break

            if (o < 0 or o > len(regras) - 1) :
                print('Ordem inválida!')
                valida_ordem = False
                break
        
        if (not valida_ordem) :
            continue

        if (regras[int(ordem[0])][0] != var_inicial) :
            print('A derivação deve começar pela variável inicial!')
            continue
        else :
            break

    resposta = var_inicial

    for ord in ordem :
        regra = regras[int(ord)][0]

        if regra in resposta :
            swap = regras[int(ord)][1]
            resposta = resposta.replace(regra, swap, 1)

palavra_valida = True

for str in resposta :
    if (str not in alfabeto) :
        palavra_valida = False

if (palavra_valida) :
    print('\nPalavra válida: ' + resposta)
else :
    print('\nPalavra inválida: ' + resposta)