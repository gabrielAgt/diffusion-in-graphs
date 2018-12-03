BASE_PATH = './logs/' # Caminho base para os arquivos de saída

# Gera as duas saidas
def resolve(graph, solutions, arguments):
	create_file_dot(graph, solutions, arguments)
	create_file_log(graph, solutions, arguments)

# Saida de arquivo .dot
def create_file_dot(graph, solutions, arguments):

	"""
		Retorna um dicionário com os nós utilizados e os nós alcançados
	"""
	def get_we_numbersrc(solutions):
		return {
			'nodes': [number['node'] for number in solutions], 
			'nodes_achieved': [number for solution in solutions for number in solution['we_achieved']]}

	wesrc = get_we_numbersrc(solutions)
	len_g = graph.getsize()
	
	header, body = '', ''
	for x in range(len_g):
		# Cabeçalho
		header += '	' + str(x + 1)
		if x in wesrc['nodes']:
			header += ' [fillcolor=yellow, style=filled]'
		elif x in wesrc['nodes_achieved']:
			header += ' [color=red]'
		header += ';\n'

		# Gera os relacionamentos
		for y in range(len_g):
			if graph.getedge(x, y):
				body += f'	{x + 1} -> {y + 1}'
				if y in wesrc['nodes_achieved'] and (x in wesrc['nodes_achieved'] or x in wesrc['nodes']):
					body += ' [color=red]'
				body += ';\n'

	content = f'# Dígrafo: {arguments.input}\n' +'digraph {\n' + header + body + '}'

	file = open(f'{BASE_PATH}{arguments.output}.dot', 'w')
	file.write(content)
	file.close() 

# Saida de log
def create_file_log(graph, solution, arguments):
	file = open(f'{BASE_PATH}{arguments.output}.log', 'a+')
	file.writelines(f'{arguments.input} {graph.getsize()} {graph.getarcs()} {arguments.seed} {arguments.method} {len(solution)}\n')
	file.close()
