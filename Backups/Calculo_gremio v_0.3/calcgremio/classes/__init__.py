class Ficha:
    """
    Gera um consumidor do grêmio.

    É possível gerenciar se pagou as mensalidades e parcelas diversas.
    variavel = Consumidor(nome)
    """
    def __init__(self, nome = '<desconhecido>'):
        self.nome= nome
        self.mensalidade = False
        self.arcond = False
        self.valficha = 0.0
        self.pagou = False


    def cobrar_mensal(self):
        self.mensalidade = True


    def cobrar_arcond(self):
        self.arcond = True


    def cobrar_valor(self,valor = 0):
        self.valficha += valor


    def validar_pag(self,pagou = True):
        self.pagou = pagou


    def zerar(self):
        self.arcond = self.mensalidade = False
        self.valficha = 0


    def __str__(self):
        return (f'O {self.nome}:\n'
                f'  {'PAGOU' if self.mensalidade else 'NÃO PAGOU'} a mensalidade;\n'
                f'  {'PAGOU' if self.arcond else 'NÃO PAGOU'} a parcela do ar condicionado;\n'
                f'  Possui valor da ficha de {self.valficha:.2f}')


    def __getstate__(self):
        return (f'Estado: nome = {self.nome};\n'
                f'mensalidade = {self.mensalidade};\n'
                f'arcond = {self.arcond};\n'
                f'vficha = {self.valficha}')


