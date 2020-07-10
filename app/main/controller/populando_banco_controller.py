from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, fields
from app.main.service.processos_service import ProcessoService

api = Namespace('Populando Banco', "GET para popular banco (apenas teste)")

service = ProcessoService()


@api.route("")
class PopulandoBanco(Resource):
    def get(self):
        service.update_processos()
        return jsonify({'data': "Populando banco"})
