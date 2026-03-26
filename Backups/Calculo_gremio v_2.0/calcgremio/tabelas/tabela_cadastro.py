from .common import *

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


