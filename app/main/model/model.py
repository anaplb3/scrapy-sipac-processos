class MovimentacaoProcessoDTO(object):
    def __init__(self, unidade_destino, recebido_em, status_terminado, link_processo, atualizado_em, tipo_auxilio, campus):
        self.unidade_destino = unidade_destino
        self.recebido_em = recebido_em
        self.status_terminado = status_terminado
        self.link_processo = link_processo
        self.atualizado_em = atualizado_em
        self.tipo_auxilio = tipo_auxilio
        self.campus = campus

    def serialize(self):
        return {
            'unidade_destino': self.unidade_destino,
            'recebido_em': self.recebido_em,
            'status_terminado': self.status_terminado,
            'link_processo': self.link_processo,
            'atualizado_em': self.atualizado_em,
            'tipo_auxilio': self.tipo_auxilio,
            'campus': self.campus
        }


class MovimentacaoProcesso(object):
    def __init__(self, unidade_destino, recebido_em, status_terminado, link_processo):
        self.unidade_destino = unidade_destino
        self.recebido_em = recebido_em
        self.status_terminado = status_terminado
        self.link_processo = link_processo

    def serialize(self):
        return {
            'unidade_destino': self.unidade_destino,
            'recebido_em': self.recebido_em,
            'status_terminado': self.status_terminado,
            'link_processo': self.link_processo
        }
