from flask import jsonify, request, Flask
from app.main.service.processos_service import ProcessoService

app = Flask(__name__)

service = ProcessoService()


@app.route("/processos")
def get():
    try:
        auxilio = request.args.get("auxilio", "", str)
        campus = request.args.get("campus", "", str)

        results = service.get_processo(campus, auxilio)

        if results == None:
            return jsonify({'data': "Campos inválidos."})

        return jsonify({'data': results})
    except Exception as e:
        return jsonify({'data': "Algo deu errado. {}".format(str(e))})


@app.route("/keepalive")
def ping():
    return "ping!"
