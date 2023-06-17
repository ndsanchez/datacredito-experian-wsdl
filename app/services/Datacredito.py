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
    ## Constructor
    def __init__(self, okta_username, okta_password):
        try:
            ## cargar las variables de entorno que luego pueden ser accedidas desde os
            load_dotenv()

            ## Verificar si el usuario y password enviado en los headers son correctos
            if okta_username != os.getenv('OKTA_USERNAME') or okta_password != os.getenv('OKTA_PASSWORD'):
                raise Exception('Forbidden')

            ## Obtener variables del servicio soap, certificados, usuario y password
            wsdl_url = os.getenv('DATACREDITO_WSDL_URL')
            cerfile_path = os.getenv('CERTFILE_PATH')
            private_key_path = os.getenv('PRIVATE_KEY_PATH')
            self.short_key = os.getenv('DATACREDITO_SHORT_KEY')
            self.user = os.getenv('DATACREDITO_USER')

            ## Crear la session con el certificado publico y llave privada
            session = Session()
            session.cert = (cerfile_path, private_key_path)
            transport = Transport(session=session)

            ## Crear la firma con el certificado publico y llave privada
            wsse = Signature(private_key_path, cerfile_path)
            username_token = UsernameToken(okta_username, okta_password)

            ## Construir el cliente soap con la firma y el TLS
            self.client = Client(wsdl_url, wsse=CustomSignature([username_token, wsse]), transport=transport)
        except Exception as error:

            raise Exception({'code': 403, 'message': str(error)})

    ## Obtener las cuentas bancarias de la persona
    def getAccounts(self, doc_type, doc_number, last_name):
        try:
            ## Crear variable para la solicitud
            accounts = []
            payload = {
                'clave': self.short_key,
                'identificacion': doc_number,
                'primerApellido': last_name,
                'tipoIdentificacion': doc_type,
                'producto':'64',
                'usuario': self.user,
            }

            ## Realiza la peticion usando el cliente soap construido en el __init__
            response = self.client.service.consultarHC2(solicitud=payload)

            ## si respuesta="13" esta incluido en la respuesta, entonces encontro informacion de la persona
            if 'respuesta="13"' in response:
                ## convierte la respuesta string a xml
                tree = ET.ElementTree(ET.fromstring(response))
                root = tree.getroot()

                ## para cada elemento CuentaAhorro en el xml
                for account in root.findall("./Informe/CuentaAhorro"):
                    ## Obtenga los atributos del elemento CuentaAhorro
                    ## Obtenga el child Estado y obtenga sus atributos (Estado de la cuenta <Activa> <Inactiva>)
                    state = account.find('./Estado').attrib
                    account = account.attrib
                    accounts.append({ **account, **state })

            return accounts
        except Exception as error:

            raise Exception({'code': 400, 'message': str(error)})

    ## Obtener xml con toda la informacion financiera
    def getXml(self, doc_type, doc_number, last_name):
        try:
            ## Crear variable para la solicitud
            accounts = []
            payload = {
                'clave': self.short_key,
                'identificacion': doc_number,
                'primerApellido': last_name,
                'tipoIdentificacion': doc_type,
                'producto':'64',
                'usuario': self.user,
            }

            ## Realiza la peticion usando el cliente soap construido en el __init__
            return self.client.service.consultarHC2(solicitud=payload)
        except Exception as error:

            raise Exception({'code': 400, 'message': str(error)})
