import psycopg2
import os
from config import DEV_CFG, PROD_CFG


def environment_config():
    if os.environ['ENV'] == 'prod':
        return PROD_CFG
    else:
        return DEV_CFG


def create_table(cursor, connection):
    query_create_table_processos = """
        CREATE TABLE IF NOT EXISTS processos(
            id_processo SERIAL PRIMARY KEY,
            id_auxilio INTEGER REFERENCES auxilios(id_auxilio),
            id_campus INTEGER REFERENCES campus(id_campus),
            unidade_destino VARCHAR NOT NULL,
            recebido_em VARCHAR NOT NULL,
            status_terminado BOOLEAN NOT NULL,
            link_processo VARCHAR NOT NULL,
            atualizado_em TIMESTAMP NOT NULL,
            proxima_atualizacao_em TIMESTAMP NOT NULL,
            campus VARCHAR NOT NULL,
            tipo_processo VARCHAR NOT NULL,
            mes_referente VARCHAR NOT NULL
        )
    """

    query_create_table_campus = """
        CREATE TABLE IF NOT EXISTS campus (
            id_campus SERIAL PRIMARY KEY,
            campus VARCHAR NOT NULL
        )
    """

    query_create_table_auxilios = """
        CREATE TABLE IF NOT EXISTS auxilios (
            id_auxilio SERIAL PRIMARY KEY,
            id_campus INTEGER REFERENCES campus(id_campus),
            tipo_auxilio VARCHAR NOT NULL,
            nome_visualizacao VARCHAR NOT NULL
        )
    """

    query_create_table_processos_anteriores = """
        CREATE TABLE IF NOT EXISTS processos_anteriores (
            id_auxilio_anterior SERIAL PRIMARY KEY,
            id_auxilio INTEGER REFERENCES auxilios(id_auxilio),
            id_campus INTEGER REFERENCES campus(id_campus),
            link_processo VARCHAR NOT NULL,
            campus VARCHAR NOT NULL,
            tipo_processo VARCHAR NOT NULL,
            mes_referente VARCHAR NOT NULL
        )
    """

    query_create_table_excluded_students = """"
     
    """

    cursor.execute(query_create_table_campus)
    cursor.execute(query_create_table_auxilios)
    cursor.execute(query_create_table_processos)
    cursor.execute(query_create_table_processos_anteriores)
    connection.commit()


def is_tables_empty(cursor):
    cursor.execute("select exists (select 1 from campus)")
    status_campus = list(cursor.fetchone())[0]
    cursor.execute("select exists (select 1 from auxilios)")
    status_auxilios = list(cursor.fetchone())[0]
    return status_campus and status_auxilios


def insert_campus_values(cursor, connection):
    campus = ["I", "II", "III", "IV", "MANGABEIRA"]
    insert = """INSERT INTO campus (
        campus) VALUES ('{}')"""

    for camp in campus:
        cursor.execute(insert.format(camp))

    connection.commit()


def get_campus_id(cursor, campus):
    query = """SELECT id_campus FROM campus WHERE campus = '{}'""".format(
        campus)
    cursor.execute(query)
    return list(cursor.fetchone())[0]


def get_auxilio_id(cursor, id_campus, tipo_auxilio):
    query = """ SELECT id_auxilio 
        FROM auxilios
        WHERE id_campus = {} and tipo_auxilio = '{}'""".format(id_campus, tipo_auxilio)
    cursor.execute(query)
    res = cursor.fetchone()
    return res[0]


def insert_auxilios_values(cursor, connection):
    processos_campus_I = ["auxilio_emergencial", "auxilio_alimentacao", "auxilio_moradia", "auxilio_residencia_rumf",
                          "auxilio_residencia_rufet", "auxilio_creche"]
    processos_campus_II = ["auxilio_emergencial",
                           "auxilio_alimentacao_residencia", "auxilio_moradia", "auxilio_creche"]
    processos_campus_III = ["auxilio_emergencial", "auxilio_alimentacao_residencia",
                            "auxilio_moradia", "auxilio_emergencial_complementar", "auxilio_creche"]
    processos_campus_IV = ["auxilio_emergencial", "auxilio_alimentacao_residencia",
                           "auxilio_alimentacao", "auxilio_moradia", "auxilio_creche"]
    processo_campus_mangabeira = ["auxilio_residentes", "auxilio_creche"]

    insert_auxilio_value(cursor, processos_campus_I, "I")
    insert_auxilio_value(cursor, processos_campus_II, "II")
    insert_auxilio_value(cursor, processos_campus_III, "III")
    insert_auxilio_value(cursor, processos_campus_IV, "IV")
    insert_auxilio_value(cursor, processo_campus_mangabeira, "MANGABEIRA")
    connection.commit()


def insert_auxilio_value(cursor, auxilios, campus):
    insert = """INSERT INTO auxilios (id_campus, tipo_auxilio, nome_visualizacao)
    VALUES ({}, '{}', '{}')"""
    for aux in auxilios:
        camp_id = get_campus_id(cursor, campus)
        cursor.execute(insert.format(
            camp_id, aux, get_visualization_name(aux)))


def get_visualization_name(auxilio):
    if (auxilio == 'auxilio_emergencial'):
        return "Pecúnia Emergencial Alimentação"
    elif (auxilio == 'auxilio_alimentacao'):
        return "Aux. Alimentação"
    elif (auxilio == 'auxilio_moradia'):
        return "Aux. Moradia"
    elif (auxilio == 'auxilio_residencia_rumf'):
        return "Aux. Residência Universitária RUMF"
    elif (auxilio == 'auxilio_residencia_rufet'):
        return "Aux. Residência Universitária RUFET"
    elif (auxilio == 'auxilio_alimentacao_residencia'):
        return "Aux. Residência Universitária"
    elif (auxilio == 'auxilio_residentes'):
        return "Aux. Alimentação Residentes Mangabeira e Santa Rita"
    elif (auxilio == 'auxilio_emergencial_complementar'):
        return "Pecúnia Emergencial Alimentação Complementar"
    elif (auxilio == 'auxilio_creche'):
        return "Aux. Creche"


def init_bd():
    cfg = environment_config()
    connection = psycopg2.connect(cfg["database_url"], sslmode=cfg["sslmode"])
    cursor = connection.cursor()

    create_table(cursor, connection)

    if not is_tables_empty(cursor):
        insert_campus_values(cursor, connection)
        insert_auxilios_values(cursor, connection)
    connection.close()
