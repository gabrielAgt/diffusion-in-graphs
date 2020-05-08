#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import argparse
from graph import Graph
from logger import log


def remove_duplicate_elements(_set):
    """
    Elimina os elementos duplicados de um conjunto
    :param _set:
    :return:
    """
    return list(set(_set))


def order_nodes(_set):
    """
    Ordenação do conjunto em ordem decrescente
    :param _set:
    :return:
    """
    return sorted(_set, key=lambda we: we['we_achieved_len'], reverse=True)


def union_len(_set, we2):
    """
    Retorna a cardinalidade do conjunto união conjunto de alcance do nó
    :param _set:
    :param we2:
    :return:
    """
    return len(remove_duplicate_elements(_set + we2))


def src_with_we_achieved(graph):
    """
    Retorna os nós fontes e os nós que são alcançado por ele
    :param graph:
    :return:
    """
    def fw(graph, size):
        """
        Retorna uma matriz contendo a transitividade do dígrafo
        O calculo da transitividade está sendo calculado com base no algoritmo de Warshall
        :param graph:
        :param size:
        :return:
        """
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    if graph[x][y] and graph[y][z]:
                        graph[x][z] = 1
        return graph

    # Tamanho do dígrafo
    size = graph.size()
    # Nós fontes
    we_src = graph.we_src()
    # Transitividade do dígrafo
    transitivity = fw(graph.copy(), graph.size())

    x = 0  # Posição do nó
    for we in we_src:  # Percorre todos os nós fontes
        for y in range(size):  # Um for do tamanho do dígrafo
            if transitivity[we['node']][y]:  # Verifica se possui uma relação
                # Coloca no conjunto de nós alcançado
                we_src[x]['we_achieved'].append(y)
                we_src[x]['we_achieved_len'] += 1

        # Coloca no conjunto de nós alcançado
        we_src[x]['we_achieved'].append(we_src[x]['node'])
        we_src[x]['we_achieved_len'] += 1
        x += 1

    return we_src


def random_solution(graph, n_porce):
    """
    Algoritmo aleatório
    :param graph: Objeto do dígrafo para a manipulação dos calculos
    :param n_porce: Quantidade de nós que devem ser atingido
    :return:
    """
    we_src = src_with_we_achieved(graph)  # Nós fontes
    we_len = len(we_src)  # Quantidade de nós fontes

    # list_we_solution => Conjunto com todos os nós fontes que serão util
    # node_set_achieved         => Conjunto de todos os nós já atigindos
    list_we_solution, node_set_achieved = [], []

    v = 0  # Total de vezes que o loop rodou
    # Enquanto a quantidade de nós não for atingida ele ira sortear outros nós fontes
    while len(node_set_achieved) < n_porce:
        # Verifica se já sorteou todos os nós fontes,
        # caso seja verdade e não tiver encontrado uma solução ele retorna nulo
        if v >= we_len:
            return None, None

        we = random.choice(we_src)  # Sortear outro no fonte
        # Cardinalidade da união do conjunto de nós já atigindos
        count = union_len(node_set_achieved, we['we_achieved'])
        if count > len(node_set_achieved):  # Verifica se os nós já foram atingido
            node_set_achieved = remove_duplicate_elements(
                node_set_achieved + we['we_achieved'])
            list_we_solution.append(we)
        # Remove da lista de nós fontes para não ser sorteado novamente
        we_src.remove(we)

        v += 1

    return list_we_solution, node_set_achieved


def greedy_solution(graph, n_porce):
    """
    Algoritmo guloso
    :param graph: Objeto do dígrafo para a manipulação dos calculos
    :param n_porce: Quantidade de nós que devem ser atingido
    :return:
    """
    we_src = order_nodes(src_with_we_achieved(graph))

    # list_we_solution  => Conjunto com todos os nós que serão util
    # node_set_achieved => Conjunto de todos os nós que são atingido
    list_we_solution, node_set_achieved = [], []

    # Nó com maior percentual de alcance
    node_set_achieved = remove_duplicate_elements(
        node_set_achieved + we_src[0]['we_achieved'])
    list_we_solution.append(we_src[0])

    count = 0
    # Verificação para saber se ele já cobre a quantidade necessaria
    if we_src[0]['we_achieved_len'] >= n_porce:
        return list_we_solution, node_set_achieved
    else:
        for we in we_src[1::]:  # Percorre todo o conjunto de nós fontes pulando o primeiro indice

            # Tamanho da união do conjunto de nós atingido com os atigindos pelo nó src
            # Caso a cardinalidade da união for menor ou igual a cardinalidade do conjunto solução
            # então todos os nós atingidos são os mesmos
            count = union_len(node_set_achieved, we['we_achieved'])
            if count > len(node_set_achieved):  # Verifica se os nós já foram atingido
                node_set_achieved = remove_duplicate_elements(
                    node_set_achieved + we['we_achieved'])  # Elimina os elementos duplicado
                list_we_solution.append(we)
                if count >= n_porce:  # Verifica se já alcançou a meta
                    break

        if count >= n_porce:  # Caso tenha chegado na meta retorna os nós que serão utilizado
            return list_we_solution, node_set_achieved
        else:  # Caso contrario retorna nulo
            return None, None


def solver(arguments):
    """
    :param arguments:
    :return:
    """
    # Sementa para geração de números aleatórios
    random.seed(arguments.seed)

    # Instância do dígrafo
    graph = Graph()

    # Carregamento do arquivo para o formato de matriz binária
    graph.load(arguments.input)

    # Número de nós que deverá ser atingido
    n_porce = int((graph.size() * arguments.percentage) / 100)

    solutions, node_set_achieved = None, []
    if arguments.method.lower() == 'g':
        solutions, node_set_achieved = greedy_solution(graph, n_porce)
    elif arguments.method.lower() == 'a':
        solutions, node_set_achieved = random_solution(graph, n_porce)
    else:
        print('\nError: Método de solução inválida\n')

    # Caso tenha encontrado alguma solução então ele gera os arquivos de logs
    if solutions and node_set_achieved:
        log(graph, solutions, node_set_achieved, arguments)

        print('Melhor Solução\nNós fontes que deveram ser utilizado: ')
        for solution in solutions:
            print(f'{solution["node"] + 1} ', end=' ')
        print('\n')
    else:  # Mostra que não achou uma solução para a porcentagem encontrada
        print('Não existe nós suficientes para cobrir esta porcentagem\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Problema da Mínima Difusão Parcial em Grafos Direcionados')

    parser.add_argument('seed',
                        help='Valor inteiro de semente informada pelo usuário que será usada para inicializar o gerador de números aleatórios', type=int)
    parser.add_argument('percentage',
                        help='Valor correspondente à p-difusão alvo, ou seja, qual é o valor percentual p de nós que devem ser atingidos na rede para considerar a difusão bem sucedida',
                        type=int)
    parser.add_argument('method',
                        help='Letra que indica qual método utilizar: \'g\' para algoritmo guloso, \'a\' para método aleatório')
    parser.add_argument('input',
                        help='Nome do arquivo de que contem a descrição de um grafo no formato ASCII DIMACS')
    parser.add_argument('output',
                        help='Nome do arquivo de saída gerado automaticamente pelo aplicativo e que contêm o log dos calculos realizados')

    solver(parser.parse_args())
