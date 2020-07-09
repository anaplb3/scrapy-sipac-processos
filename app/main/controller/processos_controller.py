from flask import jsonify, request, Flask
from app.main.service.processos_service import ProcessoService

app = Flask(__name__)

service = ProcessoService()


@app.route("/processos")
def get():

    try:
        json = request.get_json(force=True)
        auxilio = json['auxilio']
        campus = json['campus']

        return jsonify({'data': service.get_processo(campus, auxilio)})
    except Exception as e:
        return jsonify({'data': "Deu errado. {}".format(str(e))})
