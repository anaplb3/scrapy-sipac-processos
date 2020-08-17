from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, fields
from app.main.service.processos_service import ProcessoService

api = Namespace('Processos Anteriores',
                "GET para os processos dos auxílios do mês anterior.")

service = ProcessoService()


@api.route("")
@api.doc(params={
    "id_auxilio": "Id do auxílio",
    "id_campus": "Id do campus"
})
class Processo(Resource):
    def get(self):
        try:
            id_auxilio = request.args.get("id_auxilio", "", int)
            id_campus = request.args.get("id_campus", "", int)

            processo = service.get_processo_anterior(id_campus, id_auxilio)

            if processo == None:
                return jsonify({'response':
                                {
                                    'code': '404',
                                    'message': 'Campos inválidos',
                                    'body': None
                                }
                                })

            return jsonify({'response':
                            {
                                'code': '200',
                                'message': 'Auxílio encontrado com sucesso.',
                                'body': processo.serialize()
                            }
                            })

        except Exception as e:
            return jsonify({'response':
                            {
                                'code': '500',
                                'message': 'Algo deu errado. {}'.format(str(e)),
                                'body': None
                            }
                            })
