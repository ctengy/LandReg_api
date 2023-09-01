import sys 
sys.path.append(r'.')#將上級目錄加入path

import requests
from logics.Exceptions import *

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
        
        self.request_token()

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
            print('request token issue')
            return None
        
        except requests.exceptions.JSONDecodeError as e:
            print (f'解析錯誤\n狀態碼:{response.status_code}\n回傳:{response.text}')
            return None


if __name__ == "__main__":
    def case1():
        a = Get_token(ClientID='user',SecretCode='pass',TokenUrl= 'https://authenticationtest.com/HTTPAuth/')
        a.request_token()
    def case2():
        a = Get_token()
    
    # print(case2())