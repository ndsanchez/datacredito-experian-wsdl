from flask_restful import Resource
from services.Datacredito import Datacredito

class DatacreditoController(Resource):
    def get(self):
        datacredito = Datacredito()
        return datacredito.getAccounts('1', '1189213694', 'SANCHEZ')
