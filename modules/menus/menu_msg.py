from .common import *
import pyperclip

def menu_msg(arquivo, arquivo_def):
    dados = oparquivo.ler_arq(arquivo)
    definicoes = oparquivo.ler_arq(arquivo_def)

    tela_ini = Panel(f'~~ [underline]MENSAGEM DE COBRANÇA[/] ~~'.center(88),
                     title='[bold cyan]GRÊMIO DOS TENENTES MBIAM', width=80,
                     style='purple', border_style='default')

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
        msg_cob = validar.valida_int(f'Selecione para qual cobrança a mensagem será emitida:\n'
                                      f'  [green][ 1 ] - COBRANÇA MAIS RECENTE - {validar.nomemes(mes).title()} de {ano}[/];\n'
                                      f'  [yellow][ 2 ] - VISUALIZAR OUTRA COBRANÇA[/]\n'
                                      f'  [purple][ 3 ] - RETORNAR AO MENU PRINCIPAL[/]\n → ', 1, 3)
        console.clear()
        match msg_cob:
            case 1:
                if ano == 0 or mes == 0:
                    console.clear()
                    print('Não foi possível localizar a última cobrança!')
                    continue
            case 2:
                ano = validar.valida_int('Digite o [cyan]ANO[/] do qual deseja consultar a cobrança: ', 2026)
                mes = validar.valida_int('Digite o [cyan]NÚMERO DO MÊS[/] do qual deseja consultar a cobrança: ', 1, 12)
            case _:
                return None

        if not any(f'{ano}-{mes:0>2}' in user['historico'] for user in dados):
            console.rule(style='bright_white')
            print('[yellow]Não foi encontrada nenhuma cobrança com essa data![/]\n'
                  'Por favor, digite outra data.')
            console.rule(style='bright_white')
            continue
        else:
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

            list_conteudo = list()
            for user in sorted(dados, key= lambda u: u['nome']):
                pend = 0
                if f'{ano}-{mes:0>2}' in user['historico']:
                    for cob, ficha in user['historico'].items():
                        if cob != f'{ano}-{mes:0>2}' and not ficha['pagou']:
                            pend += ficha['val_final']
                    if pend == 0:
                        list_conteudo.append(f'{user['nome']:<20}'
                                f'R$ {user['historico'][f'{ano}-{mes:0>2}']['val_final']:.2f}\n')
                    else:
                        list_conteudo.append(f'{user['nome']+'*':<20}'
                                             f'R$ {user['historico'][f'{ano}-{mes:0>2}']['val_final']+pend:.2f}\n')

            conteudo = ''.join(list_conteudo)
        try:
            cabecalho = definicoes['cabecalho cobranca']
        except KeyError,TypeError:
            cabecalho = ''

        print('\n')
        console.clear()
        console.rule(style='bright_white')
        while True:
            mensagem = (f'*Cobrança de {validar.nomemes(mes).upper()}*\n\n' + cabecalho +
                        f'\nMensalidade: R$ {definicoes['mensalidade']:.2f}\n\n' +
                        f'Chave pix: {definicoes['banco']['chave']}\n'
                        f'({definicoes['banco']['tipo']} - {definicoes['banco']['dono']})\n\n'
                        + conteudo)
            painel_msg = Panel(mensagem, border_style='green')
            print(painel_msg)
            opc = validar.valida_int('    Selecione uma opção:\n'
                                     '        [green][ 1 ] - [underline bold]COPIAR[/] MENSAGEM PARA ÁREA DE TRANSFERÊNCIA\n'
                                     '        [yellow][ 2 ] - PESQUISAR OUTRO MÊS\n'
                                     '        [cyan][ 3 ] - MODIFICAR MENSAGEM CABECALHO\n'
                                     '        [purple][ 4 ] - VOLTAR PARA O MENU PRINCIPAL\n'
                                     '        [default]      → ',1,4)
            match opc:
                case 1:
                    pyperclip.copy(str(mensagem))
                    console.clear()
                    console.rule(style='green')
                    print('Copiado para [green]ÁREA DE TRANSFERÊNCIA[/]!'.center(90))
                    console.rule(style='green')
                    sleep(1)
                    console.clear()
                case 2:
                    console.clear()
                    break
                case 3:
                    texto = console.input('Digite um novo cabeçalho para a mensagem. Para cancelar, digite "CANCELAR".\n'
                                              'ATENÇÃO: Colar textos com quebra de linha resultará em ERRO\n  → ')
                    if (texto.lower() == 'cancelar' or not validar.valida_sn(
                            f'[yellow]Tem certeza de que quer reescrever a mensagem para \n'
                            f'[default underline]"{texto}"[/]?[/] [ S / N ]\n → ',n_auto= False)):
                        continue

                    cabecalho = texto
                    definicoes['cabecalho cobranca'] = cabecalho
                    oparquivo.escreva_arq(arquivo_def, definicoes, sobrescreva=True)
                    console.clear()
                case _:
                    return None