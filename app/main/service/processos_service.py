from datetime import datetime, timedelta
import pytz
from app.main.web_scrapy.sipac_selenium import open
from app.main.web_scrapy.soupbib import get_processos
from app.main.bd import repository
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
                     "auxilio_alimentacao", "auxilio_moradia", "auxilio_creche"]
        campus = ["I", "II", "III", "IV"]

        for processo in processos:
            for camp in campus:
                ano = datetime.now().year
                mes = "{}/{}".format(self.find_month_in_db(processo, camp), ano)

                if self.auxilios_inexistentes(processo, camp):
                    continue
                try:
                    resultados_selenium = open(processo, camp, mes)
                    movimentacao = get_processos(
                        resultados_selenium[0], resultados_selenium[1])

                    if movimentacao == None:
                        continue
                    else:
                        self.execute_update(
                            movimentacao, camp, processo, mes)
                except Exception as e:
                    print(
                        "ProcessosServiceError in update_processos: {}".format(str(e)))
                    continue
        self.auxilios_campus_I()
        self.auxilio_complementar_campus_III()

    def find_month_in_db(self, auxilio, campus):
        query = """SELECT status_terminado, mes_referente FROM processos 
        WHERE tipo_processo = '{}' AND campus = '{}'""".format(auxilio, campus)
        self.cursor.execute(query)

        resultado = list(self.cursor.fetchall())
        if len(resultado) == 0:
            if auxilio == "auxilio_emergencial" or "auxilio_emergencial_complementar":
                return "Agosto"
            return "Setembro"
        else:
            status = resultado[0][0]
            mes_referente = resultado[0][1].split("/")[0]
            return self.get_month(status, mes_referente)

    def get_month(self, status, mes_referente):
        months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        index = months.index(mes_referente)
        if status:
            try:
                return months[index + 1]
            except:
                return months[0]
        else:
            return mes_referente

    def get_next_update(self, timestamp):
        br = pytz.timezone("America/Sao_Paulo")
        minutes = 30

        if ((timestamp.weekday() == 4) and ((timestamp.hour - 3) >= 17) and (timestamp.minute >= 30)):
            days = 3
            tmp = timestamp + timedelta(days=days)
            hours = 9
            return br.localize(tmp - timedelta(hours=hours, minutes=30))

        elif ((timestamp.hour - 3) == 18):
            hours = 14
            return br.localize(timestamp + timedelta(hours=hours))

        return br.localize(timestamp + timedelta(minutes=minutes))

    def auxilio_complementar_campus_III(self):
        processo = "auxilio_emergencial_complementar"
        campus = "III"
        ano = datetime.now().year
        mes = "{}/{}".format(self.find_month_in_db(processo, campus), ano)
        try:
            resultados_selenium = open(processo, campus, mes)
            movimentacao = get_processos(
                resultados_selenium[0], resultados_selenium[1])
            if movimentacao == None:
                raise Exception
            else:
                self.execute_update(movimentacao, campus, processo, mes)
        except Exception as e:
            print(
                "ProcessosServiceError in auxilio_complementar_campus_III: {}".format(str(e)))

    def auxilios_campus_I(self):
        processos = ["auxilio_residencia_rumf",
                     "auxilio_residencia_rufet", "auxilio_residentes"]
        campus = "I"
        ano = datetime.now().year

        for processo in processos:
            mes = "{}/{}".format(self.find_month_in_db(processo, campus), ano)

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
                print("ProcessosServiceError in auxilios_campus_I: {}".format(str(e)))
                continue

    def auxilios_inexistentes(self, auxilio, camp):
        if (auxilio == "auxilio_alimentacao" and camp == "III") or (auxilio == "auxilio_alimentacao" and camp == "II") or (auxilio == "auxilio_alimentacao_residencia" and camp == "I"):
            return True
        else:
            return False

    def execute_update(self, movimentacao, camp, processo, mes):
        timestamp = datetime.today()
        proxima_atualizacao = self.get_next_update(timestamp)
        query_update_processos = """
            UPDATE processos
            SET unidade_destino = '{}',
            recebido_em = '{}',
            status_terminado = '{}',
            link_processo = '{}',
            atualizado_em = '{}',
            proxima_atualizacao_em = '{}',
            campus = '{}',
            tipo_processo = '{}',
            mes_referente = '{}'
            WHERE tipo_processo = '{}' and campus = '{}'
            """.format(
            movimentacao.unidade_destino,
            movimentacao.recebido_em,
            movimentacao.status_terminado,
            movimentacao.link_processo,
            timestamp, proxima_atualizacao,
            camp,
            processo, mes,
            processo, camp)
        try:
            self.cursor.execute(query_update_processos)
        except Exception as e:
            print("query in execute_update: {}".format(query))
            print("ProcessoServiceError in execute_update: {}".format(str(e)))
        self.connection.commit()

    def execute_insert(self, movimentacao, camp, processo, mes):
        timestamp = datetime.today()
        proxima_atualizacao = self.get_next_update(timestamp)
        query_update_processos = """
            INSERT INTO processos(
            unidade_destino,
            recebido_em,
            status_terminado,
            link_processo,
            atualizado_em,
            proxima_atualizacao_em,
            campus,
            tipo_processo,
            mes_referente
            )
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
            """.format(
            movimentacao.unidade_destino,
            movimentacao.recebido_em,
            movimentacao.status_terminado,
            movimentacao.link_processo,
            timestamp, proxima_atualizacao,
            camp,
            processo, mes)

        self.cursor.execute(query_update_processos)
        self.connection.commit()

    def get_processo(self, campus, auxilio):
        if campus == "" or auxilio == "":
            return None
        query = """SELECT unidade_destino, recebido_em, 
        status_terminado, link_processo, atualizado_em, proxima_atualizacao_em,
        mes_referente FROM processos 
        WHERE tipo_processo = '{}' and campus = '{}' """.format(auxilio, campus)
        try:
            self.cursor.execute(query)
        except Exception as e:
            print("query in get_processo: {}".format(query))
            print("ProcessosServiceError in get_processo: {}. Tentando novamente.".format(
                str(e)))
            self.connection.rollback()
            self.cursor.execute(query)
        processo = list(self.cursor.fetchone())

        return MovimentacaoProcessoDTO(processo[0], processo[1],
                                       processo[2], processo[3],
                                       processo[4], processo[5],
                                       auxilio, campus,
                                       processo[6])
