import datetime
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

        processos = ["auxilio_emergencial", "auxilio_alimentacao_res",
                     "auxilio_alimentacao", "auxilio_moradia"]
        campus = ["I", "II", "III", "IV"]

        for processo in processos:
            for camp in campus:
                ano = datetime.datetime.now().year
                mes = "{}/{}".format(self.format_data(1), ano)
                if processo == "auxilio_emergencial":
                    mes = "{}/{}".format(self.format_data(2), ano)

                print("processo = {} | campus = {} | referente a = {}".format(
                    processo, camp, mes))

                if processo == "auxilio_alimentacao" and camp == "II":
                    continue
                try:
                    resultados = get_processos(open(processo, camp, mes))
                    if resultados == None:
                        continue
                    else:
                        for mov in resultados:
                            self.execute_update(mov, camp, processo, mes)
                except:
                    break

    def execute_update(self, mov, camp, processo, mes):
        timestamp = datetime.datetime.today()
        query_update_processos = """
            INSERT INTO processos(
            data_origem,
            unidade_origem,
            unidade_destino,
            recebido_em,
            atualizado_em,
            campus,
            tipo_processo,
            mes_referente
            )
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
            """.format(
            mov.data_origem,
            mov.unidade_origem,
            mov.unidade_destino,
            mov.recebido_em,
            timestamp, camp,
            processo, mes)

        self.cursor.execute(query_update_processos)
        self.connection.commit()

    def get_processo(self, campus, auxilio):
        query = """SELECT data_origem, unidade_origem, unidade_destino, recebido_em, atualizado_em FROM processos 
        WHERE tipo_processo = '{}' and campus = '{}' """.format(auxilio, campus)
        self.cursor.execute(query)
        processo = list(self.cursor.fetchall())

        results = []

        for movimentacao in processo:
            if '<td' in movimentacao[0]:
                continue
            else:
                mov = MovimentacaoProcessoDTO(movimentacao[0], movimentacao[1],
                                              movimentacao[2], movimentacao[3],
                                              movimentacao[4], auxilio, campus)
                results.append(mov.serialize())

        return results

    def format_data(self, minus):
        mydate = datetime.datetime.now()
        month = mydate.month

        months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

        return months[month-minus]
