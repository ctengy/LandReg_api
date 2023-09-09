import sys
import json
from typing import Optional
#引入QT包
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget,QLabel)

#引入ui檔案
sys.path.append(r'.')#將上級目錄加入path
from gui.Ui_5 import Ui_MainWindow
from gui.Ui_login import Ui_LogInWindow

from logics.Request_api import *
from logics.Auth import *


class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.bind()


    def bind(self): # function 命名可以更清楚一點，如 bind_button_click_event
        #綁定函數
        self.pushButton_QLD.clicked.connect(self.Ask_LandDescription)
        self.pushButton_QLOwn.clicked.connect(self.Ask_LandOwnership)
        self.pushButton_QLOR.clicked.connect(self.Ask_LandOtherRights)
        self.pushButton_Clear.clicked.connect(self.Clear_Input)

    def Ask_LandDescription(self):  # function 的命名建議參考 PEP 8（Python Enhancement Proposal 8）全部以小寫開頭 -> ask_land_description，大寫開頭會容易與 class 誤會。

        # 變數的命名盡量清楚，不然過三個月再回來看就都忘光光了XD。最理想的方式是不懂的人光看變數名稱就知道這個變數是什麼，甚至不用去寫任何註解，例如 U -> office_code; S -> section_code; N -> land_number
        #取得GUI輸入
        U = self.textEdit_UNIT.toPlainText()#事務所代碼
        S = self.textEdit_SEC.toPlainText()#段代碼
        N = self.textEdit_NO.toPlainText()#地號
        ID = ''#傳入地政平台帳號
        SecretCode = ''#傳入地政平台密碼

        # auth & token 這兩段，建議移到 function 外面，將 token 當作變數傳入進來，因為你的這個 function 叫做 Ask_LandDescription，那他就只應該做麼這一件事，因為光看 function 的命名，沒進來看 code，會不知道這邊還會去 requeset token
        # 另外就是獲取 token 是一段獨立的 api 請求，下面的 Ask_LandOwnership、Ask_LandOtherRights 都會再去重新再 request 一次 token，這樣會有多餘的 request 事件發生。
        # token 或許可以寫成一個 singleton 的 TokenProvider class，只會 request 一次然後在 runtime 緩存，在全域都可以直接獲取。(token 有些人會去做加密等等，看你的需求)
        auth = Get_token(ID,SecretCode)#建立驗證物件
        token = auth.request_token()#取得Token

        # 建議 Query 如果要做成可繼承的 object 可以單純一點，只留下 format_data function 跟他本身一定需要的屬性就好如 url, params。(如果你用 data class 來接 response 的話 format_data 也可以拿掉了)
        # 然後應該 Query 也可以寫成 enum class 像這樣
        # class QueryObject(Enum):
        #     LAND_DESCRIPTION("description_url", your_custom_params)
        #     LAND_OWNER_SHIP("land_owner_url", your_custom_params)
        #     LAND_OTHER_RIGHTS("other_land_url", your_custom_params)
        #
        #     def __init__(self, url, params):
        #         self.url = url
        #         self.params = params
        #
        #     def format_response_data(self, response: any):
        #         if self == QueryObject.LAND_DESCRIPTION:
        #             # format land desc response
        #         elif: self == QueryObject.LAND_OWNER_SHIP:
        #             # format owner ship response
        #         elif: self == QueryObject.LAND_OTHER_RIGHTS
        #             # format other rights response

        # 其他如 send_request、check_input 都不適合在 parent class 裡面做，會缺乏一些彈性，即使去 override parent class ，也會導致 trace code 的難度增加
        # 所以 run 這個 function 可以改寫成更抽象像下面 query_land_information 這樣
        # def check_is_input_correct(query: QueryObject) -> bool:
        #     # do check if input correct, it will return true or false

        # def send_request(token: Token, query: QueryObject):
        #     # do request data and format it

        # def query_land_information(token: Token, query: QueryObject):
        #     if (check_is_input_correct(query)):
        #         send_request(token=token, query=query)
        #
        # query_land_information(token=TokenProvider.get_token, query=QueryObject.LAND_DESCRIPTION)

        query = LandDescriptionQuery(token=token,UNIT=U,SEC=S,NO=N)

        Received_Data = query.run()#送回{'土地標示部':formatted_LANDREG}

        # 建議 response data 可以用 data class 去接，會比用 dict 來的明確，就不用再用兩層 for 去跑所有的 key value，可以直接寫成類似下面這樣之類的
        # q_tree_widget_item = QTreeWidgetItem([your_custom_name])
        # for field in fields(receive_data):
        #     if field.name == OTHERREG:
        #         q_tree_widget_item.addChild(
        #             QTreeWidgetItem(["其他登記事項"])
        #             .addChild(
        #                 QTreeWidgetItem(field)
        #             )
        #         )
        #     else:
        #         q_tree_widget_item.addChild(
        #             QTreeWidgetItem(field)
        #         )


        if isinstance(Received_Data, dict):  # 檢查回傳資料是否正確
            try:
                self.label_return.setText('查詢成功')
                items = []  # 用來存放 QTreeWidgetItem 的列表
                for key, values in Received_Data.items():
                    # 創建一個新的 QTreeWidgetItem，包含主字典的鍵
                    item = QTreeWidgetItem([key])
                    for value in values:
                        if value == '其他登記事項':
                            # 如果子字典的鍵是 '其他登記事項'，創建第一層子節點
                            child1 = QTreeWidgetItem([value])
                            item.addChild(child1)
                            for oth_key, oth_value in values[value].items():
                                # 遍歷 '其他登記事項' 下的子字典，創建第二層子節點
                                child2 = QTreeWidgetItem([oth_key, oth_value])
                                child1.addChild(child2)
                            item.addChild(child1)  # 加入第一層子節點到主節點
                        else:
                            # 這邊我看不太懂 ext 要幹嘛的 QQ，感覺他跟 value 是同一個東西

                            ext = values[value]
                            # 創建一個包含值和擴展的 QTreeWidgetItem
                            child = QTreeWidgetItem([value, ext])
                            item.addChild(child)
                    items.append(item)  # 加入主節點到項目列表

                # 將項目列表插入到 QTreeWidget 的頂層
                self.treeWidget.insertTopLevelItems(0, items)
            except:
                self.label_return.setText('Insert Data Fail')

        else:
            self.label_return.setText(Received_Data)


    def Ask_LandOwnership(self):
        #取得GUI輸入
        U = self.textEdit_UNIT.toPlainText()#事務所代碼
        S = self.textEdit_SEC.toPlainText()#段代碼
        N = self.textEdit_NO.toPlainText()#地號
        ID = ''#傳入地政平台帳號
        SecretCode = ''#傳入地政平台密碼
        auth = Get_token(ID,SecretCode)#建立驗證物件
        token = auth.request_token()#取得Token
        query = LandOwnershipQuery(token=token,UNIT=U,SEC=S,NO=N, RNO= '0002')#fix here 測試的RNO

        Received_Data = query.run()
        print(Received_Data)

        if isinstance(Received_Data, dict):  # 檢查回傳資料是否正確
            try:
                items = []  # 用來存放 QTreeWidgetItem 的列表
                for key, values in Received_Data.items():
                    # 創建一個新的 QTreeWidgetItem，包含主字典的鍵
                    item = QTreeWidgetItem([key])
                    for value in values:
                        if value in ('權利人','前次移轉現值','相關他項權利部','其他登記事項'):
                            # 如果子字典的鍵是 '其他登記事項'，創建第一層子節點
                            child1 = QTreeWidgetItem([value])
                            item.addChild(child1)
                            for oth_key, oth_value in values[value].items():
                                # 遍歷 '其他登記事項' 下的子字典，創建第二層子節點
                                child2 = QTreeWidgetItem([oth_key, oth_value])
                                child1.addChild(child2)
                            item.addChild(child1)  # 加入第一層子節點到主節點
                        elif value:
                            ext = values[value]
                            # 創建一個包含值和擴展的 QTreeWidgetItem
                            child = QTreeWidgetItem([value, ext])
                            item.addChild(child)
                    items.append(item)  # 加入主節點到項目列表

                # 將項目列表插入到 QTreeWidget 的頂層
                self.treeWidget.insertTopLevelItems(0, items)
            except:
                self.label_return.setText('Insert Data Fail')

        else:
            self.label_return.setText(Received_Data)


    def Ask_LandOtherRights(self):#fix here 待寫insert logic
        #取得GUI輸入
        U = self.textEdit_UNIT.toPlainText()#事務所代碼
        S = self.textEdit_SEC.toPlainText()#段代碼
        N = self.textEdit_NO.toPlainText()#地號
        ID = ''#傳入地政平台帳號
        SecretCode = ''#傳入地政平台密碼
        auth = Get_token(ID,SecretCode)#建立驗證物件
        token = auth.request_token()#取得Token

        query = LandOtherRights(token=token,UNIT=U,SEC=S,NO=N,RNO='')#fix here 測試的RNO

        Received_Data = query.run()


        if isinstance(Received_Data, dict):  # 檢查回傳資料是否正確
            try:
                items = []  # 用來存放 QTreeWidgetItem 的列表
                for key, values in Received_Data.items():
                    # 創建一個新的 QTreeWidgetItem，包含主字典的鍵
                    item = QTreeWidgetItem([key])
                    for value in values:
                        if value in ('標的登記次序','權利人','他項權利檔','其他登記事項'):
                            # 如果子字典的鍵是 '其他登記事項'，創建第一層子節點
                            child1 = QTreeWidgetItem([value])
                            item.addChild(child1)
                            for oth_key, oth_value in values[value].items():
                                # 遍歷 '其他登記事項' 下的子字典，創建第二層子節點
                                child2 = QTreeWidgetItem([oth_key, oth_value])
                                child1.addChild(child2)
                            item.addChild(child1)  # 加入第一層子節點到主節點

                        elif value in ('共同擔保地／建號'):
                            child1 = QTreeWidgetItem([value])
                            item.addChild(child1)
                            for oth_key, oth_value in values[value].items():
                                # 遍歷 '其他登記事項' 下的子字典，創建第二層子節點
                                child2 = QTreeWidgetItem([oth_key])
                                child1.addChild(child2)
                                for oth_key2, oth_val2 in oth_value.items():
                                    child3 = QTreeWidgetItem([oth_key2,oth_val2])
                                    child2.addChild(child3)

                            item.addChild(child1)

                        elif value :
                            ext = values[value]
                            # 創建一個包含值和擴展的 QTreeWidgetItem
                            child = QTreeWidgetItem([value, ext])
                            item.addChild(child)
                    items.append(item)  # 加入主節點到項目列表          
                self.treeWidget.insertTopLevelItems(0, items) # 將項目列表插入到 QTreeWidget 的頂層

            except:
                self.label_return.setText('Insert Data Fail')

        else:
            self.label_return.setText(Received_Data)



    def Clear_Input(self):#清除輸入
        self.textEdit_UNIT.clear()
        self.textEdit_SEC.clear()
        self.textEdit_NO.clear()

class LogInWindow(QMainWindow,Ui_LogInWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.bind()

    def bind(self):
        self.pushButton_login.clicked.connect(self.login_auth)

    def login_auth(self):
        account = self.lineEdit_account.text()
        password = self.lineEdit_password.text()

        if account == '111' and password == '111':
            self.close()

            self.main_window = MyWindow()
            self.main_window.show()
        else:
            self.label_return.setText("登陸失敗")





if __name__ == "__main__":
    app = QApplication([])
    window = LogInWindow()
    window.show()
    app.exec()