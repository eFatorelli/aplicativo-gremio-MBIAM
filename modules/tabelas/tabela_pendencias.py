from .common import *

def tabela_pendencias(dict_pendencias):
    tabela = Table(title= '-- PENDÊNCIAS --', title_style= 'bold dark_red', row_styles= ['on default','on grey23'])
    tabela.add_column('Nome', justify='left', style='cyan', width=20)
    tabela.add_column('Pendências', justify='left', style='yellow', width=50)

    for user, data in sorted(dict_pendencias.items()):
        data_certa = [f'{nomemes(int(x[-2:])).upper()[:3]} {x[:4]}' for x in sorted(data)]
        tabela.add_row(user,'[bright_white] / [/]'.join(data_certa))

    console.print(tabela)
    console.input('Pressione [green]ENTER[/] para continuar.')
