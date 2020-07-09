from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, fields

api = Namespace('KeepAlive', "GET para manter a api ativa")


@api.route("")
class KeepAlive(Resource):
    def get(self):
        return "ping!"
