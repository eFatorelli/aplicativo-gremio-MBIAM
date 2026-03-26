from rich import print
from rich.console import Console


console = Console()


def nomemes(num_mes):
    meses=['janeiro','fevereiro','março',
           'abril','maio','junho','julho',
           'agosto','setembro','outubro',
           'novembro','dezembro']
    return meses[num_mes - 1]


def valida_int(txt, ini=0, fim=None, exceto=None, negativo = False, erro = f'[bold red]Opção inválida! Digite novamente.'):
    """
    ->Valida um número inteiro positivo ou um str definido como exceção.
    :param txt: Valor a ser analisado.
    :param ini: Intervalo inicial da validação
    :param fim: Intervalo final da validação. Se não especificado, não haverá limite final.
    :param exceto: Define a str que será a exceção da validação.
    :param negativo: Caso False, valida somente valores positivos.
    :param erro: Mensagem de erro personalizada.
    :return: Retorna um número inteiro positivo dentro do intervalo exigido
    OU uma mensagem solicitando novo input.
    """
    while True:
        num=str(console.input(txt)).strip()
        if exceto is not None and num.upper()==exceto.upper():
            return str(num)
        if num.isdecimal():
            num=int(num)
            if num>=ini and (fim is None or num<=fim):
                if (num<0 and negativo) or num>=0:
                    return int(num)

        print(erro)


def valida_float(txt, exceto=None, negativo = False):
    """
    Valida se um número é float ou não. Substitui ',' por '.' para validação.
    :param txt: Valor a ser analisado.
    :param exceto: Exceção que o usuário queira fazer para alguma str.
    :param negativo: Caso False, valida somente valores positivos.
    :return: Valor float digitado OU mensagem de erro.
    """
    while True:
        num=str(console.input(txt)).strip().replace(',', '.')
        if exceto is not None and num.upper()==exceto.upper():
            return str(num)
        else:
            try:
                num=float(num)
                if num < 0 and not negativo:
                    print('[red]ERRO! DIGITE UM VALOR VÁLIDO')
                else:
                    return num
            except ValueError:
                print('[red]ERRO! DIGITE UM VALOR VÁLIDO')



def valida_sn(txt, n_auto=True):
    """
    -> Valida uma seleção de Sim ou Não. Inclui somente a primeira letra digitada,
    sendo recomendado instruir à pessoa digitar somente S ou N. Por padrão, uma
    resposta vazia significa NÃO.
    :param txt: Valor a ser analisado. Não faz input automático.
    :param n_auto: Quanto True (padrão), faz uma resposta vazia ser equivalente a NÃO.
                Caso o parâmetro seja False, não aceitará resposta vazia.
    :return: Retorna True para 'S' e False para 'N'.
    """
    while True:
        opcao=str(console.input(txt)).strip().upper()
        if not opcao:
            if n_auto:
                opcao='N'
            else:
                opcao='a'
        match opcao[0]:
            case 'S':
                return True
            case 'N':
                return False

def valida_bool(txt):
    match str(txt.strip().upper()):
        case 'FALSE'|'NÃO'|'NAO'|'N'|'0'|'':
            return False
        case _:
            return True