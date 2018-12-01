from base64 import b64encode

# Saida de arquivo .dot
def create_file_dot(graph, solutions, path, filename):
	def get_we_numbersrc(solutions):
		return {
			'teste1': [number['node'] for number in solutions], 
			'teste2': [number for solution in solutions for number in solution['we_achieved']]
		}

	wesrc = get_we_numbersrc(solutions)
	len_g = graph.getsize()
	
	header, body = '', ''
	for x in range(len_g):
		header += '	' + str(x + 1)
		if x in wesrc['teste1']:
			header += ' [fillcolor=yellow, style=filled]'
		elif x in wesrc['teste2']:
			header += ' [color=red]'
		header += '\n'

		for y in range(len_g):
			if graph.getedge(x, y):
				body += f'	{x + 1} -> {y + 1}'
				if y in wesrc['teste2'] and (x in wesrc['teste2'] or x in wesrc['teste1']):
					body += ' [color=red]'
				body += '\n'

	content = f'# Dígrafo: {filename}\n' +'digraph {\n' + header + body + '}'
	file = open(f'{path}{b64encode(filename.encode())}.dot', 'w')
	file.write(content)
	file.close() 

# Saida de log
def create_file_log(graph, solution, path, arguments):
	file = open(f'{path}.log', 'a+')
	file.writelines(f'{arguments.input} {graph.getsize()} {graph.getarcs()} {arguments.seed} {arguments.method} {len(solution)}\n')
	file.close()
