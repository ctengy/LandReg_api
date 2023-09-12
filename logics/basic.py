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
    
    
    def bind(self):
        #綁定函數
        self.pushButton_QLD.clicked.connect(self.Ask_LandDescription)
        self.pushButton_QLOwn.clicked.connect(self.Ask_LandOwnership)
        self.pushButton_QLOR.clicked.connect(self.Ask_LandOtherRights)
        self.pushButton_Clear.clicked.connect(self.Clear_Input)

    def Ask_LandDescription(self):

        #取得GUI輸入
        U = self.textEdit_UNIT.toPlainText()#事務所代碼
        S = self.textEdit_SEC.toPlainText()#段代碼
        N = self.textEdit_NO.toPlainText()#地號
        ID = ''#傳入地政平台帳號
        SecretCode = ''#傳入地政平台密碼
        auth = GetToken(ID,SecretCode)#建立驗證物件
        token = auth.request_token()#取得Token
        query = LandDescriptionQuery(token=token,UNIT=U,SEC=S,NO=N)

        Received_Data = query.run()#送回{'土地標示部':formatted_LANDREG}     
                       
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
                            ext = values[value]
                            # 創建一個包含值和擴展的 QTreeWidgetItem
                            child = QTreeWidgetItem([value, ext])
                            item.addChild(child)
                    items.append(item)  # 加入主節點到項目列表

                # 將項目列表插入到 QTreeWidget 的頂層
                self.treeWidget.insertTopLevelItems(0, items)
            except :
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
        auth = GetToken(ID,SecretCode)#建立驗證物件
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
        auth = GetToken(ID,SecretCode)#建立驗證物件
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