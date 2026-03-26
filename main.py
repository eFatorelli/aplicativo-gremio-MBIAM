import sys
from calcgremio import menus, oparquivo
from rich.traceback import install
from rich import print
from pathlib import Path
from rich.console import Console
from time import sleep



if getattr(sys, 'frozen', False):
    DIR_BASE = Path(sys.executable).parent
else:
    DIR_BASE = Path(__file__).resolve().parent
ARQ_USERS = DIR_BASE / 'data' / 'users.json'
ARQ_DEFINICOES = DIR_BASE / 'data' / 'definicoes.json'

try:
    console = Console()
    ARQ_USERS.touch(exist_ok=True)
    ARQ_DEFINICOES.touch(exist_ok=True)
    if not oparquivo.ler_arq(ARQ_USERS):
        oparquivo.escreva_arq(ARQ_USERS, [], sobrescreva=True)
    if not oparquivo.ler_arq(ARQ_DEFINICOES):
        print('ERRO AO LER ARQ_DEFINICOES. RESETANDO DEFINIÇÕES DE COBRANÇA.')
        oparquivo.escreva_arq(ARQ_DEFINICOES, {'mensalidade': 30}, sobrescreva= True)
    while True:
        install()
        match menus.menu_inicial(6):
            case 1:
                menus.menu_calc(ARQ_USERS, ARQ_DEFINICOES)
                console.clear()
            case 2:
                menus.menu_pesquisa(ARQ_USERS)
                console.clear()
            case 3:
                menus.menu_definicoes(ARQ_DEFINICOES)
                console.clear()
            case 4:
                menus.menu_usuario(ARQ_USERS)
                console.clear()
            case 5:
                menus.menu_msg(ARQ_USERS, ARQ_DEFINICOES)
                console.clear()
            case _:
                break

except KeyboardInterrupt:
    print(f'\n\n{"USUÁRIO FINALIZOU O PROGRAMA":^85}')

except Exception as e:
    print('HOUVE UM ERRO INESPERADO NO PROGRAMA:', end=' ')
    print(e.__class__)
    print(e)
    input('Digite ENTER para encerrar o programa.')

finally:
    print(f'\n\n[bold red]{" PROGRAMA ENCERRADO ":=^85}[/]')
    sleep(2)