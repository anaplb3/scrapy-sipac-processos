import datetime
import pytz
from app.main.web_scrapy.sipac_selenium import open
from app.main.web_scrapy.soupbib import get_processos
from app.main.bd import repository
from sched import scheduler
from time import time, sleep
import psycopg2
from app.main.model.model import MovimentacaoProcessoDTO


class ProcessoService:
    def __init__(self):
        cfg = repository.environment_config()
        self.connection = psycopg2.connect(
            cfg["database_url"], sslmode=cfg["sslmode"])
        self.cursor = self.connection.cursor()

    def update_processos(self):
        processos = ["auxilio_emergencial", "auxilio_alimentacao_residencia",
                     "auxilio_alimentacao", "auxilio_moradia"]
        campus = ["I", "II", "III", "IV"]

        for processo in processos:
            for camp in campus:
                ano = datetime.datetime.now().year
                mes = "{}/{}".format(self.find_month(processo, camp), ano)

                if self.auxilios_inexistentes(processo, camp):
                    continue
                try:
                    resultados_selenium = open(processo, camp, mes)
                    movimentacao = get_processos(
                        resultados_selenium[0], resultados_selenium[1])

                    if movimentacao == None:
                        continue
                    else:
                        self.execute_update(movimentacao, camp, processo, mes)
                except Exception as e:
                    print("ProcessosServiceError: {}".format(str(e)))
                    continue
        self.auxilios_campus_i()

    def find_month(self, auxilio, campus):
        query = """SELECT status_terminado, mes_referente FROM processos 
        WHERE tipo_processo = '{}' AND campus = '{}'""".format(auxilio, campus)
        self.cursor.execute(query)

        resultado = list(self.cursor.fetchall())
        if len(resultado) == 0:
            if auxilio == "auxilio_emergencial":
                return "Julho"
            return "Agosto"
        else:
            status = resultado[0][0]
            mes_referente = resultado[0][1].split("/")[0]
            return self.get_month(status, mes_referente)

    def get_month(self, status, mes_referente):
        months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        index = months.index(mes_referente)
        if status:
            return months[index + 1]
        else:
            return mes_referente

    def auxilios_campus_i(self):
        processos = ["auxilio_residencia_rumf",
                     "auxilio_residencia_rufet", "auxilio_residentes"]
        campus = "I"
        ano = datetime.datetime.now().year

        for processo in processos:
            mes = "{}/{}".format(self.find_month(processo, campus), ano)

            try:
                if processo == "auxilio_residentes":
                    campus = "MANGABEIRA"
                resultados_selenium = open(processo, campus, mes)
                movimentacao = get_processos(
                    resultados_selenium[0], resultados_selenium[1])

                if movimentacao == None:
                    continue
                else:
                    self.execute_update(movimentacao, campus, processo, mes)
            except Exception as e:
                print("ProcessosServiceError: {}".format(str(e)))
                continue

    def auxilios_inexistentes(self, auxilio, camp):
        if (auxilio == "auxilio_alimentacao" and camp == "III") or (auxilio == "auxilio_alimentacao" and camp == "II") or (auxilio == "auxilio_alimentacao_residencia" and camp == "I"):
            return True
        else:
            return False

    def execute_update(self, movimentacao, camp, processo, mes):
        timestamp = self.format_timezone()
        query_update_processos = """
            UPDATE processos
            SET unidade_destino = '{}',
            recebido_em = '{}',
            status_terminado = '{}',
            link_processo = '{}',
            atualizado_em = '{}',
            campus = '{}',
            tipo_processo = '{}',
            mes_referente = '{}'
            WHERE tipo_processo = '{}' and campus = '{}'
            """.format(
            movimentacao.unidade_destino,
            movimentacao.recebido_em,
            movimentacao.status_terminado,
            movimentacao.link_processo,
            timestamp, camp,
            processo, mes,
            processo, camp)

        self.cursor.execute(query_update_processos)
        self.connection.commit()

    def get_processo(self, campus, auxilio):
        if campus == "" or auxilio == "":
            return None
        query = """SELECT unidade_destino, recebido_em, 
        status_terminado, link_processo, atualizado_em FROM processos 
        WHERE tipo_processo = '{}' and campus = '{}' """.format(auxilio, campus)
        self.cursor.execute(query)
        processo = list(self.cursor.fetchone())

        return MovimentacaoProcessoDTO(processo[0], processo[1],
                                       processo[2], processo[3],
                                       processo[4], auxilio, campus)

    def format_timezone(self):
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        return utc_now.astimezone(pytz.timezone("America/Sao_Paulo"))
