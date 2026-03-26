from .common import *

def menu_definicoes(arquivo_def):
    tela_ini = Panel(f'~~ [underline]DEFINIÇÕES DE COBRANÇA[/] ~~'.center(89),
                     title='[bold cyan]GRÊMIO DOS TENENTES MBIAM', width=80,
                     style='bright_yellow', border_style='default')
    definicoes = oparquivo.ler_arq(arquivo_def)
    print(tela_ini)
    while True:
        tabelas.tabela_definicoes(definicoes)
        opcao = validar.valida_int(f'    Digite uma opção:\n'
                                   f'       [blue][ 1 ] - ALTERAR MENSALIDADE\n'
                                   f'       [yellow][ 2 ] - ADICIONAR COBRANÇA RECORRENTE\n'
                                   f'       [red][ 3 ] - REMOVER COBRANÇA RECORRENTE\n'
                                   f'       [green][ 4 ] - ALTERAR PIX PARA PAGAMENTO\n'
                                   f'       [purple][ 5 ] - VOLTAR AO MENU PRINCIPAL\n '
                                   f'           [default] → ', 1, 5)
        match opcao:
            case 1:
                nova_mensalidade = validar.valida_float('Digite um novo valor pra mensalidade:\n → R$ ')
                definicoes['mensalidade'] = nova_mensalidade
                console.clear()
                print(f'[bright_green]Mensalidade redefinida para R$ {nova_mensalidade:.2f}.')
            case 2:
                while True:
                    cobranca = console.input('Digite o título da nova cobrança:\n → ').lower()
                    if cobranca in definicoes['extra']:
                        print(f'[yellow]A cobrança de título "{cobranca.capitalize()}" já existe![/] Por favor, digite outro título.')
                    else:
                        break
                valor = validar.valida_float(f'Digite o valor de "{cobranca.capitalize()}":\n → R$ ')
                parcelas = validar.valida_int(f'O pagamento será efetuado em quantas parcelas de R$ {valor:.2f}?\n'
                                              f'(Caso seja uma cobrança recorrente sem prazo definido, digite [underline bright_yellow]0 (zero)[/].',
                                              0,erro='[red]Digite um número inteiro ou 0 (zero) para cobrança sem prazo!')
                try:
                    if 'extra' not in definicoes:
                        definicoes['extra'] = {}
                    definicoes['extra'][cobranca] = (valor, parcelas)
                except Exception as e:
                    print(f'[red]Erro ao definir cobrança: {e.__class__, e}')
                else:
                    print('[bright_green]Cobrança definida com sucesso!')
                finally:
                    sleep(1)
                    console.clear()
            case 3:
                del_cobranca = console.input('Digite o título da cobrança a ser deletada:\n → ').lower()
                if del_cobranca in definicoes['extra']:
                    del definicoes['extra'][del_cobranca]
                    print(f'[bright_green]{del_cobranca.capitalize()} deletada com sucesso!')
                else:
                    print('[red]Não foi encontrada nenhuma cobrança com esse título!')
                sleep(1)
                console.clear()
            case 4:
                chave = console.input('Digite a [bold green]chave PIX[/] para receber os pagamentos:\n → ')
                console.rule(style='bright_white')
                ch = ('Celular', 'CPF', 'email', 'Chave aleatória')
                tipo_chave = validar.valida_int('Qual o tipo da chave?\n'
                                                '   [ 1 ] - CELULAR\n'
                                                '   [ 2 ] - CPF\n'
                                                '   [ 3 ] - email\n'
                                                '   [ 4 ] - aleatória\n → ',1,4)
                tipo_chave = ch[tipo_chave-1]
                console.rule(style='bright_white')
                dono_conta = console.input('Digite o nome completo do dono da conta:\n → ')
                definicoes['banco'] = {'chave': chave, 'tipo' : tipo_chave,'dono': dono_conta}
                console.clear()
            case _:
                oparquivo.escreva_arq(arquivo_def,definicoes,sobrescreva=True)
                return None