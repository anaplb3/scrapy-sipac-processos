class MovimentacaoProcesso(object):
    def __init__(self, data_origem, unidade_origem, unidade_destino, enviado_por, recebido_em, recebido_por, urgente):
        self.data_origem = data_origem
        self.unidade_origem = unidade_origem
        self.unidade_destino = unidade_destino
        self.enviado_por = enviado_por
        self.recebido_em = recebido_em
        self.recebido_por = recebido_por
        self.urgente = urgente

    def serialize(self):
        return {
            'data_origem': self.data_origem,
            'unidade_origem': self.unidade_origem,
            'unidade_destino': self.unidade_destino,
            'enviado_por': self.enviado_por,
            'recebido_em': self.recebido_em,
            'recebido_por': self.recebido_por,
            'urgente': self.urgente
        }


class MovimentacaoProcessoDTO(object):
    def __init__(self, data_origem, unidade_origem, unidade_destino, recebido_em, atualizado_em, tipo_auxilio, campus):
        self.data_origem = data_origem
        self.unidade_origem = unidade_origem
        self.unidade_destino = unidade_destino
        self.recebido_em = recebido_em
        self.atualizado_em = atualizado_em
        self.tipo_auxilio = tipo_auxilio
        self.campus = campus

    def serialize(self):
        return {
            'data_origem': self.data_origem,
            'unidade_origem': self.unidade_origem,
            'unidade_destino': self.unidade_destino,
            'recebido_em': self.recebido_em,
            'atualizado_em': self.atualizado_em,
            'tipo_auxilio': self.tipo_auxilio,
            'campus': self.campus
        }
