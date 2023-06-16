from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.signature import Signature
from zeep.wsse.username import UsernameToken
from Signature import CustomSignature
from dotenv import load_dotenv

import xml.etree.ElementTree as ET
import os

class Datacredito():
    def __init__(self):
        load_dotenv()

        self.wsdl_url = os.getenv('DATACREDITO_WSDL_URL')
        self.cerfile_path = os.getenv('CERTFILE_PATH')
        self.private_key_path = os.getenv('PRIVATE_KEY_PATH')
        self.okta_username = os.getenv('OKTA_USERNAME')
        self.okta_password = os.getenv('OKTA_PASSWORD')
        self.short_key = os.getenv('DATACREDITO_SHORT_KEY')
        self.user = os.getenv('DATACREDITO_USER')

        self.session = Session()
        self.session.cert = (cerfile_path, private_key_path)
        self.transport = Transport(session=session)

        self.wsse = Signature(private_key_path, cerfile_path)
        self.username_token = UsernameToken(okta_username, okta_password)

        self.client = Client(wsdl_url, wsse=CustomSignature([username_token, wsse]), transport=transport)

    def getAccounts(self, doc_type, doc_number):
        # metodos = dir(client.service)
        payload = {
            'clave': self.short_key,
            # 'identificacion':'70139881',
            # 'primerApellido':'MALDONADO',
            'identificacion':'1189213694',# 70139881, #1189213694
            'primerApellido':'SANCHEZ',
            'tipoIdentificacion':'1',
            'producto':'64',
            'usuario': self.user,
        }

        response = self.client.service.consultarHC2(solicitud=payload)

        if 'respuesta="13"' in response:
            tree = ET.ElementTree(ET.fromstring(response))
            root = tree.getroot()

            for account in root.findall("./Informe/CuentaAhorro"):
                print(account.attrib, '\n')

# print('Consulta OK - XML \n', response)