from flask import Flask
from flask_restful import Api
from controllers.DatacreditoController import DatacreditoController
from controllers.StatusController import StatusController

app = Flask(__name__)
api = Api(app)

api.add_resource(StatusController, '/api/status')
api.add_resource(DatacreditoController, '/api/financial/accounts/<string:doc_type>/<string:doc_number>/<string:last_name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug= True)
