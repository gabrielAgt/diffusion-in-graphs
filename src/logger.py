BASE_PATH = './logs/'  # Caminho base para os arquivos de saída


def log(graph, solutions, nodesetachieved, arguments):
    """
    Gera as duas saidas
    :param graph:
    :param solutions:
    :param nodesetachieved:
    :param arguments:
    :return:
    """
    create_file_dot(graph, solutions, nodesetachieved, arguments)
    create_file_log(graph, solutions, arguments)


def create_file_dot(graph, solutions, nodesetachieved, arguments):
    """
    Saida de arquivo .dot
    :param graph:
    :param solutions:
    :param nodesetachieved:
    :param arguments:
    :return:
    """
    we_src = [solution['node'] for solution in solutions]
    len_g = graph.size()

    header, body = '', ''
    for x in range(len_g):
        # Cabeçalho
        header += '	' + str(x + 1)
        if x in we_src:
            header += ' [fillcolor=yellow, style=filled]'
        elif x in nodesetachieved:
            header += ' [color=red]'
        else:
            header += ' [color=black]'
        header += ';\n'

        # Gera os relacionamentos
        for y in range(len_g):
            if graph.edge(x, y):
                body += f'	{x + 1} -> {y + 1}'
                if y in nodesetachieved and (x in nodesetachieved or x in we_src):
                    body += ' [color=red]'
                body += ';\n'

    content = f'# Dígrafo: {arguments.input}\n' + \
        'digraph {\n' + header + body + '}'

    file = open(f'{BASE_PATH}{arguments.output}.dot', 'w')
    file.write(content)
    file.close()


def create_file_log(graph, solution, arguments):
    """
    Saida de log
    :param graph:
    :param solution:
    :param arguments:
    :return:
    """
    file = open(f'{BASE_PATH}{arguments.output}.log', 'a+')
    file.writelines(
        f'{arguments.input} {graph.size()} {graph.len_arcs()} {arguments.seed} {arguments.method} {len(solution)}\n')
    file.close()
