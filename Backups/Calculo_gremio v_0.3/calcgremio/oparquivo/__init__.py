def arq_existe(arquivo, criar=False):
    """
    ->Verifica se um arquivo existe. Se o usuário preferir, cria o arquivo, caso não exista.
    :param arquivo: Arquivo a ser criado no formato 'str'.
    :param criar: Verifica a existência do arquivo. Caso True, cria o arquivo em sua ausência.
    :return: Retorna True se o arquivo existe OU se criar==True e seja possível criar o arquivo.
            Retorna False caso criar==True e o arquivo não possa ser criado.
            Retorna False caso criar==False e o arquivo não existe.
    """
    try:
        a=open(arquivo, 'rt')
        a.close()
        return True
    except FileNotFoundError:
        if not criar:
            return False
        else:
            return cria_arq(arquivo)


def cria_arq(arquivo):
    """
    -> Cria um arquivo de texto.
    :param arquivo: Nome do arquivo a ser criado.
    :return: True caso consiga criar o arquivo.
             False caso haja algum erro.
    """
    try:
        a = open(arquivo, 'wt+')
        a.close()
        return True
    except Exception as e:
        print('ERRO ao criar arquivo -',e.__class__)
        return False


def ler_arq(arquivo,*,linhas = True):
    """
    -> Lê um arquivo de texto referenciado.
    :param arquivo: Nome do arquivo a ser lido
    :param linhas: Caso True retorna as linhas separadas, aglomeradas em uma LISTA
                   Caso False retorna o texto por inteiro.
    :return: Lista (linhas = True) ou str (linhas = False).
    """
    try:
        with open(arquivo, 'rt') as a:
            if linhas:
                return a.readlines()
            else:
                return a.read()
    except Exception as e:
        print('ERRO ao ler o arquivo -',e.__class__)


def print_arq(arquivo):
    try:
        with open(arquivo, 'rt') as a:
            print(a.read())
            a.close()
    except Exception as e:
        print('ERRO ao ler o arquivo -', e.__class__)


def escreva_arq(arquivo, escrever,*,sobrescreva = False):
    """
    ->Acrescenta texto ao arquivo de texto designado.
    :param arquivo: Arquivo no qual será escrito.
    :param escrever: Texto ('str') a ser acrescentado no arquivo.
    :param sobrescreva: Caso True, sobrescreve ao invés de acrescentar o texto.
    :return: None
    """
    try:
        modo = 'wt' if sobrescreva else 'at'
        with open(arquivo, modo,encoding='utf-8') as a:
            a.write(escrever if sobrescreva else f'{escrever}\n')
    except Exception as e:
        print('ERRO ao preencher dados -', e.__class__)


def zerar_arq(arquivo):
    """
    -> Sobrescreve um arquivo, zerando ele.
    :param arquivo: Arquivo a ser sobrescrito.
    :return: True caso consiga sobrescrever o arquivo;
             False caso haja algum erro ao sobrescrever o arquivo.
    """
    try:
        with open(arquivo, 'wt') as a:
            a.write('')
        return True
    except Exception as e:
        print('ERRO ao sobrescrever arquivos -', e.__class__)
        return False

def idt_caloteiro(nome,mes,ano):
    """
    -> Identifica se, no arquivo do mês anterior, existe alguém inadimplente.
    :param nome: Nome a ser procurado no arquivo.
    :param mes: Mes ATUAL
    :param ano: Ano ATUAL
    :return: Valor (float) caso seja identificado o nome inadimplente;
             Caso contrário, retorna False.
    """
    from calcgremio.validar import valida_bool

    if mes - 1 < 1:
        mes += 12
        ano -= 1
    arq_velho = rf'Fichas_Gremio/{ano}_{mes - 1:0>2}.txt'
    if arq_existe(arq_velho, criar=False):
        aux = dict()
        for pessoa in ler_arq(arq_velho):
            f = pessoa[:-1].split(';')
            aux[f[0]] = {'valor': f[1], 'pagou': f[2]}
        if nome in aux and not valida_bool(aux[nome]['pagou']):
            return float(aux[nome]['valor'])
        else:
            return False
    else:
        return False


def deletar_linarq(arquivo, linha):
    try:
        a=open(arquivo, 'rt')
        txtarq=a.read()
        a.close()
        a=open(arquivo, 'wt')
        txtnovo=''
        for cont,l in enumerate(txtarq.split('\n')):
            if not cont==linha:
                txtnovo=f'{txtnovo}{l}\n'
        a.write(f'{txtnovo}')
        a.close()
        print('Linha excluída com sucesso!')
    except Exception as e:
        print('ERRO ao deletar dados -', e.__class__)