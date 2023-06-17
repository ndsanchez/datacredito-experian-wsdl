from flask import abort, jsonify, make_response, request
from flask_restful import Resource
from services.Datacredito import Datacredito
from werkzeug.exceptions import BadRequest

class DatacreditoController(Resource):
    def get(self, doc_type, doc_number, last_name):
        try:
            ## obtenga las credenciales okta de los headers de la solicitud
            okta_username = request.headers.get('okta-user')
            okta_password = request.headers.get('okta-password')

            if not okta_username or not okta_password:
                raise Exception({'code': 403, 'message': 'Forbidden'})

            ## Instancia la clase Datacredito e invoca el metodo para obtener las cuentas bancarias
            ## asociadas al tipo de documento, numero de documento y apellido de la persona
            datacredito = Datacredito(okta_username, okta_password)
            response = datacredito.getAccounts(doc_type, doc_number, last_name)

            return {'status_code': 200, 'data': response}
        except Exception as e:

            ## manejo de errores
            message = e.args[0].get('message', 'Server error')
            code = e.args[0].get('code', 500)
            return make_response(jsonify({'status_code': code, 'message': message}), code)

    def post(self, doc_type, doc_number, last_name):
        try:
            ## obtenga las credenciales okta de los headers de la solicitud
            okta_username = request.headers.get('okta-user')
            okta_password = request.headers.get('okta-password')

            if not okta_username or not okta_password:
                raise Exception({'code': 403, 'message': 'Forbidden'})

            ## Instancia la clase Datacredito e invoca el metodo para obtener las cuentas bancarias
            ## asociadas al tipo de documento, numero de documento y apellido de la persona
            datacredito = Datacredito(okta_username, okta_password)
            response = datacredito.getXml(doc_type, doc_number, last_name)

            return {'status_code': 200, 'data': response}
        except Exception as e:

            ## manejo de errores
            message = e.args[0].get('message', 'Server error')
            code = e.args[0].get('code', 500)
            return make_response(jsonify({'status_code': code, 'message': message}), code)
