from flask_restful import Resource

class StatusController(Resource):
    def get(self):

        return {'status_code': 200, 'message': 'success'}
