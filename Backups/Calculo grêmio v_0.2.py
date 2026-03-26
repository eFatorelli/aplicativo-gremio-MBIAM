from calcgremio import oparquivo, validar, funcoes
from calcgremio.classes import *
from datetime import date
from time import sleep


produto=s=qtde=qprod=total=valor_anterior=opcao=duplicata=mes=0
nome=''
gremio=dict()
meshoje=date.today().month
try:

    #===== Seleção do mês da cobrança ===== (utilidades a serem implementadas)

    print(f'\033[1;36m{" CALCULADORA DO GRÊMIO DOS TENENTES MBIAM ":=^85}\033[m')
    print(f'~~{date.today().day} de {funcoes.nomemes(meshoje).upper()} de {date.today().year}~~'.center(85))
    datacobra= validar.valida_int(f'Deseja realizar a cobrança para esse mês, mês anterior ou outro mês?\n'
                                f'  [ 1 ] - Cobrança do mês de {funcoes.nomemes(meshoje).upper()};\n'
                                f'  [ 2 ] - Cobrança do mês de {funcoes.nomemes(meshoje - 1).upper()};\n'
                                f'  [ 3 ] - Cobrança de outro mês.\n', 1, 3)
    match datacobra:
        case 1:
            mes=meshoje
        case 2:
            mes=meshoje-1
        case 3:
            mes= validar.valida_int('Digite o NÚMERO do mês que deseja realizar a cobrança: ', 1, 12)
    arquivo=rf'Fichas_Grêmio\{funcoes.nomemes(mes)}.txt'
    oparquivo.arq_existe(arquivo, True)

    #===== Início do loop principal e seleção do nome =====

    print(f'{f"  COBRANÇA DEFINIDA PARA O MÊS DE \033[1;4;35m{funcoes.nomemes(mes).upper()}\033[m  ":=^97}')
    print('\033[4mQuando quiser finalizar o programa,\033[1;33m digite "FIM" na digitação de valores/quantidades.\033[m')
    while True:
        if qprod==0:
            valor_anterior=0
            while True:
                duplicata=0
                nome=str(input('Digite o nome na ficha: ')).strip()

                #===== Tratamento de Duplicatas

                if nome in gremio:
                    funcoes.printlinha()
                    duplicata= validar.valida_int(f'Já existe uma ficha com esse nome, com o valor de \033[1;32mR$ {gremio[nome].valficha:.2f}\033[m!\n'
                                                'Deseja somar, substituir ou digitar um novo nome?\n'
                                                '\033[1;32m[ 1 ] SOMAR FICHA;\n'
                                                '\033[1;31m[ 2 ] SUBSTITUIR FICHA;\n'
                                                '\033[1;33m[ 3 ] DIGITAR NOVO NOME.\033[m\n'
                                                'Digite uma opção: ', 1, 3)
                    match duplicata:
                         case 1:
                            funcoes.printlinha()
                            print('As fichas de mesmo nome serão \033[1;32mSOMADAS\033[m.')
                         case 2:
                            funcoes.printlinha()
                            print('A outra ficha com mesmo nome será \033[1;31mSUBSTITUÍDA\033[m.')
                            gremio[nome].zerar()
                else:
                    gremio[nome] = Usuario(nome)
                if duplicata!=3: #Se não for selecionada a opção de DIGITAR NOVO NOME
                    break

       #===== Loop de cálculo, flag: "fim" =====

        funcoes.printlinha()
        produto= validar.valida_float('Digite o valor do produto: R$ ', exceto='FIM')
        if type(produto) is float: #Permite calcular vários produtos enquanto o flag não é digitado.
            qprod+=1 #Impede que o programa peça o nome após cada produto.
            qtde= validar.valida_int(f'Valor do produto: R$ {produto:.2f}. Informe a quantidade: ', exceto='FIM')
            if type(qtde) is int:
                s+=produto*qtde
                print(f'Valor até o momento: \033[4;33mR$ {s:.2f}\033[m')
                sleep(0.3)
        if (type(produto) is str and produto.upper()=='FIM') or (type(qtde) is str and qtde.upper()=='FIM'): #Caso seja digitado o flag:
            funcoes.printlinha()

            #===== Acréscimo de Mensalidade =====

            mensal=30
            if validar.valida_sn(f'\033[1;34mDeseja acrescentar a mensalidade de R$ {mensal:.2f}?\033[m\n[ S / N ] → '):
                if duplicata==1 and gremio[nome].mensalidade:
                    if validar.valida_sn(f'\033[33mA mensalidade de {nome} já foi cobrada. Deseja cobrar novamente?\033[m\n[ S / N ] → '):
                        gremio[nome].cobrar_mensal()
                        s+=30
                else:
                    gremio[nome].cobrar_mensal()
                    s+=30

            #===== Acréscimo da parcela do Ar Condicionado =====

            ar = 42
            if validar.valida_sn(f'\033[1;34mDeseja acrescentar a parcela do ar condicionado de R$ {ar:.2f}?\033[m\n[ S / N ] → '):
                if duplicata == 1 and gremio[nome].arcond:
                    if validar.valida_sn(f'\033[33mA parcela do ar condicionado já foi cobrada de {nome}. Deseja cobrar novamente?\033[m\n[ S / N ] → '):
                        gremio[nome].cobrar_arcond()
                        s+=42
                else:
                    gremio[nome].cobrar_arcond()
                    s+=42

            #===== Acréscimo da mensalidade atrasada =====

            if validar.valida_sn(f'\033[1;36m{nome}\033[1;34m possui mensalidade atrasasada?\033[m\n[ S / N ] → '):
                vdevedor = validar.valida_float('Digite o valor atrasado: R$ ')
                s+=vdevedor

            #===== Valor final =====

            print(f'Valor final para \033[1;36m{nome}\033[m: \033[1;32mR$ {s:.2f}\033[m')
            if duplicata==1:
                print(f'Somado ao valor de \033[1;33mR$ {gremio[nome].valficha:.2f}\033[m da outra ficha,'
                      f' o novo valor é de \033[1;32mR$ {gremio[nome].valficha+s:.2f}.\033[m')

            #===== Menu de seleção =====

            opcao= validar.valida_int('\033[4mSelecione uma opção abaixo:\033[m\n'
                                    '\033[1;34m[ 1 ] - NOVA FICHA\n'
                                    '\033[1;33m[ 2 ] - REFAZER ESTA FICHA\n'
                                    '\033[1;35m[ 3 ] - EXCLUIR ESTA FICHA\n'
                                    '\033[1;31m[ 4 ] - ENCERRAR PROGRAMA\033[m\n', 1, 4)
            funcoes.printlinha()
            match opcao:
                case 1:
                    qprod=0 #Permite inserir um novo nome ao começar a nova ficha
                    gremio[nome].cobrar_valor(s)
                    s = 0
                case 2:
                    if duplicata==1:
                        print('Refazendo a última ficha com este nome... ')
                    else:
                        gremio[nome].zerar()
                    s = 0  # Reseta o valor da soma pro próximo loop;
                    qprod=1
                case 3:
                    if nome in gremio:
                        del gremio[nome] #Apaga a ficha com aquele nome
                    s = 0  # Reseta o valor da soma pro próximo loop;
                    qprod=0
        if opcao==4:
            gremio[nome].cobrar_valor(s)
            break

    #===== Tabela de cobrança =====

    print('\n')
    funcoes.tabela(gremio, f'TABELA DE COBRANÇA - {funcoes.nomemes(mes).upper()}', 'TOTAL A ARRECADAR')
    funcoes.printlinha()
    input('Pressione ENTER para encerrar o programa.')
except KeyboardInterrupt:
    print(f'\n\n{"USUÁRIO FINALIZOU O PROGRAMA":^85}')
finally:
    print(f'\n\n\033[1;31m{" PROGRAMA ENCERRADO ":=^85}\033[m')
    funcoes.sleep(2)