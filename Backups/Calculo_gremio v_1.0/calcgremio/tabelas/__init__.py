from typing import Literal

from rich.table import Table
from rich.console import Console

from calcgremio.oparquivo import ler_arq
from calcgremio.validar import nomemes

console = Console()


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

def tabela_cadastro(id, nome, *apelidos):
    lista_ap = 'Apelido não cadastrado!'
    if len(*apelidos) > 0:
        for cont, a in enumerate(*apelidos):
            if cont == 0:
                lista_ap = a
            else:
                lista_ap = ' / '.join([lista_ap,a])

    tabela = Table(title='USUÁRIO CADASTRADO COM SUCESSO!',title_style='green',
                   show_header=False,row_styles=['on default','on grey3'])
    tabela.add_column(width=15, style= 'bright_yellow',justify="right")
    tabela.add_column(width=70, style= 'bright_blue')
    tabela.add_row('ID',str(id))
    tabela.add_row('NOME', nome)
    tabela.add_row('APELIDOS',str(lista_ap))

    console.print(tabela)


def tabela_pesquisa(arquivo, *, filtro: Literal['id', 'nome'] = 'id'):
    from calcgremio.oparquivo import ler_arq
    dados = ler_arq(arquivo, ext='json')
    tabela = Table(title='LISTA DE USUÁRIOS',title_style='dark_orange',
                   show_header=False,row_styles=['on default','on grey3'])
    tabela.add_column(width=15, style= 'bright_yellow',justify="right")
    tabela.add_column(width=70, style= 'bright_blue')
    d_org = sorted(dados, key= lambda u: u[filtro])
    for user in d_org:
        lista_ap = ' / '.join(user['apelidos'])
        tabela.add_row('ID',str(user['id']))
        tabela.add_row('NOME', user['nome'])
        tabela.add_row('APELIDOS',str(lista_ap))
        tabela.add_row('')
        tabela.add_row('')

    console.print(tabela)
    console.input('Pressione [green]ENTER[/] para continuar.\n')


def tabela_user(usuario):
    tabela = Table(title='DADOS DO USUÁRIO', title_style='dark_orange',
                   show_header=False, row_styles=['on default', 'on grey3'])
    tabela.add_column(width=15, style='bright_yellow', justify="right")
    tabela.add_column(width=70, style='bright_blue')

    lista_ap = ' / '.join(usuario['apelidos'])
    tabela.add_row('ID', str(usuario['id']))
    tabela.add_row('NOME', usuario['nome'])
    tabela.add_row('APELIDOS', str(lista_ap))

    console.print(tabela)


def tabela_historico(usuario):
    tabela = Table(title=f'HISTÓRICO DE "{usuario['nome']}"', title_style='dark_orange',
                   show_header=False, row_styles=['on default', 'on grey3'])
    tabela.add_column(width=8, style='bright_yellow', justify="right")
    tabela.add_column(width=20, style='bright_blue')
    tabela.add_column(width=10, style='bright_green')

    for data, ficha in usuario['historico'].items():
        tabela.add_row(f'{nomemes(int(data[-2:])).title()} {data[:4]}', f'Valor final:\nMensalidade:\nAr Condicionado:\nPagou:',
                                                                                    f'R$ {ficha['val_final']:.2f}\n'
                                                                                    f'{'[bright_white on green]Pagou[/]' if ficha['mensalidade'] else '[black on red]Não Pagou[/]'}\n'
                                                                                    f'{'[bright_white on green]Pagou[/]' if ficha['ar_cond'] else '[black on red]Não Pagou[/]'}\n'
                                                                                    f'{'[bright_white on green]Pagou[/]' if ficha['pagou'] else '[black on red]Não Pagou[/]'}')
        tabela.add_row('')
    console.print(tabela)
    console.input('Pressione [green]ENTER[/] para continuar.')