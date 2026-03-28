import json
from typing import Literal
from pathlib import Path


def cria_arq(arquivo: Path) -> bool:
    """
    -> Cria um arquivo.
    :param arquivo: Nome e caminho do arquivo a ser criado.
    :return: True caso consiga criar o arquivo.
             False caso haja algum erro.
    """
    try:
        arquivo.touch(exist_ok=False)
        return True
    except FileNotFoundError:
        print('ERRO - A pasta não existe ou não foi endereçada corretamente.')
    except FileExistsError:
        print('O arquivo já existe!')
    except Exception as e:
        print('ERRO ao criar arquivo -',e.__class__)
    return False


def ler_arq(arquivo, *, ext: Literal['txt','json'] = 'json'):
    """
    -> Lê o arquivo de texto ou json referenciado.
    :param arquivo: Nome do arquivo a ser lido
    :param ext: Extensão do arquivo em questão.

    :return: Lista (linhas = True) ou str (linhas = False).
             False caso haja algum erro.
    """
    try:
        with open(arquivo, 'r', encoding='utf-8') as a:
            if ext == 'txt':
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