import app.main.bd.config as cfg
import psycopg2


def create_connection():
    return psycopg2.connect(
        host=cfg.POSTGRES_CFG['host'],
        port=cfg.POSTGRES_CFG['port'],
        user=cfg.POSTGRES_CFG['user'],
        password=cfg.POSTGRES_CFG['pwd']
    )


def create_connection_with_db():
    return psycopg2.connect(
        host=cfg.POSTGRES_CFG['host'],
        port=cfg.POSTGRES_CFG['port'],
        dbname=cfg.POSTGRES_CFG['dbname'],
        user=cfg.POSTGRES_CFG['user'],
        password=cfg.POSTGRES_CFG['pwd']
    )


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
    connection = create_connection()
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute(
        "SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'processos_sipac'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute('CREATE DATABASE processos_sipac')

    connection = create_connection_with_db()
    cursor = connection.cursor()

    create_table(cursor, connection)

    connection.close()
