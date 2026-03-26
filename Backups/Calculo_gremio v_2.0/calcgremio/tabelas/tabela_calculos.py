from .common import *

def tabela_calculos(arquivo, ano, mes, titulo='TABELA', *, pesquisa = False):
    dados = ler_arq(arquivo)
    tabela = Table(title=titulo,row_styles=['on default','on grey23'],show_footer=True)

    total = 0
    for user in sorted(dados, key=lambda u: u['nome']):
        if f'{ano}-{mes:0>2}' in user['historico']:
            total += user['historico'][f'{ano}-{mes:0>2}']['val_final']


    if pesquisa:
        tabela.add_column('ID',justify="right",style='yellow',width=3)
    tabela.add_column('Nome',justify='left',style='cyan',width=50,footer='Arrecadação do mês (sem contar PENDÊNCIAS):')
    tabela.add_column('Valor',justify='right',style='green',width=20,footer=f'R$ {total:.2f}',footer_style='dark_green')

    if pesquisa:
        tabela.add_column('Pago?',justify='center',width=5)
        for user in sorted(dados, key=lambda u: u['nome']):
            if f'{ano}-{mes:0>2}' in user['historico']:
                val_atraso = 0
                for m, i in user['historico'].items():
                    if m != f'{ano}-{mes:0>2}' and not i['pagou']:
                        val_atraso += i['val_final']
                tabela.add_row(f'{user['id']}',f'{user['nome']}',
                               f'R$ {user['historico'][f'{ano}-{mes:0>2}']['val_final']:.2f}',
                               '[bright_white on bright_green]SIM[/]' if user['historico'][f'{ano}-{mes:0>2}']['pagou']
                               else '[black on bright_red]NÃO[/]')
    else:
        for user in sorted(dados, key=lambda u: u['nome']):
            #================ Cálculo do valor atrasado ===================
            mes_atraso = list()
            val_atraso = 0
            for m, i in user['historico'].items():
                if m != f'{ano}-{mes:0>2}' and not i['pagou']:
                    mes_atraso.append(f'{nomemes(int(m[-2:]))[:3].upper()} {m[:4]}')
                    val_atraso += i['val_final']
            mes_atraso = '\n[black on yellow]Meses pendentes:[/] '+', '.join(mes_atraso) if val_atraso else ''
            pendencia = f'\n[black on red]+ R$ {val_atraso:.2f} PENDENTE[/]' if val_atraso else ''
            #==============================================================

            if user['historico'].get(f'{ano}-{mes:0>2}'):
                tabela.add_row(f'{user['nome']}'+f'{mes_atraso}', f'R$ {f' {user['historico'][f'{ano}-{mes:0>2}']['val_final']:.2f}'+
                               pendencia: >7}')

    console.print(tabela)

