from calcgremio.menus import menu_msg
from classes import Usuario
from rich.traceback import install
from sistema import *
from pathlib import *
import pyperclip
from prompt_toolkit import prompt

install()

DIR_BASE = Path(__file__).resolve().parent
ARQ_TESTE = DIR_BASE / 'data' / 'teste.json'
arq_def = r'C:\Users\enzof\PycharmProjects\gremio_teste\data\definicoes.json'
definicoes = ler_arq(arq_def)
ano = 2026
mes = 2
arq_users = r'C:\Users\enzof\PycharmProjects\gremio_teste\data\users.json'
dados = ler_arq(arq_users)
data_user = localizar_usuario(dados,'Fatorelli','nome')
user = Usuario().to_obj(data_user)


texto = '''Jonas
Brothers
é
legal'''


print(texto)
pyperclip.copy(texto)

print('Cole ou digite o novo cabeçalho. Pressione enter TRÊS VEZES para terminar:\n'
                          '[yellow]ATENÇÃO: O texto colado não pode ter mais de duas quebras de linha seguidas!\n ')
cabecalho, cont = list(), 0
while True:
    _ = console.input()
    if _ == '':
        cont += 1
        if cont > 2:
            cabecalho.pop()
            cabecalho.pop()
            break
    else:
        cont = 0
    cabecalho.append(_)

cabecalho = '\n'.join(cabecalho)
pyperclip.copy(cabecalho)

print(cabecalho)
