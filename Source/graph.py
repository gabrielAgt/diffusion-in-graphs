class Graph():
	"""
    	Class do dígrafo
    """
	def __init__(self):
		# Dígrafo no formato de matriz binária 
		self.__graph = None

		# Dígrafo do digrago
		self.__size = 0

		# Quantidade de relacionamento
		self.__edge = 0

	"""
		Carrega uma digrafo no formato ASCII para uma matriz binária

		Args:
			filename (str): Caminho do digrafo.
	"""
	def load(self, filename):
		try:
			file = open(filename, 'r')
		except Exception as e:
			raise e

		content = file.readlines()
		for line in content:
			line = line.split(' ')

			if line[0] == 'c': # Caso o primeiro caracter for igual a 'c' então é uma linha de comentário e não presiar se tratada
				continue
			elif line[0] == 'p': # Linha que indica o tamanho do dígrafo é o número de relacionamentos
				self.__size = int(line[2])
				self.__edge = int(line[3])
				self.__create()
			elif line[0] == 'e': # Nós que se relaciona
				self.addedge(int(line[1]) - 1, int(line[2]) - 1)

		file.close()

	"""
		Retorna todos os nós fontes do dígrafo, sendo aqueles nós que se relaciona com outros,
		mas nenhum se relaciona com ele.

		Conjunto de retorno:
			Ex: [{ 'node': <número do nó>, 'degree': <seu grau> }]
	"""
	def wesrc(self):
		src = []
		for x in range(self.__size):
			lin, col = 0, 0
			
			for i in range(self.__size):
				col += self.__graph[i][x] # Para ser um nó fonte esta variavel 'col' deve ser igual a 0, pois nenhum nó se relaciona com ela
				lin += self.__graph[x][i]

			if col == 0 and lin > 0:
				src.append({ 'node': x, 'degree': lin, 'we_achieved': [], 'we_achieved_len': 0 })

		return src

	"""
		Retorna uma matriz contendo a transitividade do dígrafo

		O calculo da transitividade está sendo calculado com base no algoritmo de Warshall
	"""
	def transitivity(self):
		tr = self.__graph.copy()
		for x in range(self.__size):
			for y in range(self.__size):
				for z in range(self.__size):
					if tr[x][y] and tr[y][z]:
						tr[x][z] = 1
		return tr

	"""
		Adiciona mais um arco na relação
	"""
	def addedge(self, x, y):
		self.__graph[x][y] = 1

	"""
		Retorna se x se relaciona com y 
	"""
	def getedge(self, x, y):
		return bool(self.__graph[x][y])

	"""
		Retorna o número do grafo
	"""
	def getsize(self):
		return self.__size

	"""
		Cria a matriz do dígrafo 
	"""
	def __create(self):
		self.__graph = [[0 for x in range(self.__size)] for y in range(self.__size)]

	"""
		Quando for dado um "print" no objeto, mostra a matriz binária
	"""
	def __str__(self):
		response = ''
		for line in self.__graph:
			response +=  '['+ ', '.join(map(str, line)) + ']\n'
		return response
