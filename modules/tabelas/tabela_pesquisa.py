from .common import *

def tabela_pesquisa(arquivo, *, filtro: Literal['id', 'nome'] = 'id'):
    dados = ler_arq(arquivo, ext='json')
    tabela = Table(title='LISTA DE USUÁRIOS',title_style='dark_orange',
                   show_header=False,row_styles=['on default','on grey3'])
    tabela.add_column(width=15, style= 'bright_yellow',justify="right")
    tabela.add_column(width=70, style= 'bright_blue')
    if filtro == 'id':
        d_org = sorted(dados, key= lambda u: u['id'])
    else:
        d_org = sorted(dados, key= lambda u: u['nome'].lower())

    for user in d_org:
        lista_ap = ' / '.join(user['apelidos'])
        tabela.add_row('ID',str(user['id']))
        tabela.add_row('NOME', user['nome'])
        tabela.add_row('APELIDOS',str(lista_ap))
        tabela.add_row('')
        tabela.add_row('')

    console.print(tabela)
    console.input('Pressione [green]ENTER[/] para continuar.\n')