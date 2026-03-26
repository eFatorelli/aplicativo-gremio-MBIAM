from .common import *

def tabela_definicoes(dict_definicoes):
    try:
        tabela_pix = Table(row_styles=['on default', 'on grey23'], show_header=False)
        tabela_pix.add_column(style='green', width=30)
        tabela_pix.add_column(style='cyan', width=52)

        tabela_pix.add_row('Chave Pix:', dict_definicoes['banco']['chave'])
        tabela_pix.add_row('Tipo da chave:', dict_definicoes['banco']['tipo'])
        tabela_pix.add_row('Nome:', dict_definicoes['banco']['dono'])

        console.print(tabela_pix)
    except:
        pass

    try:
        tabela_cobra = Table(row_styles= ['on default','on grey23'], show_header=False)
        tabela_cobra.add_column(style='green', width=40)
        tabela_cobra.add_column(style='cyan', width=20)
        tabela_cobra.add_column(style='yellow', width=32)

        tabela_cobra.add_row('Mensalidade:', f'R$ {dict_definicoes['mensalidade']:.2f}','Cobrança Padrão')
        for k, v in dict_definicoes['extra'].items():
            tabela_cobra.add_row(f'{str(k).capitalize()}:',f'R$ {v[0]:.2f}',f'{v[1]} parcelas' if v[1]>0 else 'Cobrança Recorrente')

        console.print(tabela_cobra)
    except Exception as e:
        print('Erro ao exibir tabela:', e.__class__, e)
