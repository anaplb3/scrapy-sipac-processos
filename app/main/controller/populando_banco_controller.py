from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, fields
from app.main.service.processos_service import ProcessoService
from app.main.bd.repository import environment_config, init_bd

api = Namespace('Populando banco', "Popular o banco.")

service = ProcessoService()

cfg = environment_config()


@api.route("")
class PopulandoBanco(Resource):
    def get(self):
        chave = request.args.get("chave", "", str)
        if chave == cfg["chave_populando"]:
            service.update_processos()
        else:
            return jsonify({'data': 'Chave incorreta'})
