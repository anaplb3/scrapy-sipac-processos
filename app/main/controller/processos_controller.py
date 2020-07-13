from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, fields
from app.main.service.processos_service import ProcessoService

api = Namespace('Processo', "GET para os processos dos auxílios.")

service = ProcessoService()


@api.route("")
@api.doc(params={
    "auxilio": "Tipo de auxílio (auxilio_emergencial, auxilio_alimentacao_res, auxilio_alimentacao, auxilio_moradia)",
    "campus": "Campus da UFPB referente ao auxílio (I, II, III, IV)"
})
class Processo(Resource):
    def get(self):
        try:
            auxilio = request.args.get("auxilio", "", str)
            campus = request.args.get("campus", "", str)

            processo = service.get_processo(campus, auxilio)

            if processo == None:
                return jsonify({'data': "Campos inválidos."})

            return jsonify({'data': processo.serialize()})
        except Exception as e:
            return jsonify({'data': "Algo deu errado. {}".format(str(e))})
