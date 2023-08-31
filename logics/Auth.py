import requests
import base64
import json
from logics.exceptions import *

class Get_token(object):

    TokenUrl = "https://api.land.moi.gov.tw/cp/getToken"
    Token = ""
    ClientID = ''
    SecretCode = ''


    def __init__(self,ClientID = '',SecretCode = '') -> None:
        self.ClientID = ClientID
        self.SecretCode = SecretCode

    def request_token(self):
        try:
            if all((self.ClientID,self.SecretCode)):
                credentials = f"{self.ClientID}:{self.SecretCode}"
                cred_bytes = credentials.encode('ascii')
                cred_base64 = base64.b64encode(cred_bytes).decode('utf-8')
                headers = {
                    "Authorization": f"Basic {cred_base64}",
                    "Content-Type": "application/json; charset=utf-8"
                }
                response = requests.get(self.TokenUrl, headers=headers)
                res_obj = response.json()
                self.Token = res_obj['access_token']

                return self.Token
            else:
                raise GetTokenFialed("ID and SecretCode is EMPTY")
            
        except GetTokenFialed as e:
            raise GetTokenFialed('request token issue')


