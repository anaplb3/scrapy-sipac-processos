import psycopg2
import os


def create_conn():
    return os.environ['DATABASE_URL']


def create_table(cursor, connection):
    query_create_table = """
        CREATE TABLE IF NOT EXISTS processos(
            id SERIAL PRIMARY KEY,
            data_origem VARCHAR NOT NULL,
            unidade_origem VARCHAR NOT NULL,
            unidade_destino VARCHAR NOT NULL,
            recebido_em VARCHAR NOT NULL,
            atualizado_em TIMESTAMP NOT NULL,
            campus VARCHAR NOT NULL,
            tipo_processo VARCHAR NOT NULL,
            mes_referente VARCHAR NOT NULL
        )
    """

    cursor.execute(query_create_table)
    connection.commit()


def init_bd():
    connection = psycopg2.connect(create_conn(), sslmode='require')
    cursor = connection.cursor()

    create_table(cursor, connection)

    connection.close()
