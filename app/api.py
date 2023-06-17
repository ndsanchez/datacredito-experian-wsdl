from flask import Flask
from flask_restful import Resource, Api
from services.Datacredito import Datacredito

app = Flask(__name__)
api = Api(app)

class DatacreditoController(Resource):
    def get(self):
        datacredito = Datacredito()
        return datacredito.getAccounts('1', '1189213694', 'SANCHEZ')

api.add_resource(DatacreditoController, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug= True)
