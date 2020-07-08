from flask import jsonify, request, Flask
from app.main.service.processos_service import ProcessoService

app = Flask(__name__)

service = ProcessoService()


@app.route("/processos")
def get():
    json = request.get_json(force=True)

    try:
        auxilio = json['auxilio']
        campus = json['campus']

        return jsonify({'data': service.get_processo(campus, auxilio)})
    except Exception as e:
        return jsonify({'data': "Deu errado. {}".format(str(e))})


if __name__ == '__main__':
    # cron.start()
    # app.run(debug=True)
    service.update_processos()
