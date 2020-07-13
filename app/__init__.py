from app.main.controller.processos_controller import api as processo_namespace
from app.main.controller.keepalive_controller import api as keepalive_namespace
from app.main.controller.populando_banco_controller import api as populando_namespace
from flask import Flask, Blueprint, url_for
from flask_restx import Api, Resource, apidoc

url_prefix = "/api/v1"


class MyCustomApi(Api):

    def _register_apidoc(self, app: Flask) -> None:
        conf = app.extensions.setdefault('restplus', {})
        custom_apidoc = apidoc.Apidoc('restplus_doc', 'flask_restplus.apidoc',
                                      template_folder='templates', static_folder='static',
                                      static_url_path=url_prefix)

        @custom_apidoc.add_app_template_global
        def swagger_static(filename: str) -> str:
            return url_for('restplus_doc.static', filename=filename)

        if not conf.get('apidoc_registered', False):
            app.register_blueprint(custom_apidoc)
        conf['apidoc_registered'] = True


blueprint = Blueprint('api', __name__, url_prefix=url_prefix)

api = MyCustomApi(blueprint, version='1.0', doc="/docs")

api.add_namespace(processo_namespace, path="/processos")
api.add_namespace(keepalive_namespace, path="/keepalive")
api.add_namespace(populando_namespace, path="/populando")
