import requests

# 自定義異常
from logics.Exceptions import InvalidInputException, RequestFailedException, FormatFailedException

class QueryObject(object):#搜尋的父類別，定義了每次搜尋的流程:檢查token及參數、發送request、提取回傳資料 

    url = None
    def __init__(self,token= None,**kwargs) -> None:
        self.token = token
        if all(kwargs.values()):#檢查查詢參數及token並建構requst header及body
            self.request_body = [kwargs]
            self.request_headers = {
                        "Content-Type":"text/plain",
                        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                        "Accept": "*/*",
                        "Cache-Control": "no-cache",
                        "Host":"api.land.moi.gov.tw",
                        "Accept-Encoding":"gzip, deflate, br",
                        "Connection":"keep-alive",
                        'Authorization': f'Bearer {self.token}'

                    } 

        else:
            raise InvalidInputException("Input parameters are not complete")
    
    def send_request(self,request_headers = None,request_body = None):

            if request_body is None:
                request_body = self.request_body

            if request_headers is None:
                request_headers = self.request_headers

            try:         
                url = self.url
                response = requests.post(url, json=request_body, headers=request_headers)
                response.raise_for_status()
                if response.status_code == 200:
                    response_data = response.json()
                    raw_data = response_data
                    return raw_data
                
                elif response.status_code == 401:
                    raise RequestFailedException(f'身分認證失敗:{response.status_code}')
                
                else:
                    raise RequestFailedException(f'失敗狀態碼:{response.status_code}')

        
            except requests.exceptions.RequestException as e:
                raise RequestFailedException(f"Request failed with error: {e}")

    def format_data(self, raw_data):
        formatted_data = raw_data
        return formatted_data

    def run(self):
        try:
            raw_data = self.send_request()
            send_back_data = self.format_data(raw_data)
            return send_back_data

        except InvalidInputException as e:
            return str(e)

        except RequestFailedException as e:
            return str(e)

        except FormatFailedException as e:
            return f"An unexpected error occurred:,\n, {e}"

class LandDescriptionQuery(QueryObject):#土地標示部搜尋的子類別，定義要求api的網址，rewrite format_data方法
    url = "https://api.land.moi.gov.tw/sandbox/api/LandDescription/1.0/QueryByLandNo"

    # 標示部查詢
    def __init__(self, token='',UNIT='', SEC='', NO='') -> None:
        super().__init__(token=token,UNIT=UNIT, SEC=SEC, NO=NO)
    
    def format_data(self, raw_data):
        #對照表
        field_mapping = {
            "RDATE": "登記日期(年月日)",
            "REASON": "登記原因",
            "AREA": "面積",
            "ZONING": "使用分區",
            "LCLASS": "使用地類別",
            "ALVALUE": "公告地現值",
            "ALPRICE": "公告地價",
            "COUNTY": "縣市",
            "DISTRICT": "鄉鎮市區",
            "Y_COORDINATE": "視中心縱坐標",
            "X_COORDINATE": "視中心橫坐標",
            "MAPSHEET": "圖幅號",
            "BUILDINGCOUNT": "地上建物建號數量",
            "OTHERREG": "其他登記事項",
            "NUMBER": "其他登記事項序號",
            "CATEGORY": "其他登記事項代碼",
            "CONTENT": "其他登記事項內容",

        }   
        if raw_data['QUANTITY'] != 0:
            formatted_LANDREG = {}  # 存储格式化后的数据
            formatted_OTHERREG = {}
            try:
                if raw_data and isinstance(raw_data, dict):
                    response = raw_data.get("RESPONSE", "無回應")
       
                    result_dic_discripe = response[0]["LANDREG"]

                    for result in result_dic_discripe:
                        #當OTHERREG有值時處理OTHERREG
                        if result =='OTHERREG' and any(result_dic_discripe['OTHERREG']) :
                            ressult_dic = result_dic_discripe['OTHERREG'][0]#list中的dic值
                            for otherreg in ressult_dic:
                                formatted_OTHERREG[field_mapping.get(otherreg,otherreg)] = ressult_dic[otherreg]
                            formatted_LANDREG['其他登記事項'] = formatted_OTHERREG
                        else:    
                            formatted_LANDREG[field_mapping.get(result,result)] = result_dic_discripe[result]#轉換成中文

                    return {'土地標示部':formatted_LANDREG}


            except TypeError as e:
                raise FormatFailedException(f'{raw_data} ,\n,{e}')
        else:
            raise FormatFailedException(f'查詢無結果{raw_data}')

class LandOwnershipQuery(QueryObject):#土地所有權部搜尋的子類別，定義要求api的網址
    
    
    #所有權部查詢
    def __init__(self, token='',UNIT='', SEC='', NO='',OFFSET = '1',LIMIT = '2', RNO = '') -> None:#fix here
        if RNO:#如果RNO有值，優先以RNO查找
            self.url = 'https://api.land.moi.gov.tw/sandbox/api/LandOwnership/1.0/QueryByRegisterNo'
            super().__init__(token=token,UNIT=UNIT, SEC=SEC, NO=NO,RNO = RNO)
        else:
            self.url = 'https://api.land.moi.gov.tw/sandbox/api/LandOwnership/1.0/QueryByLimit'
            super().__init__(token=token,UNIT=UNIT, SEC=SEC, NO=NO,OFFSET = OFFSET,LIMIT = LIMIT)


    
    def format_data(self, raw_data):#fix here
        #對照表
        field_mapping = {
            "OWRNO": "所有權登記次序",
            "RDATE": "登記日期",
            "REASON": "登記原因(※代碼06)",
            "REASONDATE": "登記原因發生日期",
            "RIGHT": "權利範圍類別",
            "DENOMINATOR": "權利範圍分母",
            "NUMERATOR": "權利範圍分子",
            "OCDATE": "收件年期",
            "OCNO1": "收件字",
            "OCNO2": "收件號",
            "DLPRICE": "申報地價",
            "LTYPE": "類別(※代碼09)",
            "LID": "統一編號",
            "LNAME": "姓名",
            "LADDR": "地址",
            "ORNO": "他項權利登記次序",
            "LTDATE": "前次移轉年月",
            "LTVALUE": "前次移轉現值或原規定地價",
            "PORIGHT": "歷次取得權利範圍類別(※代碼15)",
            "PODENOMINATOR": "歷次取得權利範圍持分分母",
            "PONUMERATOR": "歷次取得權利範圍持分分子",
            "NUMBER": "其他登記事項序號",
            "CATEGORY": "其他登記事項代碼(※代碼30)",
            "CONTENT": "其他登記事項內容",
            'OWNER' : '權利人',
            'LTPRICE': '前次移轉現值',
            'OTHERRIGHTS' : '相關他項權利部',
            'OTHERREG' : '其他登記事項'
        }

        if raw_data['QUANTITY'] != False:#fix here 因為免費測試資料這格是0，為了測試先去除
            formatted_OWNERREG = {}  # 存储格式化后的数据

            try:
                if raw_data and isinstance(raw_data, dict):
                    response = raw_data.get("RESPONSE", "無回應")

                    result_dic_ownership = response[0]['LANDOWNERSHIP'][0]#取出回傳結果字典
                    print(result_dic_ownership)
                    
                    for title, val in result_dic_ownership.items():
                        translate_title = field_mapping.get(title,title)

                        if isinstance(val,str):#資料直接是str
                            formatted_OWNERREG[translate_title] = val

                        elif title == 'OWNER':#資料直接是dic
                             translateted_dic = {}
                             ressult_dic = result_dic_ownership[title]
                             
                             for OWNER_title, OWNER_val in ressult_dic.items():
                                 
                                 translate_OWNER_title = field_mapping.get(OWNER_title,OWNER_title)
                                 translateted_dic[translate_OWNER_title] = OWNER_val

                                 formatted_OWNERREG[translate_title] = translateted_dic
                        
                        elif title in ('LTPRICE','OTHERRIGHTS','OTHERREG') and any(result_dic_ownership[title]) :#資料內是list-dic
                            translateted_dic = {}
                            ressult_dic =  result_dic_ownership[title][0]

                            for OTH_title ,OTH_val in ressult_dic.items():
                                
                                translateted_OTH_title = field_mapping.get(OTH_title,OTH_title)
                                translateted_dic[translateted_OTH_title] = OTH_val

                                formatted_OWNERREG[translate_title] = translateted_dic

                                
                    
                    return {'土地所有權部':formatted_OWNERREG}

            except TypeError as e:
                raise FormatFailedException(f'{raw_data} ,\n,{e}')
        else:
            raise FormatFailedException(f'查詢無結果{raw_data}')
        

class LandOtherRights(QueryObject):#土地他項權利部搜尋的子類別，定義要求api的網址   
     #他項權利部查詢
    def __init__(self,token='', UNIT='', SEC='', NO='',OFFSET = 1,LIMIT = 1, RNO = '') -> None:
        if RNO:
            self.url = 'https://api.land.moi.gov.tw/sandbox/api/LandOtherRights/1.0/QueryByRegisterNo'
            super().__init__(token=token,UNIT=UNIT, SEC=SEC, NO=NO,RNO = RNO)
        else:
            self.url = 'https://api.land.moi.gov.tw/sandbox/api/LandOtherRights/1.0/QueryByLimit'
            super().__init__(token=token,UNIT=UNIT, SEC=SEC, NO=NO,OFFSET = OFFSET,LIMIT = LIMIT)

    def format_data(self, raw_data):#fix here

        field_mapping = {
            "ORNO": "他項權利登記次序",
            "RECEIVEYEAR": "收件年期",
            "RECEIVENO1": "收件字",
            "RECEIVENO2": "收件號",
            "RDATE": "登記日期",
            "REASON": "登記原因(※代碼06)",
            "SETRIGHT": "設定權利範圍類別(※代碼15)",
            "SRDENOMINATOR": "設定權利範圍持分分母",
            "SRNUMERATOR": "設定權利範圍持分分子",
            "AREA": "設定權利範圍面積",
            "CERTIFICATENO": "證明書字號",
            "CLAIMRIGHT": "債權權利範圍類別(※代碼18)",
            "CRDENOMINATOR": "債權權利範圍持分分母",
            "CRNUMERATOR": "債權權利範圍持分分子",
            "RIGHTTYPE": "權利種類(※代碼27)",
            "SUBJECTTYPE": "標的種類(※代碼27)",
            "OWRNO": "所有權登記次序",
            "LTYPE": "類別(※代碼09)",
            "LID": "統一編號",
            "LNAME": "姓名",
            "LADDR": "地址",
            "OTFNO": "他項權利檔號",
            "CCPT_RVT": "擔保債權總金額/權利價值類別(※代碼17)",
            "CCP_RV": "擔保債權總金額/權利價值",
            "DURATIONTYPE": "存續期間類別(※代碼19)",
            "STARTDATE": "起始日期",
            "ENDDATE": "終止日期",
            "PODT": "清償日期類別(※代碼20)",
            "PODD": "清償日期說明",
            "ITYPE_LRTYPE": "利息(率)或地租類別(※代碼21)",
            "ID_LRD": "利息(率)或地租說明",
            "DITYPE": "遲延利息(率)類別(※代碼21)",
            "DID": "遲延利息(率)說明",
            "PTYPE": "違約金類別(※代碼21)",
            "PD": "違約金說明",
            "CCTYPE": "擔保債權種類及範圍類別(※代碼33)",
            "CCCONTENT": "擔保債權種類及範圍內容",
            "CCSDT": "擔保債權確定期日類別(※代碼34)",
            "CCSDD": "擔保債權確定期日日期",
            "OGSAT": "其他擔保範圍約定類別(※代碼35)",
            "OGSAC": "其他擔保範圍約定內容",
            "NUMBER": "其他登記事項序號",
            "CATEGORY": "其他登記事項代碼(※代碼30)",
            "CONTENT": "其他登記事項內容",
            "SEC": "共同擔保地號-段",
            "NO": "共同擔保地號",
            'LANDOTHERIGHTS': '他項權利部',
            'LANDOWNERSHIP': '標的登記次序',
            'OWNER': '權利人',
            'OTHERRIGHTFILE': '他項權利檔',
            'OTHERREG' : '其他登記事項',
            'JOINTGUARANTY' : '共同擔保地／建號',
            'LAND':'擔保土地',
            'BUILDING': '共同擔保建號',


        }

        if raw_data['QUANTITY'] != False:#fix here 因為免費測試資料這格是0，為了測試先去除
            formatted_OTHRREG = {}  # 存储格式化后的数据

            try:
                if raw_data and isinstance(raw_data, dict):
                    response = raw_data.get("RESPONSE", "無回應")

                    result_dic_ownership = response[0]['OTHERRIGHTS'][0]#fix here 取出回傳結果字典 
                    
                    for title, val in result_dic_ownership.items():
                        translate_title = field_mapping.get(title,title)

                        if isinstance(val,str):#資料直接是str
                            formatted_OTHRREG[translate_title] = val

                        elif title in ('OWNER','OTHERRIGHTFILE') and any(result_dic_ownership[title]):#資料直接是dic
                             translateted_dic = {}
                             ressult_dic = result_dic_ownership[title]
                             
                             for title, val in ressult_dic.items():
                                 
                                 translate_OWNER_title = field_mapping.get(title,title)
                                 translateted_dic[translate_OWNER_title] = val

                                 formatted_OTHRREG[translate_title] = translateted_dic
                        
                        elif title in ('LANDOWNERSHIP','OTHERREG') and any(result_dic_ownership[title]) :#資料內是list-dic
                            translateted_dic = {}
                            ressult_dic =  result_dic_ownership[title][0]

                            for title, val in ressult_dic.items():
                                
                                translateted_OTH_title = field_mapping.get(title,title)
                                translateted_dic[translateted_OTH_title] = val

                                formatted_OTHRREG[translate_title] = translateted_dic   
                        elif title == 'JOINTGUARANTY' and any(result_dic_ownership[title]):#資料內是dic-list-dic
                             translateted_dic = {}
                             JOINTGUARANTY_item_dic = {}
                             ressult_dic = result_dic_ownership[title]

                             for title, val_dic in ressult_dic.items():
                                 translate_JOINTGUARANTY_title = field_mapping.get(title,title)
                                 if ressult_dic[title]:
                                    val_dic = ressult_dic[title][0]
                                    for val_title, val_val in val_dic.items():
                                        translate_val_title = field_mapping.get(val_title,val_title)
                                        JOINTGUARANTY_item_dic[translate_val_title] = val_val
                                        translateted_dic[translate_JOINTGUARANTY_title] = JOINTGUARANTY_item_dic

                                 formatted_OTHRREG[translate_title] = translateted_dic 
                            
                                            

                   
                    return {'土地他項權利部':formatted_OTHRREG}

            except TypeError as e:
                raise FormatFailedException(f'{raw_data} ,\n,{e}')
        else:
            raise FormatFailedException(f'查詢無結果{raw_data}')
        


        
if __name__ == "__main__":

    def case1():
        query = LandDescriptionQuery('BA','0001','00010001')
        a = query.run()
        print(a)

    def case2():
        query = LandDescriptionQuery('','','')
        a = query.run()
        print(a)

    def case3():
        query = LandDescriptionQuery('BA','','')
        a = query.run()
        print(a)

    def case4():
        query = LandDescriptionQuery('BA','0002','00010001')
        a = query.run()
        print(a)

    def case5():#沒有其他登記事項
        query = LandDescriptionQuery(1,2,3)
        raw_data = {
  "STATUS": 1,
  "MESSAGE": 0,
  "TRANSACTIONID": "d979df26-881e-4e64-aaa6-4aeaa10b9e98",
  "RETURNROWS": 1,
  "QUANTITY": 1,
  "RESPONSE": [
    {
      "UNIT": "BA",
      "SEC": "0001",
      "NO": "00010001",
      "LANDREG": {
        "RDATE": "0520310",
        "REASON": "03",
        "AREA": "4453",
        "ZONING": 0,
        "LCLASS": 0,
        "ALVALUE": "71264",
        "ALPRICE": "15384",
        "COUNTY": "B",
        "DISTRICT": "01",
        "Y_COORDINATE": 0,
        "X_COORDINATE": 0,
        "MAPSHEET": 0,
        "BUILDINGCOUNT": 0,
        "OTHERREG": [

        ]
      }
    }
  ]
}
        print(query.format_data(raw_data))

    def case6():
        query = LandOtherRights(UNIT='BA',SEC='0001',NO='00020002',OFFSET= 1,LIMIT=10)
        a = query.run()
        print(a)
    # case1()
    # case2()
    # case3()
    # case4()
    case6()