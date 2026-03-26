import menus, tabelas
from rich.traceback import install
from rich import print

arquivo = r'C:\Users\enzof\PycharmProjects\gremio_teste\data\users.json'

try:
    tabelas.console.clear()
    while True:
        install()
        match menus.menu_inicial():
            case 1:
                menus.menu_calc(arquivo)
                tabelas.console.clear()
            case 2:
                menus.menu_pesquisa(arquivo)
                tabelas.console.clear()
            case 3:
                menus.menu_usuario(arquivo)
                tabelas.console.clear()
            case _:
                break

except KeyboardInterrupt:
    print(f'\n\n{"USUÁRIO FINALIZOU O PROGRAMA":^85}')
finally:
    print(f'\n\n[bold red]{" PROGRAMA ENCERRADO ":=^85}[/]')
    #menus.sleep(2)