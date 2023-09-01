import sys
import json
#引入QT包
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextBrowser, QTextEdit, QVBoxLayout, QWidget,QTreeWidgetItem)
from PySide6.QtCore import Qt

#引入ui檔案
sys.path.append(r'.')#將上級目錄加入path
from gui.Ui_5 import Ui_MainWindow

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
        self.pushButton_Clear.clicked.connect(self.Clear_Input)

    def Ask_LandDescription(self):#fix here 重寫insert邏輯

        #取得GUI輸入
        U = self.textEdit_UNIT.toPlainText()#事務所代碼
        S = self.textEdit_SEC.toPlainText()#段代碼
        N = self.textEdit_NO.toPlainText()#地號
        ID = ''#傳入地政平台帳號
        SecretCode = ''#傳入地政平台密碼
        auth = Get_token(ID,SecretCode)#建立驗證物件
        token = auth.request_token()#取得Token
        query = LandDescriptionQuery(token=token,UNIT=U,SEC=S,NO=N)

        Received_Data = query.run()#送回{'土地標示部':formatted_LANDREG} 
        
        if isinstance(Received_Data, dict):  # 檢查回傳資料是否正確
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

        else:
            raise UnFormatedException('Data UnFormated!')


    def Ask_LandOwnership(self):#fix here 待寫insert logic
        #取得GUI輸入
        U = self.textEdit_UNIT.toPlainText()#事務所代碼
        S = self.textEdit_SEC.toPlainText()#段代碼
        N = self.textEdit_NO.toPlainText()#地號
        ID = ''#傳入地政平台帳號
        SecretCode = ''#傳入地政平台密碼
        auth = Get_token(ID,SecretCode)#建立驗證物件
        token = auth.request_token()#取得Token
        query = LandDescriptionQuery(token=token,UNIT=U,SEC=S,NO=N)

        Received_Data = query.run()

        pass

    def Ask_LandOtherRights(self):#fix here 待寫insert logic
        #取得GUI輸入
        U = self.textEdit_UNIT.toPlainText()#事務所代碼
        S = self.textEdit_SEC.toPlainText()#段代碼
        N = self.textEdit_NO.toPlainText()#地號
        ID = ''#傳入地政平台帳號
        SecretCode = ''#傳入地政平台密碼
        auth = Get_token(ID,SecretCode)#建立驗證物件
        token = auth.request_token()#取得Token

        query = LandOtherRights(token=token,UNIT=U,SEC=S,NO=N)

        Received_Data = query.run()
        
        pass

    def Clear_Input(self):#清除輸入
        self.textEdit_UNIT.clear()
        self.textEdit_SEC.clear()
        self.textEdit_NO.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()       