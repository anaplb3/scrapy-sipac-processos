from flask import jsonify, request, Flask
from flask_restx import Resource, Namespace, fields
from app.main.service.campus_service import CampusService

api = Namespace('Campus', "GET para os Campus disponíveis e seus auxílios.")

service = CampusService()


@api.route("")
class CampusList(Resource):
    def get(self):
        '''
        Retorna os campus disponíveis
        '''
        campus = service.get_all_campus()

        if campus == None or len(campus) == 0:
            return jsonify({'response':
                            {
                                'code': '503',
                                'message': 'Não foi possível retornar os campus disponíveis. Tente novamente mais tarde.',
                                'body': None
                            }
                            })

        return jsonify({'response':
                        {
                            'code': '200',
                            'message': 'Campus encontrados com sucesso!',
                            'body': campus
                        }
                        })


@api.route("/<string:id>/auxilios")
@api.doc(params={'id': 'id do campus'})
class Auxilios(Resource):
    def get(self, id):
        '''
        Retorna os auxílios do Campus passado no id
        '''

        auxilios = service.get_auxilios_from_id(id)

        if auxilios == None or len(auxilios) == 0:
            return jsonify({'response':
                            {
                                'code': '404',
                                'message': 'ID não encontrado.',
                                'body': None
                            }
                            })
        else:
            return jsonify({'response':
                            {
                                'code': '200',
                                'message': 'Auxílios encontrados com sucesso!',
                                'body': auxilios
                            }
                            })
