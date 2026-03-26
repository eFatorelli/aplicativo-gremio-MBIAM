from calcgremio import oparquivo, validar, funcoes,tabelas
from calcgremio.classes import Usuario
from datetime import date
from time import sleep
from rich.panel import Panel
from rich import print
from rich.console import Console

console = Console()

#==================================== CÁLCULO DE FICHAS ====================================

def menu_calc():
    s = qtde = qprod = opcao = duplicata = mes = 0
    nome = ''
    sobrescrever = False
    gremio = dict()
    meshoje = date.today().month
    ano = date.today().year

    # ===== Seleção do mês da cobrança ===== (utilidades a serem implementadas)
    tela_ini = Panel(f'~~ [underline]CALCULADORA DE FICHAS[/] ~~'.center(89),
                     title='[bold cyan]GRÊMIO DOS TENENTES MBIAM', width=80,
                     style='bright_green', border_style='default',
                     subtitle=f'[bright_yellow]{date.today().day} de '
                              f'{funcoes.nomemes(meshoje).upper()} de {ano}')
    print(tela_ini)
    while True:
        datacobra = validar.valida_int(f'Deseja realizar a cobrança para esse mês, mês anterior ou outro mês?\n'
                                      f'  [ 1 ] - Cobrança de [yellow]{funcoes.nomemes(meshoje).upper()} de {ano}[/];\n'
                                      f'  [ 2 ] - Cobrança de [yellow]{funcoes.nomemes(meshoje - 1).upper()} de {ano - 1 if meshoje - 1 < 0 else ano}[/];\n'
                                      f'  [ 3 ] - Cobrança de [yellow]outro mês[/].\n', 1, 3)
        match datacobra:
            case 1:
                mes = meshoje
            case 2:
                mes = meshoje - 1
                if mes < 1:
                    ano -= 1
            case _:
                mes = validar.valida_int('Digite o [cyan]NÚMERO[/] do mês que deseja realizar a cobrança: ', 1, 12)
                anocobra = validar.valida_int(f'[yellow]{funcoes.nomemes(mes).upper()}[/] de qual ano?\n'
                                       f'  [ 1 ] - [bright_blue]{ano - 1}[/];\n'
                                       f'  [ 2 ] - [bright_blue]{ano}[/];\n'
                                       f'  [ 3 ] - [bright_blue]{ano + 1}.\n', 1, 3)
                match anocobra:
                    case 1:
                        ano -= 1
                    case 3:
                        ano += 1
        arquivo = rf'Fichas_Gremio\{ano}_{mes:0>2}.txt'
        if oparquivo.arq_existe(arquivo):
            opc_arq = validar.valida_int(f'Foi identificado um arquivo de cobrança para esse mês. Escolha uma opção:\n'
                               f'[ 1 ] - SOBRESCREVER ARQUIVO\n'
                               f'[ 2 ] - ESCOLHER OUTRO MÊS\n'
                               f'[ 3 ] - RETORNAR AO MENU PRINCIPAL\n',1,3)
            match opc_arq:
                case 1:
                    sobrescrever = True
                    break
                case 2:
                    pass
                case _:
                    return None

        else:
            oparquivo.cria_arq(arquivo)
            break

    # ===== Início do loop principal e seleção do nome =====
    console.clear()
    console.rule(style='cyan')
    print(f'{f"  COBRANÇA DEFINIDA PARA O MÊS DE [bold underline purple]{funcoes.nomemes(mes).upper()}[/]  ":=^97}')
    print('[bold]Quando quiser finalizar o programa,'
          '[bold underline yellow] digite "FIM" na digitação de valores/quantidades.')
    while True:
        if qprod == 0:
            while True:
                duplicata = 0
                nome = str(input('Digite o nome na ficha: ')).strip()

                # ===== Tratamento de Duplicatas

                if nome in gremio:
                    funcoes.printlinha()
                    duplicata = validar.valida_int(
                        f'Já existe uma ficha com esse nome, com o valor de \033[1;32mR$ {gremio[nome].valficha:.2f}\033[m!\n'
                        'Deseja somar, substituir ou digitar um novo nome?\n'
                        '[bold green][ 1 ] SOMAR FICHA;\n'
                        '[bold red][ 2 ] SUBSTITUIR FICHA;\n'
                        '[bold yellow][ 3 ] DIGITAR NOVO NOME.[/][/][/]\n'
                        'Digite uma opção: ', 1, 3)
                    match duplicata:
                        case 1:
                            funcoes.printlinha()
                            print('As fichas de mesmo nome serão [bold green]SOMADAS.')
                        case 2:
                            funcoes.printlinha()
                            print('A outra ficha com mesmo nome será [bold red]SUBSTITUÍDA.')
                            gremio[nome].zerar()
                else:
                    gremio[nome] = Usuario(nome)
                if duplicata != 3:  # Se não for selecionada a opção de DIGITAR NOVO NOME
                    break

        # ===== Loop de cálculo, flag: "fim" =====

        funcoes.printlinha()
        produto = validar.valida_float('Digite o valor do produto: R$ ', exceto='FIM')
        if type(produto) is float:  # Permite calcular vários produtos enquanto o Flag não é digitado.
            qprod += 1  # Impede que o programa peça o nome após cada produto.
            qtde = validar.valida_int(f'Valor do produto: R$ {produto:.2f}. Informe a quantidade: ', exceto='FIM')
            if type(qtde) is int:
                s += produto * qtde
                print(f'Valor até o momento: [underline yellow]R$ {s:.2f}')
                sleep(0.3)
        if (type(produto) is str and produto.upper() == 'FIM') or (
                type(qtde) is str and qtde.upper() == 'FIM'):  # Caso seja digitado o Flag:
            funcoes.printlinha()

            # ===== Acréscimo de Mensalidade =====

            mensal = 30
            if validar.valida_sn(f'[cyan]Deseja acrescentar a mensalidade de R$ {mensal:.2f}?\n[ S / N ] → '):
                if duplicata == 1 and gremio[nome].mensalidade:
                    if validar.valida_sn(
                            f'[yellow]A mensalidade de [underline]{nome}[/underline] '
                            f'já foi cobrada. Deseja cobrar novamente?\n[ S / N ] → [/]'):
                        gremio[nome].cobrar_mensal()
                        s += 30
                else:
                    gremio[nome].cobrar_mensal()
                    s += 30
            console.rule(style='bright_white')

            # ===== Acréscimo da parcela do Ar Condicionado =====

            ar = 42
            if validar.valida_sn(
                    f'[cyan]Deseja acrescentar a parcela do ar condicionado de R$ {ar:.2f}?\n[ S / N ] → [/]'):
                if duplicata == 1 and gremio[nome].arcond:
                    if validar.valida_sn(
                            f'[yellow]A parcela do ar condicionado já foi cobrada de {nome}. '
                            f'Deseja cobrar novamente?\n[ S / N ] → [/]'):
                        gremio[nome].cobrar_arcond()
                        s += 42
                else:
                    gremio[nome].cobrar_arcond()
                    s += 42
            console.rule(style='bright_white')


            # ===== Acréscimo da mensalidade atrasada =====
            vdevedor = oparquivo.idt_caloteiro(nome,mes, ano)
            if vdevedor and validar.valida_sn(f'Foi identificado que [bold blue]{nome}[/] '
                                              f'possui uma cobrança pendente de [yellow]R$ {vdevedor:.2f}[/].\n'
                                              f'[cyan]Deseja acrescentar esse valor ao valor final? \n[ S / N ][/] → '):
                s += vdevedor
                console.rule(style='bright_white')
            elif validar.valida_sn(f'[bold blue]{nome}[cyan] possui mensalidade atrasasada?\n[ S / N ] → '):
                vdevedor = validar.valida_float('Digite o valor atrasado: R$ ')
                s += vdevedor

            # ===== Valor final =====

            print(f'Valor final para [bold blue]{nome}[/]: [green]R$ {s:.2f}')
            if duplicata == 1:
                print(f'Somado ao valor de [bold yellow]R$ {gremio[nome].valficha:.2f}[/] da outra ficha,'
                      f' o novo valor é de [bold green]R$ {gremio[nome].valficha + s:.2f}[/].')

            # ===== Menu de seleção =====

            opcao = validar.valida_int('[bold]Selecione uma opção abaixo:\n'
                                      '[cyan][ 1 ] - NOVA FICHA\n'
                                      '[yellow][ 2 ] - REFAZER ESTA FICHA\n'
                                      '[purple][ 3 ] - EXCLUIR ESTA FICHA\n'
                                      '[dark_green][ 4 ] - FINALIZAR CÁLCULO\n', 1, 4)
            console.rule(style='bright_white')
            match opcao:
                case 1:
                    qprod = 0  # Permite inserir um novo nome ao começar a nova ficha
                    gremio[nome].cobrar_valor(s)
                    s = 0
                case 2:
                    if duplicata == 1:
                        print('Refazendo a última ficha com este nome... ')
                    else:
                        gremio[nome].zerar()
                    s = 0  # Reseta o valor da soma pro próximo loop;
                    qprod = 1
                case 3:
                    if nome in gremio:
                        del gremio[nome]  # Apaga a ficha com aquele nome
                    s = 0  # Reseta o valor da soma pro próximo loop;
                    qprod = 0
            console.clear()
        if opcao == 4:
            gremio[nome].cobrar_valor(s)
            break

    # ===== Tabela de cobrança =====

    console.clear()
    tabelas.tabela_calculos(gremio, f'TABELA DE COBRANÇA - {funcoes.nomemes(mes).upper()}')
    console.rule(style='bright_white')
    if sobrescrever:
        if not oparquivo.zerar_arq(arquivo):
            print('Retornando ao menu principal...')
    for nome, obj in sorted(gremio.items()):
        oparquivo.escreva_arq(arquivo, f'{nome};{obj.valficha};{obj.pagou}')
    console.input('Digite [green]ENTER[/] para continuar.')
    return arquivo

#====================================CONSULTA/EDIÇÃO DE FICHAS====================================

def menu_pesquisa():
    tela_ini = Panel(f'~~ [underline]CONSULTA DE FICHAS[/] ~~'.center(89),
                     title='[bold cyan]GRÊMIO DOS TENENTES MBIAM', width=80,
                     style='bright_green', border_style='default')
    print(tela_ini)
    while True:
        anocobra = validar.valida_int(f'Deseja pesquisar a cobrança de qual ano?\n'
                                       f'  [ 1 ] - [bright_blue]{date.today().year}[/];\n'
                                       f'  [ 2 ] - [bright_blue]{date.today().year - 1}[/];\n'
                                       f'  [ 3 ] - [bright_blue]Outro ano[/].\n', 1, 3)
        match anocobra:
            case 1:
                ano = date.today().year
            case 2:
                ano = date.today().year - 1
            case _:
                ano = validar.valida_int('Digite o [cyan]ANO[/] do qual deseja consultar a cobrança: ', 2026)
        mes = validar.valida_int('Digite o [cyan]NÚMERO DO MÊS[/] do qual deseja consultar a cobrança: ', 1, 12)
        arquivo = rf'Fichas_Gremio\{ano}_{mes:0>2}.txt'
        if oparquivo.arq_existe(arquivo):
            consulta = oparquivo.ler_arq(arquivo)
            gremio = dict()
            for pessoa in consulta:
                ficha = pessoa[:-1].split(';')
                gremio[ficha[0]]=Usuario(ficha[0])
                gremio[ficha[0]].cobrar_valor(float(ficha[1]))
                gremio[ficha[0]].validar_pag(pagou=validar.valida_bool(ficha[2]))
            tabelas.tabela_calculos(gremio,f'COBRANÇA DE {funcoes.nomemes(mes).upper()} DE {ano}',pesquisa=True)
            if not validar.valida_sn('Deseja continuar consultando? [ S / N ]\n → ',False):
                break
        else:
            funcoes.printlinha()
            print('[yellow]Não foi encontrado nenhum arquivo com essa data![/]\n'
                  'Por favor, digite outra data.')
            funcoes.printlinha()

#====================================VALIDAÇÃO DE PAGAMENTO (ÚLTIMA FICHA)====================================

def menu_validar(arquivo):
    oparquivo.ler_arq(arquivo)
    consulta = oparquivo.ler_arq(arquivo)
    ano = arquivo[-11:-7]
    try:
        mes = int(arquivo[-6:-4])
    except TypeError:
        print('ERRO ao encontrar o mês da cobrança. Verifique o arquivo gerado:\n'
              'O formato correto é "aaaa_mm.txt"')
        return
    gremio = dict()
    for pessoa in consulta:
        ficha = pessoa[:-1].split(';')
        gremio[ficha[0]] = Usuario(ficha[0])
        gremio[ficha[0]].cobrar_valor(float(ficha[1]))
        gremio[ficha[0]].validar_pag(pagou=validar.valida_bool(ficha[2]))
    tabelas.tabela_calculos(gremio, f'COBRANÇA DE {funcoes.nomemes(mes).upper()} DE {ano}', pesquisa=True)
    while True:
        nome = str(console.input('Insira o [green]NOME[/] da pessoa para validar o pagamento.\n'
                                 'Digite [red]"FIM"[/] para retornar ao menu principal: ').strip())
        if nome.upper() == 'FIM':
            fim = console.input('Você digitou "FIM". Caso seja um nome na ficha, digite "nome".'
                  '\nCaso queira sair, digite qualquer coisa.').strip().upper()
            if not fim == 'NOME':
                break
        if gremio.get(nome):
            if gremio[nome].pagou:
                if validar.valida_sn(f'{nome} já foi validado! Deseja [red]DESVALIDAR[/] o pagamento de {nome}? [ S / N ]\n → '):
                    gremio[nome].validar_pag(pagou=False)
            else:
                gremio[nome].validar_pag()

            tabelas.tabela_calculos(gremio, f'COBRANÇA DE {funcoes.nomemes(mes).upper()} DE {ano}', pesquisa=True)
        else:
            print('Ficha não encontrada! Digite novamente.')
    oparquivo.zerar_arq(arquivo)
    for nome, obj in sorted(gremio.items()):
        oparquivo.escreva_arq(arquivo, f'{nome};{obj.valficha};{obj.pagou}')

