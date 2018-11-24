#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import graph as g
import output
import args

# Retorna os nós fontes, os nós que são alcançado por ele
def getsrcwithwe_achieved(graph):
	size = graph.getsize() # Tamanho do dígrafo
	wesrc = graph.wesrc() # Nós fontes
	tra = graph.transitivity() # Transitividade do dígrafo

	x = 0 # Posição do nó
	for we in wesrc: # Percorre todos os nós fontes
		for y in range(size): # Um for do tamanho do dígrafo
			if tra[we['node']][y]: # Verifica se possui uma relação
				wesrc[x]['we_achieved'].append(y) # Coloca no conjunto de nós alcançado
				wesrc[x]['we_achieved_len'] += 1
		x += 1

	return wesrc

def unionlen(we1, we2):
	return  len(list(set(we1 + we2)))

def get_number_random(n):
	return random.randint(0, n)

def random_solution(graph, n_porce):
<<<<<<< HEAD
	wesrc = getsrcwithwe_achieved(graph)
	we_len = len(wesrc)

	# listweSolution => Guarda todos os nós fontes que serão util
	# count          => Quantidade de nós ja atigindos
	listweSolution, count = [], 0

	# Enquanto a quantidade de nós não for atingida ele ira sortear outros nós fontes
	while count < n_porce:
		we = wesrc[get_number_random(we_len) - 1] # Sortear outro no fonte
		count += we['we_achieved_len']
		listweSolution.append(we)

	return listweSolution

=======
	pass
	
>>>>>>> parent of b643eb2... Procedimento aleatório e reestruturação do projeto
def greedy_solution(graph, n_porce):
	"""
		Retorna o tamanho do conjunto de nós alcançado
	"""
	def getwe_achievedlen(we): 
		return we['we_achieved_len']

	# Lista de todos os nós fontes já ordenado em ordem decrescente
	wesrc = sorted(getsrcwithwe_achieved(graph), key=getwe_achievedlen, reverse=True)

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


	solution = None
	if arguments.method.lower() == 'g':
		solution = greedy_solution(graph, n_porce)
	elif arguments.method.lower() == 'a':
		solution = random_solution(graph, n_porce)
	else:
		print("Error: Método de solução inválida\n")

	if solution:
		output.create_file_dot(graph, f'Dot/{arguments.output}')
		output.create_file_log(graph, solution, f'{arguments.output}', arguments)

if __name__ == '__main__':
	main()
