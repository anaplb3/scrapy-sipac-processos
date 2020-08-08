from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, fields
from app.main.service.processos_service import ProcessoService

api = Namespace('Processo', "GET para os processos dos auxílios.")

service = ProcessoService()


@api.route("")
@api.doc(params={
    "auxilio": "Tipo de auxílio (auxilio_emergencial, auxilio_alimentacao_residencia, auxilio_alimentacao, auxilio_moradia, auxilio_residencia_rumf, auxilio_residencia_rufet, auxilio_residentes)",
    "campus": "Campus da UFPB referente ao auxílio (I, MANGABEIRA, II, III, IV)"
})
class Processo(Resource):
    def get(self):
        try:
            auxilio = request.args.get("auxilio", "", str)
            campus = request.args.get("campus", "", str)

            processo = service.get_processo(campus, auxilio)

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
