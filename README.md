
## Problema da Mínima Difusão Parcial em Grafos Direcionados (PMDPGD)

> O trabalho consiste em solucionar um problema proposto em sala de aula (disciplina matemática discreta), para a mínima difusão em grafos, que consiste em achar uma quantidade mínima de nós para cobrir uma certa porcentagem de algum grafo.

### Instalação

```
$ git clone https://github.com/gabrielAgt/diffusion-in-graphs.git
```

### Como usar

```
python pdif-solver.py --help

usage: pdif-solver.py [-h] <seed> <percentage> <method> <input> <output>

argumentos obrigatórios:
  seed        Valor inteiro de semente informada pelo usuário que será usada
              para inicializar o gerador de números aleatórios
  percentage  Valor correspondente à p-difusão alvo, ou seja, qual é o valor
              percentual p de nós que devem ser atingidos na rede para
              considerar a difusão bem sucedida
  method      Letra que indica qual método utilizar: 'g' para algoritmo
              guloso, 'a' para método aleatório
  input       Nome do arquivo de que contem a descrição de um grafo no formato
              ASCII DIMACS
  output      Nome do arquivo de saída gerado automaticamente pelo aplicativo
              e que contêm o log dos calculos realizados

argumentos opcionais:
  -h, --help  show this help message and exit
```

### Entrada

Os grafos de entrada devem ser no formato ASCII DIMACS. Onde 'c' indica que é uma linha de comentário, 'e' indica os relacionamento de um nó para o outro e 'p edge' o tamanho do grafo e quantidade de relacionamentos.

Exemplo:

```
c example of ASCII DIMACS
p edge 12 11
e 1 2 
e 1 3
e 1 4 
e 1 5 
e 1 6 
e 1 7 
e 1 8 
e 1 9 
e 1 10 
e 1 11 
e 1 12
```

### Saida

O algoritmo tem como saída uma arquivo de log e o grafo no formato dot.

#### Log
Os arquivos de logs seguirão este formato:
instancia | quantidade de arcos | semente | método | tamanho do conjunto solução 

#### Dot
• Os nós que foram selecionados para compor o conjunto solução deverão estar destacados em amarelo;  
• Os arcos e os nós que serão atingidos pelo conjunto solução deverão estar destacados em vermelho;  
• Os demais arcos, não alcançáveis deverão estar em cor preta.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes
