from .common import *

def menu_calc(arquivo, arq_def):

    s = qtde = qprod = opcao_ficha = duplicata = mes = 0
    meshoje = date.today().month
    ano = date.today().year
    dados = oparquivo.ler_arq(arquivo)
    definicoes = oparquivo.ler_arq(arq_def)

    # ===== Seleção do mês da cobrança ===== (utilidades a serem implementadas)
    tela_ini = Panel(f'~~ [underline]CALCULADORA DE FICHAS[/] ~~'.center(89),
                     title='[bold cyan]GRÊMIO DOS TENENTES MBIAM', width=80,
                     style='bright_green', border_style='default',
                     subtitle=f'[bright_yellow]{date.today().day} de '
                              f'{validar.nomemes(meshoje).upper()} de {ano}')
    print(tela_ini)
    datacobra = validar.valida_int(f'Deseja realizar a cobrança para esse mês, mês anterior ou outro mês?\n'
                                  f'  [ 1 ] - Cobrança de [yellow]{validar.nomemes(meshoje).upper()} de {ano}[/];\n'
                                  f'  [ 2 ] - Cobrança de [yellow]{validar.nomemes(meshoje - 1).upper()} de {ano - 1 if meshoje - 1 < 0 else ano}[/];\n'
                                  f'  [ 3 ] - Cobrança de [yellow]outro mês[/].\n'
                                  f'  [ 4 ] - [red]VOLTAR AO MENU PRINCIPAL\n', 1, 4)
    match datacobra:
        case 1:
            mes = meshoje
        case 2:
            mes = meshoje - 1
            if mes < 1:
                ano -= 1
        case 3:
            mes = validar.valida_int('Digite o [cyan]NÚMERO[/] do mês que deseja realizar a cobrança: ', 1, 12)
            anocobra = validar.valida_int(f'[yellow]{validar.nomemes(mes).upper()}[/] de qual ano?\n'
                                   f'  [ 1 ] - [bright_blue]{ano - 1}[/];\n'
                                   f'  [ 2 ] - [bright_blue]{ano}[/];\n'
                                   f'  [ 3 ] - [bright_blue]{ano + 1}.\n', 1, 3)
            match anocobra:
                case 1:
                    ano -= 1
                case 3:
                    ano += 1
        case _:
            return None

    # ===== Início do loop principal e seleção do nome =====
    console.clear()
    console.rule(style='cyan')
    print(f'{f"  COBRANÇA DEFINIDA PARA O MÊS DE [bold underline purple]{validar.nomemes(mes).upper()}[/]  ":=^97}')
    user = Usuario()
    while True:
        if qprod == 0:
            while True:
                duplicata = 0
                nome = str(input('Digite o nome na ficha: ')).strip().title()
                if sistema.localizar_usuario(dados,nome,'nome'):
                    print(f'Nome "{nome}" localizado!')
                    user = Usuario().to_obj(sistema.localizar_usuario(dados,nome,'nome'))
                elif sistema.localizar_usuario(dados,nome,'apelido'):
                    u = sistema.localizar_usuario(dados,nome,'apelido')
                    print(f'"{nome}" localizado como APELIDO de "{u['nome']}" ')
                    user = Usuario().to_obj(u)
                else:
                    console.clear()
                    console.rule(style='bright_white')
                    cad = validar.valida_int(f'"{nome}" não foi identificado como [underline]NOME[/] ou [underline]APELIDO[/] de usuário.\n'
                                             f'Selecione uma opção:\n'
                                             f'[ 1 ] - Cadastrar {nome} como NOME;\n'
                                             f'[ 2 ] - Cadastrar {nome} como APELIDO de algum usuário;\n'
                                             f'[ 3 ] - Digitar novo nome;\n'
                                             f'[ 4 ] - RETORNAR AO MENU\n → ',1,4)
                    match cad:
                        case 1:
                            sistema.escreva_arq(arquivo,sistema.cadastrar_usuario(arquivo, nome), sobrescreva=True)
                            dados = oparquivo.ler_arq(arquivo)
                            console.clear()
                            user = Usuario().to_obj(sistema.localizar_usuario(dados,nome,'nome'))
                            break
                        case 2:
                            user_dict = sistema.localizar_usuario(dados,console.input('Digite o NOME do usuário: '),'nome')
                            if user_dict is not None:
                                console.clear()
                                user = Usuario().to_obj(user_dict)
                                print(f'Usuário {user.nome} localizado! Adicionando apelido e prosseguindo com a ficha.')
                                user.apelidar(nome)
                                break
                            else:
                                print('Usuário não localizado!')
                                continue
                        case 3:
                            console.clear()
                            console.rule(style='bright_white')
                            continue
                        case _:
                            return None

                # ===== Tratamento de Duplicatas

                if user.historico.get(f'{ano}-{mes:0>2}'):
                    console.rule(style='bright_white')
                    duplicata = validar.valida_int(
                        f'Já existe uma ficha com esse nome, com o valor de [green]R$ {user.ler_valor(ano, mes):.2f}[/]!\n'
                        'Deseja somar, substituir ou digitar um novo nome?\n'
                        '[bold green][ 1 ] SOMAR FICHA;\n'
                        '[bold red][ 2 ] SUBSTITUIR FICHA;\n'
                        '[bold yellow][ 3 ] DIGITAR NOVO NOME.[/][/][/]\n'
                        'Digite uma opção: ', 1, 3)
                    match duplicata:
                        case 1:
                            console.rule(style='bright_white')
                            print('As fichas de mesmo nome serão [bold green]SOMADAS.')
                        case 2:
                            console.rule(style='bright_white')
                            print('A outra ficha com mesmo nome será [bold red]SUBSTITUÍDA.')
                            user.zerar(ano, mes)
                        case 3:
                            console.clear()
                            console.rule(style='bright_white')
                            continue
                break
            user.registrar(ano, mes)

        # ===== Loop de cálculo, flag: "fim" =====
        console.rule(style='bright_white')
        print('[bold]Quando quiser finalizar o programa, '
              '[bold underline yellow] digite "FIM" na digitação de valores/quantidades.')
        produto = validar.valida_float('Digite o valor do produto: R$ ', exceto='FIM')
        if isinstance(produto,float):  # Permite calcular vários produtos enquanto o Flag não é digitado.
            qprod += 1  # Impede que o programa peça o nome após cada produto.
            qtde = validar.valida_int(f'Valor do produto: R$ {produto:.2f}. Informe a quantidade: ', exceto='FIM')
            if isinstance(qtde,int):
                s += produto * qtde
                print(f'Valor até o momento: [underline yellow]R$ {s:.2f}')
                sleep(0.3)
        if (isinstance(produto,str) and produto.upper() == 'FIM') or (
                isinstance(qtde, str) and qtde.upper() == 'FIM'):  # Caso seja digitado o Flag:
            console.rule(style='bright_white')

            # ===== Acréscimo de Mensalidade =====

            mensal = definicoes['mensalidade']
            if validar.valida_sn(f'[cyan]Deseja acrescentar a mensalidade de R$ {mensal:.2f}?\n[ S / N ] → '):
                if duplicata == 1 and user.ler_mensalidade(ano,mes):
                    if validar.valida_sn(
                            f'[yellow]A mensalidade de [underline]{user.nome}[/underline] '
                            f'já foi cobrada. Deseja cobrar novamente?\n[ S / N ] → [/]'):
                        user.cobrar_mensal(ano, mes)
                        s += mensal
                else:
                    user.cobrar_mensal(ano, mes)
                    s += mensal
            console.rule(style='bright_white')

            # ===== Acréscimo de cobranças extras: =====

            for titulo, (valor, q_parcelas) in definicoes['extra'].items():
                if validar.valida_sn(
                        f'[cyan]Deseja cobrar "{titulo.capitalize()}" na ficha (R$ {valor:.2f})?\n'+
                        ('' if q_parcelas == 0 else
                        f'[green]Todas as parcelas ja foram pagas!\n' if q_parcelas > 0 and q_parcelas == user.ler_qtde_parcel(titulo,ano) else
                        f'[yellow][ {user.ler_qtde_parcel(titulo,ano) + 1}ª parcela de {q_parcelas} ]\n')
                        + f'[cyan][ S / N ] → [/]'):
                    if duplicata == 1 and user.ler_extra(titulo, ano, mes):
                        if validar.valida_sn(
                                f'[yellow]"{titulo}" já foi cobrada de {user.nome} esse mês. '
                                f'Deseja cobrar novamente?\n[ S / N ] → [/]'):
                            user.cobrar_extra(titulo, ano, mes, valor, True)
                            s += valor
                        else:
                            user.cobrar_extra(titulo, ano, mes, valor, False)
                    else:
                        user.cobrar_extra(titulo, ano, mes, valor, True)
                        s += valor
                else:
                    user.cobrar_extra(titulo, ano, mes, valor, False)

            console.rule(style='bright_white')

            # ===== Identificação da mensalidade atrasada =====
            cal = sistema.idt_caloteiro(user)
            if cal:
                d_calot, v_calot = cal
                print(f'[yellow]AVISO:[/] Foram identificadas cobranças não pagas de {d_calot} somando o valor de R$ {v_calot:.2f}.\n'
                      f'Confira mais detalhes no menu "VALIDAR PAGAMENTO".')

            # ===== Valor final =====

            console.clear()
            print(f'Valor final para [bold blue]{user.nome}[/]: [green]R$ {s:.2f}')
            if duplicata == 1:
                print(f'Somado ao valor de [bold yellow]R$ {user.ler_valor(ano, mes):.2f}[/] da outra ficha,'
                      f' o novo valor é de [bold green]R$ {user.ler_valor(ano, mes) + s:.2f}[/].')
            user.cobrar_valor(s, ano, mes)
            oparquivo.escreva_arq(arquivo,sistema.atualizar_ficha(arquivo,user),sobrescreva=True)


            # ===== Menu de seleção =====
            while True:
                opcao_ficha = validar.valida_int('[bold]Selecione uma opção abaixo:\n'
                                           '[cyan][ 1 ] - NOVA FICHA\n'
                                           '[yellow][ 2 ] - REFAZER ESTA FICHA\n'
                                           '[red][ 3 ] - EXCLUIR ESTA FICHA\n'
                                           '[purple][ 4 ] - FINALIZAR CÁLCULO\n', 1, 4)
                console.rule(style='bright_white')
                match opcao_ficha:
                    case 1:
                        qprod = 0  # Permite inserir um novo nome ao começar a nova ficha
                        s = 0
                    case 2:
                        user.zerar(ano, mes)
                        s = 0  # Reseta o valor da soma pro próximo loop;
                        qprod = 1
                    case 3:
                        if user.apagar_mes(ano,mes):
                            print('[green]FICHA APAGADA COM SUCESSO![/]')
                        else:
                            print('[yellow]A FICHA JA FOI APAGADA![/]')
                        s = 0  # Reseta o valor da soma pro próximo loop;
                        qprod = 0
                        continue
                break
            console.clear()
        if opcao_ficha == 4:
            break

    # ===== Tabela de cobrança =====

    console.clear()
    tabelas.tabela_calculos(arquivo, ano, mes,f'TABELA DE COBRANÇA - {validar.nomemes(mes).upper()}')
    console.rule(style='bright_white')
    console.input('Digite [green]ENTER[/] para continuar.')
    return None
