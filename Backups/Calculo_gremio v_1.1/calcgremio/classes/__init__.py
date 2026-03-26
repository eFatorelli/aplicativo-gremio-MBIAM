class Usuario:
    """
    Gera uma ficha de um consumidor do grêmio.

    É possível gerenciar se pagou as mensalidades e parcelas diversas.
    Variável = Ficha(nome)
    """

    def __init__(self, nome = 'DEFINA UM NOME'):
        self.id = 0
        self.apelidos = []
        self.nome = nome
        self.historico = {}
            #{aaaa-mm:{'mensalidade':False, 'ar_cond':False, 'pagou':False, 'val_final':0.0}}

#=======================CADASTRO DE USUÁRIOS=======================

    def definir_id(self, id):
        self.id = id


    def apelidar(self, apelido):
        self.apelidos.append(apelido)


#=====================PORTABILIDADE JSON====================


    def to_dict(self):
        return {'id':self.id,'nome':self.nome,'apelidos':self.apelidos,'historico':self.historico}


    def to_obj(self,dict_user):
        self.id = dict_user['id']
        self.nome = dict_user['nome']
        self.apelidos = dict_user['apelidos']
        self.historico = dict_user['historico']
        return self
#=====================CÁLCULO DE COBRANÇA=======================

    def registrar(self, ano, mes) -> None:
        """
        -> Registra um ano e mês no histórico de cobranças
        para que uma nova cobrança seja feita.

        Caso já tenha sido registrada uma cobrança para a
        data em questão, não faz nada.

        :param ano: Ano da cobrança
        :param mes: Mês da cobrança
        :return: None
        """
        if not self.historico.get(f'{ano}-{mes:0>2}'):
            self.historico[f'{ano}-{mes:0>2}'] = {'mensalidade':False,
                                                  'ar_cond':False,
                                                  'pagou':False,
                                                  'val_final':0.0}


    def cobrar_mensal(self, ano, mes):
        self.historico[f'{ano}-{mes:0>2}']['mensalidade'] = True


    def cobrar_arcond(self, ano, mes):
        self.historico[f'{ano}-{mes:0>2}']['ar_cond'] = True


    def cobrar_valor(self,valor,ano,mes):
        self.historico[f'{ano}-{mes:0>2}']['val_final'] += valor


    def validar_pag(self,ano, mes, pagou = True):
        self.historico[f'{ano}-{mes:0>2}']['pagou'] = pagou


    def zerar(self, ano, mes):
        self.historico[f'{ano}-{mes:0>2}'] = {'mensalidade': False,
                                              'ar_cond': False,
                                              'pagou': False,
                                              'val_final': 0.0}


    def apagar_mes(self,ano,mes) -> bool:
        if self.historico.get(f'{ano}-{mes:0>2}'):
            del self.historico[f'{ano}-{mes:0>2}']
            return True
        else:
            return False


    def ler_valor(self, ano, mes):
        return self.historico[f'{ano}-{mes:0>2}']['val_final']


    def ler_mensalidade(self,ano,mes):
        return self.historico[f'{ano}-{mes:0>2}']['mensalidade']


    def ler_arcond(self,ano,mes):
        return self.historico[f'{ano}-{mes:0>2}']['ar_cond']


    def ler_pagamento(self,ano,mes) -> bool:
        """
        -> Verifica se o usuário pagou determinada mensalidade.
        :param ano: Ano da mensalidade.
        :param mes: Mês da mensalidade.
        :return: True caso tenha pagado.
                 False caso não tenha pagado.
        """
        return self.historico[f'{ano}-{mes:0>2}']['pagou']
