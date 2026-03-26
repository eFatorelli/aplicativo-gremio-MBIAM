from .common import *

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
