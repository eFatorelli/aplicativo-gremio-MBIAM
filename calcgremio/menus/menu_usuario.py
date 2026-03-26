from .common import *

def menu_usuario(arquivo):
    from calcgremio.sistema import cadastrar_usuario

    dados = oparquivo.ler_arq(arquivo,ext='json')

    while True:
        console.clear()
        painel_inicial = Panel('        Selecione uma das opções:\n[green]'
                       '            [ 1 ] - CADASTRAR USUÁRIOS\n[yellow]'
                       '            [ 2 ] - LISTAR USUÁRIOS\n[bright_blue]'
                       '            [ 3 ] - GERENCIAR USUÁRIOS\n[purple]'
                       '            [ 4 ] - RETORNAR AO MENU PRINCIPAL'
                       ,title='[dark_orange]SISTEMA DE GERENCIAMENTO DE USUÁRIOS', title_align='center',width=85)
        print(painel_inicial)
        opcao = validar.valida_int('          --→  ', 1, 4)
        console.clear()
        console.rule(style='dark_orange')

        match opcao:
            case 1:
                while True:
                    new_user = console.input('Digite o nome do novo usuário:\n → ').title()
                    for u in dados:
                        if u['nome'] == new_user:
                            console.clear()
                            console.rule(style='dark_orange')
                            print(f'[yellow]Usuário [cyan]"{new_user}"[/] já cadastrado![/]\n'
                                  'Digite outro nome ou exclua-o do registro de usuários.')
                            console.rule(style='dark_orange')
                            break
                    else:
                        break
                oparquivo.escreva_arq(arquivo,cadastrar_usuario(arquivo,new_user), sobrescreva=True)
            case 2:
                while True:
                    console.clear()
                    painel_listar = Panel('        Como deseja ordenar os usuários:\n[bright_blue]'
                           '            [ 1 ] - POR ID\n[yellow]'
                           '            [ 2 ] - POR NOME\n[red]'
                           '            [ 3 ] - VOLTAR',width=85)
                    print(painel_listar)
                    filtro = ''
                    match validar.valida_int(' → ',1,3):
                        case 1:
                            filtro = 'id'
                        case 2:
                            filtro = 'nome'
                        case 3:
                            break
                    console.clear()
                    tabelas.tabela_pesquisa(arquivo, filtro= cast(Literal['id', 'nome'], filtro))
            case 3:
                console.clear()
                dados = oparquivo.ler_arq(arquivo)
                while True:
                    painel_gerenciar = Panel('        Informe o método de busca:\n[bright_blue]'
                                             '            [ 1 ] - POR ID\n[yellow]'
                                             '            [ 2 ] - POR NOME\n[purple]'
                                             '            [ 3 ] - POR APELIDO\n[red]'
                                             '            [ 4 ] - VOLTAR',width=85)
                    print(painel_gerenciar)
                    k = 'nome'
                    localizador = ''
                    gerenciar = validar.valida_int(' → ',1,4)
                    match gerenciar:
                        case 1:
                            k = 'id'
                            localizador = validar.valida_int('Digite o [bright_blue]ID[/] do usuário:\n → ')
                        case 2:
                            k = 'nome'
                            localizador = console.input('Digite o [yellow]NOME[/] do usuário:\n → ')
                        case 3:
                            k = 'apelido'
                            localizador = console.input('Digite um [purple]APELIDO[/] do usuário:\n → ')
                        case 4:
                            break
                    console.clear()
                    show_user = sistema.localizar_usuario(dados,localizador=localizador,metodo=cast(Literal['id','nome','apelido'],k))
                    if show_user is None:
                        print('[red]USUÁRIO NÃO ENCONTRADO. VERIFIQUE MAIÚSCULAS E MINÚSCULAS!')
                    else:
                        while True:
                            tabelas.tabela_user(show_user)
                            opc = validar.valida_int('          [bright_green][ 1 ] - ACRESCENTAR APELIDOS\n'
                                                     '          [purple][ 2 ] - EXCLUIR APELIDOS\n'
                                                     '          [bright_blue][ 3 ] - VISUALIZAR HISTÓRICO\n'
                                                     '          [red][ 4 ] - EXCLUIR USUÁRIO\n'
                                                     '          [yellow][ 5 ] - VOLTAR\n[default] → ',1,5)
                            console.clear()
                            match opc:
                                case 1:
                                    show_user['apelidos'].append(console.input('Insira o novo apelido: '))
                                    console.clear()
                                case 2:
                                    tira_ap = console.input('Insira o apelido a ser removido: ')
                                    if tira_ap in show_user['apelidos']:
                                        show_user['apelidos'].remove(tira_ap)
                                        console.clear()
                                    else:
                                        console.clear()
                                        print('Apelido não identificado!')
                                case 3:
                                    tabelas.tabela_historico(show_user)
                                    console.clear()
                                case 4:
                                    painel_excluir = Panel(
                                        '-----[red]VOCÊ TEM CERTEZA QUE DESEJA EXCLUIR O USUÁRIO?-----'
                                        '\n-TODO O HISTÓRICO/APELIDOS DESSE USUÁRIO SERÃO PERDIDOS-'
                                        '\n----A AÇÃO NÃO PODERÁ SER DESFEITA. EXCLUIR USUÁRIO?----',
                                        width=60, title='[underline bright_white]!!! ATENÇÃO !!!', style='red')
                                    print(painel_excluir)
                                    if validar.valida_sn(' [ S / N ]\n → '):
                                        for cont, u in enumerate(dados):
                                            if u['id'] == show_user['id']:
                                                del dados[cont]
                                                break
                                        else:
                                            print('ERRO AO DELETAR, USUÁRIO NÃO ENCONTRADO!')
                                        oparquivo.escreva_arq(arquivo,dados,ext='json',sobrescreva=True)
                                        console.clear()
                                        print('[red]USUÁRIO EXCLUÍDO COM SUCESSO')
                                        break
                                    else:
                                        console.clear()
                                case 5:
                                    oparquivo.escreva_arq(arquivo, dados, ext='json', sobrescreva=True)
                                    console.clear()
                                    break
                        if opc == 4:
                            break
            case _:
                break
