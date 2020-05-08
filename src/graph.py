class Graph(object):
    def __init__(self):
        # Dígrafo no formato de matriz binária
        self.__graph = None

        # Dígrafo do digrago
        self.__size = 0

        # Quantidade de relacionamento
        self.__edge = 0

    def load(self, filename):
        """
        Carrega uma digrafo no formato ASCII para uma matriz binária
        :param filename: Caminho do digrafo.
        :return:
        """
        try:
            file = open(filename, 'r')
            content = file.readlines()
            for line in content:  # Percorrendo cada linha do arquivo
                line = line.split(' ')
                # Caso o primeiro caracter for igual a 'c' então é uma linha de comentário e não precisa ser tratada
                if line[0] == 'c':
                    continue
                # Linha que indica o tamanho do dígrafo é o número de relacionamentos
                elif line[0] == 'p':
                    self.__size = int(line[2])
                    self.__edge = int(line[3])
                    self.__graph = self.__create()
                elif line[0] == 'e':  # Nós que se relaciona
                    self.add_edge(int(line[1]) - 1, int(line[2]) - 1)

                file.close()
        except Exception as e:
            raise e

    def we_src(self):
        """
        Retorna todos os nós fontes do dígrafo, sendo aqueles nós que se relaciona com outros,
        mas nenhum se relaciona com ele.
        Conjunto de retorno:
                        Ex: [{
                                        'node': <número do nó>,
                                        'degree': <seu grau>,
                                        'we_achieved': <nós alcançados pela transitividade>,
                                        'we_achieved_len': <quantidade de nós alcançado>
                        }]
        :param self:
        :return:
        """
        src = []
        for x in range(self.__size):
            lin, col = 0, 0

            # Para ser um nó fonte esta variavel 'col' deve ser igual a 0, pois nenhum nó se relaciona com ela
            for i in range(self.__size):
                col += self.__graph[i][x]
                lin += self.__graph[x][i]

            if col == 0:
                src.append({'node': x, 'degree': lin,
                            'we_achieved': [], 'we_achieved_len': 0})

        return src

    def add_edge(self, x, y):
        """
        Adiciona mais um arco na relação
        :param self:
        :param x:
        :param y:
        :return:
        """
        self.__graph[x][y] = 1

    def edge(self, x, y):
        """
        Retorna se x se relaciona com y
        :param self:
        :param x:
        :param y:
        :return:
        """
        return bool(self.__graph[x][y])

    def size(self):
        """
        Retorna o número do grafo
        :param self:
        :return:
        """
        return self.__size

    def len_arcs(self):
        """
        Retorna a quantidade de arcos
        :param self:
        :return:
        """
        return self.__edge

    def copy(self):
        """
        Retorna uma copia do dígrafo
        :param self:
        :return:
        """
        graph = self.__create()
        for x in range(self.__size):
            for y in range(self.__size):
                graph[x][y] = self.__graph[x][y]
        return graph

    def __create(self):
        """
        Cria a matriz do dígrafo
        :param self:
        :return:
        """
        return [[0 for x in range(self.__size)] for y in range(self.__size)]

    def __str__(self):
        """
        Quando for dado um "print" no objeto, mostra a matriz binária
        :param self:
        :return:
        """
        s = ''
        for line in self.__graph:
            s += '[' + ', '.join(map(str, line)) + ']\n'
        return s
