from calcgremio import funcoes, menus, tabelas, oparquivo
from rich.traceback import install
from rich import print

arquivo = r'Fichas_Gremio\menu.txt'
try:
    tabelas.console.clear()
    while True:
        install()
        match tabelas.tabela_inicial():
            case 1:
                ult_ficha = menus.menu_calc()
                oparquivo.arq_existe(arquivo,criar=True)
                oparquivo.escreva_arq(arquivo, ult_ficha,sobrescreva=True)
                tabelas.console.clear()
            case 2:
                try:
                    ult_ficha = oparquivo.ler_arq(arquivo,linhas=False)
                    print(f'Acessando ficha em "[italic]{ult_ficha}[/]": ')
                    menus.menu_validar(ult_ficha)
                    tabelas.console.clear()
                except Exception as e:
                    print('[red]ERRO[/] - Você precisa Calcular uma ficha primeiro!', e.__class__)
            case 3:
                menus.menu_pesquisa()
                tabelas.console.clear()
            case 4:
                print('EM IMPLEMENTAÇÃO')
                tabelas.console.clear()
            case _:
                break

except KeyboardInterrupt:
    print(f'\n\n{"USUÁRIO FINALIZOU O PROGRAMA":^85}')
finally:
    print(f'\n\n[bold red]{" PROGRAMA ENCERRADO ":=^85}[/]')
    #funcoes.sleep(2)