import app.main.bd.config as cfg
import psycopg2
import subprocess


def create_conn():
    proc = subprocess.Popen('heroku config:get DATABASE_URL -a consultaprocessosipac', stdout=subprocess.PIPE, shell=True)
    db_url = proc.stdout.read().decode('utf-8').strip()
    return psycopg2.connect(db_url)


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
    connection = create_conn()
    cursor = connection.cursor()

    create_table(cursor, connection)

    connection.close()
