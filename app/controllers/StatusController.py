from flask_restful import Resource

class StatusController(Resource):
    def get(self):
        return {'status': 'success', 'message': 'success'}
