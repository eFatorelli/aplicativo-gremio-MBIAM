from calcgremio import menus, tabelas, oparquivo
from rich.traceback import install
from rich import print
from pathlib import *

DIR_BASE = Path(__file__).resolve().parent
ARQ_USERS = DIR_BASE / 'data' / 'users.json'

try:
    oparquivo.arq_existe(ARQ_USERS, criar=True)
    if not oparquivo.ler_arq(ARQ_USERS):
        oparquivo.escreva_arq(ARQ_USERS, [], sobrescreva=True)
    while True:
        install()
        match menus.menu_inicial(4):
            case 1:
                menus.menu_calc(ARQ_USERS)
                tabelas.console.clear()
            case 2:
                menus.menu_pesquisa(ARQ_USERS)
                tabelas.console.clear()
            case 3:
                menus.menu_usuario(ARQ_USERS)
                tabelas.console.clear()
            case _:
                break

except KeyboardInterrupt:
    print(f'\n\n{"USUÁRIO FINALIZOU O PROGRAMA":^85}')

except Exception as e:
    print('HOUVE UM ERRO INESPERADO NO PROGRAMA:', end=' ')
    print(e.__class__)
    input('Digite ENTER para encerrar o programa.')

finally:
    print(f'\n\n[bold red]{" PROGRAMA ENCERRADO ":=^85}[/]')
    #menus.sleep(2)