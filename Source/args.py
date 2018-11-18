import argparse

def get():
	parser = argparse.ArgumentParser(description='Problema da Mínima Difusão Parcial em Grafos Direcionados')

	parser.add_argument('seed', 
		help='Valor inteiro de semente informada pelo usuário que será usada para inicializar o gerador de números aleatórios', type=int)
	parser.add_argument('method', 
		help='Letra que indica qual método utilizar: \'g\' para algoritmo guloso, \'a\' para método aleatório')
	parser.add_argument('input',
		help='Nome do arquivo de que contem a descrição de um grafo no formato ASCII DIMACS')
	parser.add_argument('output', 
		help='Nome do arquivo de saída gerado automaticamente pelo aplicativo e que contêm o log dos calculos realizados')

	return parser.parse_args()
