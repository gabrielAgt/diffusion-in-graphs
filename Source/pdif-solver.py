#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import graph as g
import output
import args

# Retorna os nós fontes e os nós que são alcançado por ele
def getsrcwithwe_achieved(graph, transitivity):
	size = graph.getsize() # Tamanho do dígrafo
	wesrc = graph.wesrc() # Nós fontes

	x = 0 # Posição do nó
	for we in wesrc: # Percorre todos os nós fontes
		for y in range(size): # Um for do tamanho do dígrafo
			if transitivity[we['node']][y]: # Verifica se possui uma relação
				wesrc[x]['we_achieved'].append(y) # Coloca no conjunto de nós alcançado
				wesrc[x]['we_achieved_len'] += 1
		x += 1

	return wesrc

def unionlen(we1, we2):
	return  len(list(set(we1 + we2)))

def random_solution(graph, transitivity, n_porce):
	wesrc = getsrcwithwe_achieved(graph, transitivity)
	we_len = len(wesrc)

	# listweSolution => Guarda todos os nós fontes que serão util
	# count          => Quantidade de nós ja atigindos
	listweSolution, count = [], 0

	# Enquanto a quantidade de nós não for atingida ele ira sortear outros nós fontes
	while count < n_porce:
		we = random.choice(wesrc) # Sortear outro no fonte
		count += we['we_achieved_len']
		listweSolution.append(we)

	return listweSolution

def greedy_solution(graph, transitivity, n_porce):

	# Lista de todos os nós fontes já ordenado em ordem decrescente
	wesrc = sorted(getsrcwithwe_achieved(graph, transitivity), key=lambda we: we['we_achieved_len'], reverse=True)

	# listweSolution => Guarda todos os nós que serão util
	# listwe         => Lista de todos os nós que são atingido
	listweSolution, listwe = [], []

	# Nó com maior percentual de alcance
	listwe = listwe + wesrc[0]['we_achieved']
	listweSolution.append(wesrc[0])

	# Verificação para saber se ele já cobre a quantidade necessaria
	if wesrc[0]['we_achieved_len'] >= n_porce:
		return listweSolution
	else:
		for we in wesrc[1::]: # Percorre todo o conjunto de nós fontes pulando o primeiro indice
			count = unionlen(listwe, we['we_achieved']) # Tamanho da união do conjunto de nós atingido com os atigindos pelo nó src
			if count > len(listwe): # Verifica se os nós já foram atingido
				listwe = listwe + we['we_achieved']
				listweSolution.append(we)
				if count >= n_porce: # Verifica se já alcançou a meta
					break
		return listweSolution

def main():
	arguments = args.get()

	# Sementa para geração de números aleatórios
	random.seed(arguments.seed)

	# Instância do dígrafo
	graph = g.Graph()
	graph.load(arguments.input) # Carregamento do arquivo para o formato de matriz binária

	# Número de nós que deverá ser atingido
	n_porce = int((graph.getsize() * arguments.percentage) / 100)

	# Transitividade do dígrafo
	transitivity = graph.transitivity()

	solutions = None
	if arguments.method.lower() == 'g':
		solutions = greedy_solution(graph, transitivity, n_porce)
	elif arguments.method.lower() == 'a':
		solutions = random_solution(graph, transitivity, n_porce)
	else:
		print("\nError: Método de solução inválida\n")

	if solutions:
		output.create_file_dot(graph, transitivity, 'Logs/', arguments.input)
		output.create_file_log(graph, solutions, f'Logs/{arguments.output}', arguments)

	print('\nSolução\nNós fontes que deveram ser utilizado: ')
	for solution in solutions:
		print(f'{solution["node"] + 1} ', end=' ')
	print('\n')

if __name__ == '__main__':
	main()
