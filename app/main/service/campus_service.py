from app.main.bd import repository
import psycopg2
from app.main.model.model import CampusDTO, AuxilioDTO


class CampusService:
    def __init__(self):
        cfg = repository.environment_config()
        self.connection = psycopg2.connect(
            cfg["database_url"], sslmode=cfg["sslmode"])
        self.cursor = self.connection.cursor()

    def get_all_campus(self):
        query = """SELECT id_campus, campus
        FROM campus
        """
        self.cursor.execute(query)
        campus_list = list(self.cursor.fetchall())

        campus_dto_list = []
        for camp in campus_list:
            dto = CampusDTO(camp[0], camp[1])
            campus_dto_list.append(dto.serialize())

        return campus_dto_list

    def get_auxilios_from_id(self, id):
        query = """ SELECT id_auxilio, id_campus, tipo_auxilio, nome_visualizacao 
        FROM auxilios
        WHERE id_campus = {}
        """.format(id)
        try:
            self.cursor.execute(query)
        except:
            self.cursor.rollback()

        auxilios_list = list(self.cursor.fetchall())
        auxilios_dto_list = []

        for auxilio in auxilios_list:
            dto = AuxilioDTO(auxilio[0], auxilio[1], auxilio[2], auxilio[3])
            auxilios_dto_list.append(dto.serialize())

        return auxilios_dto_list
