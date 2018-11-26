def create_file_dot(graph, path):
	def get_we_numbersrc():
		wesrc = graph.wesrc()
		return [number['node'] for number in wesrc]

	wesrc = get_we_numbersrc()
	tra = graph.transitivity()
	len_g = graph.getsize()

	header, body = '', ''
	for x in range(len_g):
		header += '	' + str(x + 1)
		if x in wesrc:
			header += ' [fillcolor=yellow, style=filled]'
		header += ';\n'

		for y in range(len_g):
			if tra[x][y]:
				body += f'	{x + 1} -> {y + 1};\n'


	content = 'digraph {\n' + header + body + '}'

	file = open(f'{path}.dot', 'w') 
	file.write(content)
	file.close() 

def create_file_log(graph, solution, path, arguments):
	file = open(f'{path}.log', 'a+')
	file.writelines(f'{arguments.input} {graph.getsize()} {graph.getarcs()} {arguments.seed} {arguments.method} {len(solution)}\n')
	file.close()

	
