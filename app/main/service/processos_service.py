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
        self.cursor.execute("DROP TABLE IF EXISTS processos")
        self.connection.commit()

        repository.create_table(self.cursor, self.connection)

        processos = ["auxilio_emergencial", "auxilio_alimentacao_residencia",
                     "auxilio_alimentacao", "auxilio_moradia"]
        campus = ["I", "II", "III", "IV"]

        for processo in processos:
            for camp in campus:
                ano = datetime.datetime.now().year
                mes = "{}/{}".format(self.format_data(1), ano)
                if processo == "auxilio_emergencial":
                    mes = "{}/{}".format(self.format_data(2), ano)

                if processo == "auxilio_alimentacao" and camp == "II":
                    continue
                try:
                    resultados_selenium = open(processo, camp, mes)
                    movimentacao = get_processos(
                        resultados_selenium[0], resultados_selenium[1])
                    if movimentacao == None:
                        continue
                    else:
                        self.execute_update(movimentacao, camp, processo, mes)
                except:
                    break

    def execute_update(self, movimentacao, camp, processo, mes):
        timestamp = self.format_timezone()
        query_update_processos = """
            INSERT INTO processos(
            unidade_destino,
            recebido_em,
            status_terminado,
            link_processo,
            atualizado_em,
            campus,
            tipo_processo,
            mes_referente
            )
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
            """.format(
            movimentacao.unidade_destino,
            movimentacao.recebido_em,
            movimentacao.status_terminado,
            movimentacao.link_processo,
            timestamp, camp,
            processo, mes)

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

    def format_data(self, minus):
        mydate = datetime.datetime.now()
        month = mydate.month

        months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

        return months[month-minus]

    def format_timezone(self):
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        return utc_now.astimezone(pytz.timezone("America/Sao_Paulo"))
