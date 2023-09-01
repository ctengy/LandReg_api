import sys 
sys.path.append(r'.')#將上級目錄加入path

import requests
from logics.exceptions import *

class Get_token(object):

    TokenUrl = "https://api.land.moi.gov.tw/cp/getToken"
    Token = ""
    ClientID = ''
    SecretCode = ''
    
    def __init__(self,ClientID = None,SecretCode = None,TokenUrl = None) -> None:
        self.ClientID = ClientID
        self.SecretCode = SecretCode

        if TokenUrl is None: 
            TokenUrl = self.TokenUrl

    def request_token(self) -> str:
        try:
            if all((self.ClientID,self.SecretCode)):
                response = requests.get(self.TokenUrl, auth=(f'{self.ClientID}', f'{self.SecretCode}'))
                print(response.status_code)
                res_obj = response.json()
                self.Token = res_obj['access_token']

                return self.Token
            else:
                raise GetTokenFialed("ID and SecretCode is EMPTY")
            
        except GetTokenFialed as e:
            raise GetTokenFialed('request token issue')
        
        except requests.exceptions.JSONDecodeError as e:
            raise GetTokenFialed(f'解析錯誤\n狀態碼:{response.status_code}\n回傳:{response.text}')


if __name__ == "__main__":
    a = Get_token(ClientID='user',SecretCode='pass',TokenUrl= 'https://authenticationtest.com/HTTPAuth/')
    a.request_token()