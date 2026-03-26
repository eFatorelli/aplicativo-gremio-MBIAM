from time import sleep



def nomemes(nummes):
    meses=['janeiro','fevereiro','março',
           'abril','maio','junho','julho',
           'agosto','setembro','outubro',
           'novembro','dezembro']
    return meses[nummes-1]


def printlinha(tipo='-', tam=85):
    """
    ->Cria uma linha de tamanho variável
    :param tipo: Tipo da linha a ser criada. Por padrão, '-='
    :param tam: Tamanho da linha. Por padrão, 35.
    :return: Linha do tamanho e tipo desejado.
    """
    print(tipo*tam)


