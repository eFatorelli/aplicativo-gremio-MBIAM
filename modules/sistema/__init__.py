from ..oparquivo import *
from rich.console import Console
from rich import print
from ..tabelas import tabela_cadastro
from ..validar import nomemes
from pathlib import Path

console = Console()

def cadastrar_usuario(arquivo, nome):
    """
    Menu para cadastrar um Usuário, baseando-se em seu nome.

    O cadastro de um Usuário gera automaticamente um ID, e permite que
    sejam cadastrados apelidos para auxiliar na identificação.

    :param arquivo: Arquivo do cadastro de usuários.
    :param nome: Nome do Usuário.
    :return: True caso seja possível criar
             False caso não seja possível criar (problemas de arquivo)
             None caso o arquivo esteja corrompido.
    """
    from ..classes import Usuario
    from ..validar import valida_sn


    if not arquivo.exists():
        if cria_arq(arquivo):
            escreva_arq(arquivo,[],ext='json',sobrescreva= True)
        else:
            print('ERRO ao criar o arquivo!')
            return False
    dados = ler_arq(arquivo,ext = 'json')
    if dados is False or dados is None:
        if valida_sn('O arquivo está corrompido. Deseja sobrescrevê-lo? [ S / N ] → '):
            escreva_arq(arquivo,[],ext='json',sobrescreva=True)
        else:
            return None
    usuario = Usuario(nome)
    dados = ler_arq(arquivo, ext='json')
    for cont, u in enumerate(sorted(dados, key= lambda i: i['id'])):
        if cont+1 != u['id']:
            usuario.definir_id(cont+1)
            break
    else:
        usuario.definir_id(len(dados)+1)
    if valida_sn('Deseja adicionar [bright_blue]APELIDOS[/] '
                 'pelo qual o usuário pode ser identificado?\n [ S / N ] → ', n_auto= False):
        while True:
            apelido = str(console.input('Digite um apelido. Quando quiser finalizar, digite "FIM".\n → ').strip())
            if apelido.upper() == 'FIM':
                nfim = str(console.input('Você digitou fim. Caso esse seja um apelido, digite [cyan]"APELIDO"[/].\n'
                                         'Caso só queira sair, pressione [green]ENTER[/].').strip().upper())
                if nfim == 'APELIDO':
                    usuario.apelidar(apelido)
                else:
                    break
            else:
                usuario.apelidar(apelido)
    console.clear()
    tabela_cadastro(usuario.id,usuario.nome,usuario.apelidos)
    dados.append(usuario.to_dict())
    console.input('Pressione [green]ENTER[/] para continuar.')
    return dados


def localizar_usuario(lista, localizador, metodo: Literal['id','nome','apelido']):
    """
    -> Localiza um usuário pelo parâmetro informado em uma lista gerada.
    :param lista: Lista onde o usuário será procurado.
    :param localizador: ID, nome ou apelido do usuário.
    :param metodo: Método pelo qual a busca será feita: por ID, nome ou apelido.
    :return: Retorna o dicionário do usuário caso seja encontrado e None caso não seja.
    """
    for u in lista:
        if metodo == 'apelido' and localizador in u['apelidos']:
            return u
        elif metodo != 'apelido' and u[metodo] == localizador:
            return u
    return None


def localizar_cobranca(arquivo,ano,mes):
    dados = ler_arq(arquivo,ext='json')
    cont = 0
    for u in dados:
        if u['historico'].get(f'{ano}-{mes:0>2}'):
            cont+=1
    return cont


def idt_caloteiro(obj):

    """
    -> Identifica se, no arquivo do mês anterior, existe alguém inadimplente.
    :param obj: Nome a ser procurado no arquivo.
    :return: Valor (float) caso seja identificado o nome inadimplente;
             Caso contrário, retorna False.
    """

    user_dict = obj.to_dict()
    s = 0
    dat_extenso = list()
    for data, ficha in user_dict['historico'].items():
        if not ficha['pagou']:
            data_certa = f'{nomemes(int(data[-2:])).title()} de {data[:4]}'
            dat_extenso.append(data_certa)
            s+= ficha['val_final']
    data = ', '.join(dat_extenso)
    return data, s


def atualizar_ficha(arquivo, usuario_atualizado):
    dados = ler_arq(arquivo,ext='json')
    for i, u in enumerate(dados):
        if u['id'] == usuario_atualizado.id:
            dados[i] = usuario_atualizado.to_dict()
            return dados
    else:
        print('ERRO AO GUARDAR OS DADOS!')
        return None
