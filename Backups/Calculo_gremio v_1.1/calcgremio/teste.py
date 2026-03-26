from tabelas import *
from classes import Usuario
from validar import *
import json
from rich.traceback import install
from oparquivo import *
from sistema import *
from rich.panel import Panel
from datetime import date
from pathlib import *

install()

DIR_BASE = Path(__file__).resolve().parent.parent
ARQ_TESTE = DIR_BASE / 'data' / 'teste.json'

arq_existe(ARQ_TESTE,criar=True)
if not ler_arq(ARQ_TESTE):
    lista = list()
    escreva_arq(ARQ_TESTE, lista, sobrescreva=True)
dados = ler_arq(ARQ_TESTE)
dados.append('ada')
escreva_arq(ARQ_TESTE, dados, sobrescreva=True)
print(dados)

