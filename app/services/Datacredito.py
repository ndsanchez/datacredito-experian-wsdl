from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.signature import Signature
from zeep.wsse.username import UsernameToken
from services.Signature import CustomSignature
from dotenv import load_dotenv

import xml.etree.ElementTree as ET
import os

class Datacredito():
    def __init__(self, okta_username, okta_password):
        try:
            load_dotenv()

            if okta_username != os.getenv('OKTA_USERNAME') or okta_password != os.getenv('OKTA_PASSWORD'):
                raise Exception('Forbidden')

            wsdl_url = os.getenv('DATACREDITO_WSDL_URL')
            cerfile_path = os.getenv('CERTFILE_PATH')
            private_key_path = os.getenv('PRIVATE_KEY_PATH')
            self.short_key = os.getenv('DATACREDITO_SHORT_KEY')
            self.user = os.getenv('DATACREDITO_USER')

            session = Session()
            session.cert = (cerfile_path, private_key_path)
            transport = Transport(session=session)

            wsse = Signature(private_key_path, cerfile_path)
            username_token = UsernameToken(okta_username, okta_password)

            self.client = Client(wsdl_url, wsse=CustomSignature([username_token, wsse]), transport=transport)
        except Exception as error:

            raise Exception({'code': 403, 'message': str(error)})

    def getAccounts(self, doc_type, doc_number, last_name):
        try:
            accounts = []
            payload = {
                'clave': self.short_key,
                'identificacion': doc_number,
                'primerApellido': last_name,
                'tipoIdentificacion': doc_type,
                'producto':'64',
                'usuario': self.user,
            }

            response = self.client.service.consultarHC2(solicitud=payload)

            if 'respuesta="13"' in response:
                tree = ET.ElementTree(ET.fromstring(response))
                root = tree.getroot()

                for account in root.findall("./Informe/CuentaAhorro"):
                    state = account.find('./Estado').attrib
                    account = account.attrib
                    accounts.append({ **account, **state })

            return accounts
        except Exception as error:

            raise Exception({'code': 400, 'message': str(error)})
