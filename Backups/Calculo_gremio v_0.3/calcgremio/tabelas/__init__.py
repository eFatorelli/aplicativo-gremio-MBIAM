from rich.table import Table
from rich.console import Console

console = Console()

def tabela_inicial():
    from calcgremio.validar import valida_int
    tabela = Table(show_header=True)

    tabela.add_column(header='GRÊMIO DOS TENENTES MBIAM'.center(75),header_style='cyan' ,width=85,justify="left")
    tabela.add_row('        Selecione uma das opções:')
    tabela.add_row('            [ 1 ] - CÁLCULO DE FICHAS',style='bright_cyan')
    tabela.add_row('            [ 2 ] - VALIDAR PAGAMENTO (ÚLTIMA FICHA)',style='bright_green')
    tabela.add_row('            [ 3 ] - CONSULTA RÁPIDA',style='bright_blue')
    tabela.add_row('            [ 4 ] - EDITAR/DELETAR FICHAS',style='dark_orange')
    tabela.add_row('            [ 5 ] - ENCERRAR PROGRAMA',style='bright_red')
    console.print(tabela)
    opcao = valida_int('          --→  ',1,5)
    console.clear()
    return opcao


def tabela_calculos(dicionario, titulo='TABELA', *, pesquisa = False):
    tabela = Table(title=titulo,row_styles=['on default','on grey3'],show_footer=True)

    total=sum(obj.valficha for obj in dicionario.values())

    tabela.add_column('Nome',justify='left',style='cyan',width=30,footer='Total:')
    tabela.add_column('Valor',justify='right',style='green',width=10,footer=f'R$ {total:.2f}',footer_style='dark_green')
    if pesquisa:
        tabela.add_column('Pago?',justify='center',width=5)

    for nome,obj in sorted(dicionario.items()):
        if not pesquisa:
            tabela.add_row(f'{nome}',f'R$ {obj.valficha:.2f}')
        if pesquisa:
            tabela.add_row(f'{nome}',f'R$ {obj.valficha:.2f}','[bright_white on bright_green]SIM[/]' if obj.pagou else '[black on bright_red]NÃO[/]')


    console.print(tabela)

