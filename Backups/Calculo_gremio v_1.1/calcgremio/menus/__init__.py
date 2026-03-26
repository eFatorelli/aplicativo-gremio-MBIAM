from typing import cast, Literal
from calcgremio import oparquivo, validar, tabelas, sistema
from calcgremio.classes import Usuario
from datetime import date
from time import sleep
from rich.panel import Panel
from rich import print
from rich.console import Console

from calcgremio.oparquivo import ler_arq

console = Console()
#==================================== CÁLCULO DE FICHAS ====================================

def menu_inicial(qtde_opcoes = 4):
    painel = Panel('        Selecione uma das opções:\n[bright_cyan]'
                   '            [ 1 ] - CÁLCULO DE FICHAS\n[bright_green]'
                   '            [ 2 ] - CONSULTAR/VALIDAR FICHAS\n[dark_orange]'
                   '            [ 3 ] - GERENCIAR USUÁRIOS\n[bright_red]'
                   '            [ 4 ] - ENCERRAR PROGRAMA'
                   ,title='[cyan]GRÊMIO DOS TENENTES MBIAM', title_align='center',width=85)
    print(painel)
    opcao = validar.valida_int('          --→  ', 1, qtde_opcoes)
    console.clear()
    return opcao


def menu_calc(arquivo):
    s = qtde = qprod = opcao_ficha = duplicata = mes = 0
    meshoje = date.today().month
    ano = date.today().year
    dados = oparquivo.ler_arq(arquivo,ext='json')

    # ===== Seleção do mês da cobrança ===== (utilidades a serem implementadas)
    tela_ini = Panel(f'~~ [underline]CALCULADORA DE FICHAS[/] ~~'.center(89),
                     title='[bold cyan]GRÊMIO DOS TENENTES MBIAM', width=80,
                     style='bright_green', border_style='default',
                     subtitle=f'[bright_yellow]{date.today().day} de '
                              f'{validar.nomemes(meshoje).upper()} de {ano}')
    print(tela_ini)
    datacobra = validar.valida_int(f'Deseja realizar a cobrança para esse mês, mês anterior ou outro mês?\n'
                                  f'  [ 1 ] - Cobrança de [yellow]{validar.nomemes(meshoje).upper()} de {ano}[/];\n'
                                  f'  [ 2 ] - Cobrança de [yellow]{validar.nomemes(meshoje - 1).upper()} de {ano - 1 if meshoje - 1 < 0 else ano}[/];\n'
                                  f'  [ 3 ] - Cobrança de [yellow]outro mês[/].\n', 1, 3)
    match datacobra:
        case 1:
            mes = meshoje
        case 2:
            mes = meshoje - 1
            if mes < 1:
                ano -= 1
        case _:
            mes = validar.valida_int('Digite o [cyan]NÚMERO[/] do mês que deseja realizar a cobrança: ', 1, 12)
            anocobra = validar.valida_int(f'[yellow]{validar.nomemes(mes).upper()}[/] de qual ano?\n'
                                   f'  [ 1 ] - [bright_blue]{ano - 1}[/];\n'
                                   f'  [ 2 ] - [bright_blue]{ano}[/];\n'
                                   f'  [ 3 ] - [bright_blue]{ano + 1}.\n', 1, 3)
            match anocobra:
                case 1:
                    ano -= 1
                case 3:
                    ano += 1

    # ===== Início do loop principal e seleção do nome =====
    console.clear()
    console.rule(style='cyan')
    print(f'{f"  COBRANÇA DEFINIDA PARA O MÊS DE [bold underline purple]{validar.nomemes(mes).upper()}[/]  ":=^97}')
    user = Usuario()
    while True:
        if qprod == 0:
            while True:
                duplicata = 0
                nome = str(input('Digite o nome na ficha: ')).strip()
                if sistema.localizar_usuario(dados,nome,'nome'):
                    print(f'Nome "{nome}" localizado!')
                    user = Usuario().to_obj(sistema.localizar_usuario(dados,nome,'nome'))
                elif sistema.localizar_usuario(dados,nome,'apelido'):
                    u = sistema.localizar_usuario(dados,nome,'apelido')
                    print(f'"{nome}" localizado como APELIDO de "{u['nome']}" ')
                    user = Usuario().to_obj(u)
                else:
                    console.clear()
                    console.rule(style='bright_white')
                    cad = validar.valida_int(f'"{nome}" não foi identificado como [underline]NOME[/] ou [underline]APELIDO[/] de usuário.\n'
                                             f'Selecione uma opção:\n'
                                             f'[ 1 ] - Cadastrar {nome} como NOME;\n'
                                             f'[ 2 ] - Cadastrar {nome} como APELIDO de algum usuário;\n'
                                             f'[ 3 ] - Digitar novo nome;\n'
                                             f'[ 4 ] - RETORNAR AO MENU\n → ',1,4)
                    match cad:
                        case 1:
                            sistema.escreva_arq(arquivo,sistema.cadastrar_usuario(arquivo, nome), sobrescreva=True)
                            dados = ler_arq(arquivo)
                            console.clear()
                            user = Usuario().to_obj(sistema.localizar_usuario(dados,nome,'nome'))
                            break
                        case 2:
                            user_dict = sistema.localizar_usuario(dados,console.input('Digite o NOME do usuário: '),'nome')
                            if user_dict is not None:
                                console.clear()
                                user = Usuario().to_obj(user_dict)
                                print(f'Usuário {user.nome} localizado! Adicionando apelido e prosseguindo com a ficha.')
                                user.apelidar(nome)
                                break
                            else:
                                print('Usuário não localizado!')
                                continue
                        case 3:
                            console.clear()
                            console.rule(style='bright_white')
                            continue
                        case _:
                            return None

                # ===== Tratamento de Duplicatas

                if user.historico.get(f'{ano}-{mes:0>2}'):
                    console.rule(style='bright_white')
                    duplicata = validar.valida_int(
                        f'Já existe uma ficha com esse nome, com o valor de [green]R$ {user.ler_valor(ano, mes):.2f}[/]!\n'
                        'Deseja somar, substituir ou digitar um novo nome?\n'
                        '[bold green][ 1 ] SOMAR FICHA;\n'
                        '[bold red][ 2 ] SUBSTITUIR FICHA;\n'
                        '[bold yellow][ 3 ] DIGITAR NOVO NOME.[/][/][/]\n'
                        'Digite uma opção: ', 1, 3)
                    match duplicata:
                        case 1:
                            console.rule(style='bright_white')
                            print('As fichas de mesmo nome serão [bold green]SOMADAS.')
                        case 2:
                            console.rule(style='bright_white')
                            print('A outra ficha com mesmo nome será [bold red]SUBSTITUÍDA.')
                            user.zerar(ano, mes)
                        case 3:
                            console.clear()
                            console.rule(style='bright_white')
                            continue
                break
            user.registrar(ano, mes)

        # ===== Loop de cálculo, flag: "fim" =====
        console.rule(style='bright_white')
        print('[bold]Quando quiser finalizar o programa, '
              '[bold underline yellow] digite "FIM" na digitação de valores/quantidades.')
        produto = validar.valida_float('Digite o valor do produto: R$ ', exceto='FIM')
        if isinstance(produto,float):  # Permite calcular vários produtos enquanto o Flag não é digitado.
            qprod += 1  # Impede que o programa peça o nome após cada produto.
            qtde = validar.valida_int(f'Valor do produto: R$ {produto:.2f}. Informe a quantidade: ', exceto='FIM')
            if isinstance(qtde,int):
                s += produto * qtde
                print(f'Valor até o momento: [underline yellow]R$ {s:.2f}')
                sleep(0.3)
        if (isinstance(produto,str) and produto.upper() == 'FIM') or (
                isinstance(qtde, str) and qtde.upper() == 'FIM'):  # Caso seja digitado o Flag:
            console.rule(style='bright_white')

            # ===== Acréscimo de Mensalidade =====

            mensal = 30
            if validar.valida_sn(f'[cyan]Deseja acrescentar a mensalidade de R$ {mensal:.2f}?\n[ S / N ] → '):
                if duplicata == 1 and user.ler_mensalidade(ano,mes):
                    if validar.valida_sn(
                            f'[yellow]A mensalidade de [underline]{user.nome}[/underline] '
                            f'já foi cobrada. Deseja cobrar novamente?\n[ S / N ] → [/]'):
                        user.cobrar_mensal(ano, mes)
                        s += 30
                else:
                    user.cobrar_mensal(ano, mes)
                    s += 30
            console.rule(style='bright_white')

            # ===== Acréscimo da parcela do Ar Condicionado =====

            ar = 42
            if validar.valida_sn(
                    f'[cyan]Deseja acrescentar a parcela do ar condicionado de R$ {ar:.2f}?\n[ S / N ] → [/]'):
                if duplicata == 1 and user.ler_arcond(ano,mes):
                    if validar.valida_sn(
                            f'[yellow]A parcela do ar condicionado já foi cobrada de {user.nome}. '
                            f'Deseja cobrar novamente?\n[ S / N ] → [/]'):
                        user.cobrar_arcond(ano, mes)
                        s += 42
                else:
                    user.cobrar_arcond(ano, mes)
                    s += 42
            console.rule(style='bright_white')


            # ===== Identificação da mensalidade atrasada =====
            cal = sistema.idt_caloteiro(user)
            if cal:
                d_calot, v_calot = cal
                print(f'[yellow]AVISO:[/] Foram identificadas cobranças não pagas de {d_calot} somando o valor de R$ {v_calot:.2f}.\n'
                      f'Confira mais detalhes no menu "VALIDAR PAGAMENTO".')

            # ===== Valor final =====

            console.clear()
            print(f'Valor final para [bold blue]{user.nome}[/]: [green]R$ {s:.2f}')
            if duplicata == 1:
                print(f'Somado ao valor de [bold yellow]R$ {user.ler_valor(ano, mes):.2f}[/] da outra ficha,'
                      f' o novo valor é de [bold green]R$ {user.ler_valor(ano, mes) + s:.2f}[/].')
            user.cobrar_valor(s, ano, mes)
            oparquivo.escreva_arq(arquivo,sistema.atualizar_ficha(arquivo,user),sobrescreva=True)


            # ===== Menu de seleção =====
            while True:
                opcao_ficha = validar.valida_int('[bold]Selecione uma opção abaixo:\n'
                                           '[cyan][ 1 ] - NOVA FICHA\n'
                                           '[yellow][ 2 ] - REFAZER ESTA FICHA\n'
                                           '[red][ 3 ] - EXCLUIR ESTA FICHA\n'
                                           '[purple][ 4 ] - FINALIZAR CÁLCULO\n', 1, 4)
                console.rule(style='bright_white')
                match opcao_ficha:
                    case 1:
                        qprod = 0  # Permite inserir um novo nome ao começar a nova ficha
                        s = 0
                    case 2:
                        user.zerar(ano, mes)
                        s = 0  # Reseta o valor da soma pro próximo loop;
                        qprod = 1
                    case 3:
                        if user.apagar_mes(ano,mes):
                            print('[green]FICHA APAGADA COM SUCESSO![/]')
                        else:
                            print('[yellow]A FICHA JA FOI APAGADA![/]')
                        s = 0  # Reseta o valor da soma pro próximo loop;
                        qprod = 0
                        continue
                break
            console.clear()
        if opcao_ficha == 4:
            break

    # ===== Tabela de cobrança =====

    console.clear()
    tabelas.tabela_calculos(arquivo, ano, mes,f'TABELA DE COBRANÇA - {validar.nomemes(mes).upper()}')
    console.rule(style='bright_white')
    console.input('Digite [green]ENTER[/] para continuar.')
    return None

#====================================CONSULTA/EDIÇÃO DE FICHAS====================================

                ####ADICIONAR OPÇÃO DE ÚLTIMA FICHA


def menu_pesquisa(arquivo):
    dados = oparquivo.ler_arq(arquivo)

    tela_ini = Panel(f'~~ [underline]CONSULTA DE FICHAS[/] ~~'.center(89),
                     title='[bold cyan]GRÊMIO DOS TENENTES MBIAM', width=80,
                     style='bright_green', border_style='default')
    while True:
        print(tela_ini)
        list_cob, pendencia = set(), dict()
        pend = 0
        for user in dados:
            list_mes = []
            for cob, ficha in user['historico'].items():
                list_cob.add(cob)
                if not ficha['pagou']:
                    pend += 1
                    list_mes.append(cob)
            if list_mes:
                pendencia[user['nome']] = list_mes
        list_cob = sorted(list_cob, reverse=True)
        ano = int(list_cob[0][:4]) if list_cob else 0
        mes = int(list_cob[0][-2:]) if list_cob else 0
        pesquisa = validar.valida_int(f'Selecione uma opção:\n'
                                      f'  [red][ 1 ] - IDENTIFICAR PENDÊNCIAS NO PAGAMENTO ({pend} identificadas)[/];\n'
                                      f'  [green][ 2 ] - VISUALIZAR COBRANÇA MAIS RECENTE - {validar.nomemes(mes).title()} de {ano}[/];\n'
                                      f'  [yellow][ 3 ] - VISUALIZAR OUTRA COBRANÇA[/]\n'
                                      f'  [purple][ 4 ] - RETORNAR AO MENU PRINCIPAL[/]\n → ', 1, 4)
        console.clear()
        match pesquisa:
            case 1:
                if pend:
                    tabelas.tabela_pendencias(pendencia)
                else:
                    print('Não existem pendências a serem mostradas!')
                console.clear()
                continue
            case 2:
                if ano == 0 or mes == 0:
                    console.clear()
                    print('Não foi possível localizar a última cobrança!')
                    continue
            case 3:
                ano = validar.valida_int('Digite o [cyan]ANO[/] do qual deseja consultar a cobrança: ', 2026)
                mes = validar.valida_int('Digite o [cyan]NÚMERO DO MÊS[/] do qual deseja consultar a cobrança: ', 1, 12)
            case 4:
                return None
        if not any(f'{ano}-{mes:0>2}' in user['historico'] for user in dados):
            console.rule(style='bright_white')
            print('[yellow]Não foi encontrada nenhuma cobrança com essa data![/]\n'
                  'Por favor, digite outra data.')
            console.rule(style='bright_white')
        else:
            while True:
                console.clear()
                tabelas.tabela_calculos(arquivo, ano, mes, f'COBRANÇA DE {validar.nomemes(mes).upper()} DE {ano}',
                                        pesquisa=True)
                opcao = validar.valida_int('    Digite uma opção:\n'
                                           '        [green][ 1 ] - VALIDAR PAGAMENTO\n'
                                           '        [yellow][ 2 ] - CONSULTAR OUTRO MÊS\n'
                                           '        [purple][ 3 ] - RETORNAR AO MENU PRINCIPAL\n[default] → ', 1, 3)
                match opcao:
                    case 1:
                        while True:
                            console.clear()
                            tabelas.tabela_calculos(arquivo, ano, mes,
                                                    f'COBRANÇA DE {validar.nomemes(mes).upper()} DE {ano}', pesquisa=True)
                            val_id = validar.valida_int('Digite o ID do usuário para validar seu pagamento.\n'
                                                        'Digite "0" para retornar:\n → ',0)
                            if val_id == 0:
                                break
                            elif sistema.localizar_usuario(dados,val_id,'id'):
                                user = Usuario().to_obj(sistema.localizar_usuario(dados,val_id,'id'))
                                if f'{ano}-{mes:0>2}' in user.historico:
                                    if (user.ler_pagamento(ano, mes) and
                                            validar.valida_sn('O pagamento já foi validado. Deseja marcar como não pago?\n [ S / N ] → ')):
                                        user.validar_pag(ano, mes, pagou=False)

                                    elif not user.ler_pagamento(ano, mes):
                                        user.validar_pag(ano, mes)
                                    oparquivo.escreva_arq(arquivo,sistema.atualizar_ficha(arquivo,user),sobrescreva=True)
                                else:
                                    print('Digite um ID de usuário válido!')
                            else:
                                print('Digite um ID de usuário válido!')
                    case 2:
                        console.clear()
                        break
                    case 3:
                        return None


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
                    new_user = console.input('Digite o nome do novo usuário:\n → ')
                    for u in dados:
                        if u.get('nome') == new_user:
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
                        print('[red]USUÁRIO NÃO ENCONTRADO')
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
                                case 5:
                                    oparquivo.escreva_arq(arquivo, dados, ext='json', sobrescreva=True)
                                    console.clear()
                                    break
                        if opc == 4:
                            break
            case _:
                break
        pass

