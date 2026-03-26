from .common import *

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
