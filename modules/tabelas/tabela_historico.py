from .common import *

def tabela_historico(usuario):
    tabela = Table(title=f'HISTÓRICO DE "{usuario['nome']}"', title_style='dark_orange',
                   show_header=False, row_styles=['on default', 'on grey3'])
    tabela.add_column(width=8, style='bright_yellow', justify="right")
    tabela.add_column(width=20, style='bright_blue')
    tabela.add_column(width=20, style='bright_green')

    for data, ficha in usuario['historico'].items():
        cob = ['Valor final:','Mensalidade:']
        pag = [f'R$ {ficha['val_final']:.2f}',f'{'[bright_white on green]Cobrado[/]' if ficha['mensalidade'] else '[black on red]Não Cobrado[/]'}']
        if 'extra' in ficha.keys():
            for k,v in ficha['extra'].items():
                cob.append(f'{str(k).capitalize()}:')
                pag.append(f'{'[bright_white on green]Cobrado[/]' if v[1] else '[black on red]Não Cobrado[/]'}')
        cob.append('Pagou:')
        pag.append(f'{'[bright_white on green]Pagou[/]' if ficha['pagou'] else '[black on red]Não Pagou[/]'}')
        cob = '\n'.join(cob)
        pag = '\n'.join(pag)

        tabela.add_row(f'{nomemes(int(data[-2:])).title()} {data[:4]}', cob, pag)
        tabela.add_row('')
    console.print(tabela)
    console.input('Pressione [green]ENTER[/] para continuar.')
