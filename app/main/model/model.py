class MovimentacaoProcessoDTO(object):
    def __init__(self, unidade_destino, recebido_em, status_terminado, link_processo, atualizado_em, proxima_atualizacao, tipo_auxilio, campus, mes_referente):
        self.unidade_destino = unidade_destino
        self.recebido_em = recebido_em
        self.status_terminado = status_terminado
        self.link_processo = link_processo
        self.atualizado_em = atualizado_em
        self.proxima_atualizacao_em = proxima_atualizacao
        self.tipo_auxilio = tipo_auxilio
        self.campus = campus
        self.mes_referente = mes_referente

    def serialize(self):
        return {
            'unidade_destino': self.unidade_destino,
            'recebido_em': self.recebido_em,
            'status_terminado': self.status_terminado,
            'link_processo': self.link_processo,
            'atualizado_em': self.atualizado_em,
            'proxima_atualizacao_em': self.proxima_atualizacao_em,
            'tipo_auxilio': self.tipo_auxilio,
            'campus': self.campus,
            'mes_referente': self.mes_referente
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


class CampusDTO(object):
    def __init__(self, id_campus, campus):
        self.id_campus = id_campus
        self.campus = campus

    def serialize(self):
        return {
            'id_campus': self.id_campus,
            'campus': self.campus
        }


class AuxilioDTO(object):
    def __init__(self, id_auxilio, id_campus, tipo_auxilio, nome_visualizacao):
        self.id_auxilio = id_auxilio
        self.id_campus = id_campus
        self.tipo_auxilio = tipo_auxilio
        self.nome_visualizacao = nome_visualizacao

    def serialize(self):
        return {
            'id_auxilio': self.id_auxilio,
            'id_campus': self.id_campus,
            'tipo_auxilio': self.tipo_auxilio,
            'nome_visualizacao': self.nome_visualizacao
        }


class MovimentacaoAnteriorDTO(object):
    def __init__(self, id_auxilio, id_campus, link_processo, campus, tipo_processo, mes_referente):
        self.id_auxilio = id_auxilio
        self.id_campus = id_campus
        self.link_processo = link_processo
        self.campus = campus
        self.tipo_processo = tipo_processo
        self.mes_referente = mes_referente

    def serialize(self):
        return {
            'id_auxilio': self.id_auxilio,
            'id_campus': self.id_campus,
            'link_processo': self.link_processo,
            'tipo_processo': self.tipo_processo,
            'campus': self.campus,
            'mes_referente': self.mes_referente
        }

class Excluded(object):
    def __init__(self, registration, reason_to_be_excluded):
        self.registration = registration
        self.reason_to_be_excluded = reason_to_be_excluded
    
    def serialize(self):
        return {
            'registration': self.registration,
            'reason_to_be_excluded': self.reason_to_be_excluded
        }
