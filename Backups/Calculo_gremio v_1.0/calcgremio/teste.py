from calcgremio.sistema import cadastrar_usuario
from calcgremio.tabelas import *
from classes import Usuario
import json
from rich.traceback import install
from oparquivo import *
from sistema import *
from rich.table import Table
from rich.console import Console
from rich.panel import Panel

install()

arq = r'C:\Users\enzof\PycharmProjects\gremio_teste\data\users.json'
ano = 2026
mes = 2
dados = ler_arq(arq, ext='json')

painel_excluir = Panel('-----[red]VOCÊ TEM CERTEZA QUE DESEJA EXCLUIR O USUÁRIO?-----'
                       '\n-TODO O HISTÓRICO/APELIDOS DESSE USUÁRIO SERÃO PERDIDOS-'
                       '\n----A AÇÃO NÃO PODERÁ SER DESFEITA. EXCLUIR USUÁRIO?----',
                       width=60,title='[underline bright_white]!!! ATENÇÃO !!!',style='red')
print(painel_excluir)
