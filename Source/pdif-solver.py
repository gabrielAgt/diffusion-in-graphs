#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from graph import *
import args
import output

"""
	Elimina os elementos duplicados de um conjunto
"""
def remove_duplicate_elements(_set):
	return list(set(_set))

"""
	Retorna a cardinalidade do conjunto união conjunto de alcance do nó
"""
def unionlen(_set, we2):
	return len(remove_duplicate_elements(_set + we2))

# Retorna os nós fontes e os nós que são alcançado por ele
def getsrcwithwe_achieved(graph):
	"""
		Retorna uma matriz contendo a transitividade do dígrafo
		O calculo da transitividade está sendo calculado com base no algoritmo de Warshall
	"""
	def transitivity_calc(graph, size):
		for x in range(size):
			for y in range(size):
				for z in range(size):
					if graph[x][y] and graph[y][z]:
						graph[x][z] = 1
		return graph

	# Tamanho do dígrafo
	size = graph.getsize()
	# Nós fontes
	wesrc = graph.wesrc()
	# Transitividade do dígrafo
	transitivity = transitivity_calc(graph.getGraph(), graph.getsize())

	x = 0 # Posição do nó
	for we in wesrc: # Percorre todos os nós fontes
		for y in range(size): # Um for do tamanho do dígrafo
			if transitivity[we['node']][y]: # Verifica se possui uma relação
				wesrc[x]['we_achieved'].append(y) # Coloca no conjunto de nós alcançado
				wesrc[x]['we_achieved_len'] += 1
		x += 1

	return wesrc

"""
	Algoritmo aleatório
	
	graph => Objeto do dígrafo para a manipulação dos calculos
	n_porce => Quantidade de nós que devem ser atingido
"""
def random_solution(graph, n_porce):
	wesrc = getsrcwithwe_achieved(graph) 
	we_len = len(wesrc)

	# listweSolution => Guarda todos os nós fontes que serão util
	# listwe         => Conjunto com todos os nós já atigindos
	listweSolution, listwe = [], []

	# Enquanto a quantidade de nós não for atingida ele ira sortear outros nós fontes
	while len(listwe) < n_porce:
		we = random.choice(wesrc) # Sortear outro no fonte
		count = unionlen(listwe, we['we_achieved']) # Cardinalidade da união do conjunto de nós já atigindos
		if count > len(listwe): # Verifica se os nós já foram atingido
			listwe = remove_duplicate_elements(listwe + we['we_achieved'])
			listweSolution.append(we)

	return listweSolution

"""
	Algoritmo guloso
	
	graph => Objeto do dígrafo para a manipulação dos calculos
	n_porce => Quantidade de nós que devem ser atingido
"""
def greedy_solution(graph, n_porce):

	# Lista de todos os nós fontes já ordenado em ordem decrescente
	wesrc = sorted(getsrcwithwe_achieved(graph), key=lambda we: we['we_achieved_len'], reverse=True)

	# listweSolution => Guarda todos os nós que serão util
	# listwe         => Lista de todos os nós que são atingido
	listweSolution, listwe = [], []

	# Nó com maior percentual de alcance
	listwe = remove_duplicate_elements(listwe + wesrc[0]['we_achieved'])
	listweSolution.append(wesrc[0])

	# Verificação para saber se ele já cobre a quantidade necessaria
	if wesrc[0]['we_achieved_len'] >= n_porce:
		return listweSolution
	else:
		for we in wesrc[1::]: # Percorre todo o conjunto de nós fontes pulando o primeiro indice
		
			# Tamanho da união do conjunto de nós atingido com os atigindos pelo nó src
			# Caso a cardinalidade da união for menor ou igual a cardinalidade do conjunto solução
			# então todos os nós atingidos são os mesmos
			count = unionlen(listwe, we['we_achieved'])
			if count > len(listwe): # Verifica se os nós já foram atingido
				listwe = remove_duplicate_elements(listwe + we['we_achieved']) # Elimina os elementos duplicado
				listweSolution.append(we)
				if count >= n_porce: # Verifica se já alcançou a meta
					break

		return listweSolution

def main():
	# Obtendo os argumentos
	arguments = args.get()

	# Sementa para geração de números aleatórios
	random.seed(arguments.seed)

	# Instância do dígrafo
	graph = Graph()
	graph.load(arguments.input) # Carregamento do arquivo para o formato de matriz binária

	# Número de nós que deverá ser atingido
	n_porce = int((graph.getsize() * arguments.percentage) / 100)

	solutions = None
	if arguments.method.lower() == 'g':
		solutions = greedy_solution(graph, n_porce)
	elif arguments.method.lower() == 'a':
		solutions = random_solution(graph, n_porce)
	else:
		print("\nError: Método de solução inválida\n")

	# Caso tenha encontrado alguma solução então ele gera os arquivos de logs
	if solutions:
		output.resolve(graph, solutions, arguments)

	print('\nMelhor Solução\nNós fontes que deveram ser utilizado: ')
	for solution in solutions:
		print(f'{solution["node"] + 1} ', end=' ')
	print('\n')

if __name__ == '__main__':
	main()
