from flask import abort, jsonify, make_response, request
from flask_restful import Resource
from services.Datacredito import Datacredito
from werkzeug.exceptions import BadRequest

class DatacreditoController(Resource):
    def get(self, doc_type, doc_number, last_name):
        try:
            okta_username = request.headers.get('okta-user')
            okta_password = request.headers.get('okta-password')

            if not okta_username or not okta_password:
                raise Exception({'code': 403, 'message': 'Forbidden'})

            datacredito = Datacredito(okta_username, okta_password)
            response = datacredito.getAccounts(doc_type, doc_number, last_name) #'1', '1189213694', 'SANCHEZ'

            return {'status_code': 200, 'data': response}
        except Exception as e:

            message = e.args[0].get('message', 'Server error')
            code = e.args[0].get('code', 500)
            return make_response(jsonify({'status_code': code, 'message': message}), code)
