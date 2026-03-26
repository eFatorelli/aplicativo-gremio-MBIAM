import json
from typing import Literal


def arq_existe(arquivo, *, criar: Literal[True,False] = False):
    """
    ->Verifica se um arquivo existe. Se o usuário preferir, cria o arquivo, caso não exista.
    :param arquivo: Arquivo a ser criado no formato 'str'.
    :param criar: Verifica a existência do arquivo. Caso True, cria o arquivo em sua ausência.
    :return: Retorna True se o arquivo existe OU se criar==True e é possível criar o arquivo.
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
        a = open(arquivo, 'w')
        a.close()
        return True
    except FileNotFoundError:
        print('ERRO - A pasta não existe ou não foi endereçada corretamente.')
        return False
    except Exception as e:
        print('ERRO ao criar arquivo -',e.__class__)
        return False


def ler_arq(arquivo, *, ext: Literal['txt','json'] = 'json', txt_linhas = True):
    """
    -> Lê o arquivo de texto ou json referenciado.
    :param arquivo: Nome do arquivo a ser lido
    :param ext: Extensão do arquivo em questão.
    :param txt_linhas: (SOMENTE TXT) - Não altera funcionamento em json.
                    Caso True retorna as linhas separadas, aglomeradas em uma LISTA
                   Caso False retorna o texto por inteiro.
    :return: Lista (linhas = True) ou str (linhas = False).
    """
    try:
        with open(arquivo, 'r', encoding='utf-8') as a:
            if ext == 'txt':
                if txt_linhas:
                    return a.readlines()
                else:
                    return a.read()
            elif ext == 'json':
                return json.load(a)
    except Exception as e:
        print('ERRO ao ler o arquivo -',e.__class__)
        return False


def escreva_arq(arquivo, escrever, *, ext: Literal['txt','json'] ='json', sobrescreva = False):

    """
    ->Escreve em um arquivo de texto ou json especificado.
    :param arquivo: Arquivo no qual será escrito.
    :param escrever: Texto ('str') a ser acrescentado no arquivo.
    :param ext: Extensão do arquivo ('txt' ou 'json')
    :param sobrescreva: Caso True, sobrescreve ao invés de acrescentar o texto.
    :return: None
    """
    try:
        modo = 'w' if sobrescreva else 'a'
        with open(arquivo, modo,encoding='utf-8') as a:
            if ext == 'txt':
                a.write(escrever if sobrescreva else f'{escrever}\n')
            elif ext == 'json':
                json.dump(escrever, a, indent=4, ensure_ascii=False)
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