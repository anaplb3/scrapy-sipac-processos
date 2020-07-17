import psycopg2
import os
from config import DEV_CFG, PROD_CFG


def environment_config():
    if os.environ['ENV'] == 'prod':
        return PROD_CFG
    else:
        return DEV_CFG


def create_table(cursor, connection):
    query_create_table = """
        CREATE TABLE IF NOT EXISTS processos(
            id SERIAL PRIMARY KEY,
            unidade_destino VARCHAR NOT NULL,
            recebido_em VARCHAR NOT NULL,
            status_terminado BOOLEAN NOT NULL,
            link_processo VARCHAR NOT NULL,
            atualizado_em TIMESTAMP NOT NULL,
            campus VARCHAR NOT NULL,
            tipo_processo VARCHAR NOT NULL,
            mes_referente VARCHAR NOT NULL
        )
    """

    cursor.execute(query_create_table)
    connection.commit()


def init_bd():
    cfg = environment_config()
    connection = psycopg2.connect(cfg["database_url"], sslmode=cfg["sslmode"])
    cursor = connection.cursor()

    cursor.execute("DROP TABLE processos")
    connection.commit()

    create_table(cursor, connection)

    connection.close()
