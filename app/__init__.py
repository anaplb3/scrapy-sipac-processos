from app.main.controller.processos_controller import api as processo_namespace
from app.main.controller.keepalive_controller import api as keepalive_namespace
from app.main.controller.populando_banco_controller import api as populando_namespace
from app.main.controller.campus_controller import api as campus_namespace
from app.main.controller.processos_anteriores_controller import api as processo_anterior_namespace
from flask import Blueprint
from flask_restx import Api, apidoc

url_prefix = "/api/v1"
apidoc.url_prefix = url_prefix

blueprint = Blueprint('api', __name__, url_prefix=url_prefix)

api = Api(blueprint, version='1.0', doc="/docs")

api.add_namespace(processo_namespace, path="/processos")
api.add_namespace(keepalive_namespace, path="/keepalive")
api.add_namespace(populando_namespace, path="/populando")
api.add_namespace(campus_namespace, path="/campus")
api.add_namespace(processo_anterior_namespace, path="/processos-anteriores")
