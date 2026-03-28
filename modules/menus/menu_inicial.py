from .common import *

def menu_inicial(qtde_opcoes = 5):

    painel = Panel('        Selecione uma das opções:\n[bright_cyan]'
                   '            [ 1 ] - CÁLCULO DE FICHAS\n\n[bright_green]'
                   '            [ 2 ] - CONSULTAR/VALIDAR FICHAS\n\n[bright_yellow]'
                   '            [ 3 ] - DEFINIÇÃO DE COBRANÇAS\n\n[dark_orange]'
                   '            [ 4 ] - GERENCIAR USUÁRIOS\n\n[purple]'
                   '            [ 5 ] - GERAR MENSAGEM DE COBRANÇA\n\n[bright_red]'
                   '            [ 6 ] - ENCERRAR PROGRAMA'
                   ,title='[cyan]GRÊMIO DOS TENENTES MBIAM', title_align='center',width=85)
    print(painel, '\n')
    opcao = validar.valida_int('          --→  ', 1, qtde_opcoes)
    console.clear()
    return opcao
