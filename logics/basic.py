import sys
import json
#引入QT包
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextBrowser, QTextEdit, QVBoxLayout, QWidget,QTreeWidgetItem)
from PySide6.QtCore import Qt

import requests
#引入ui檔案
sys.path.append(r'.')#將上級目錄加入path
from gui.Ui_4 import Ui_MainWindow

from logics.requestapi import *
from logics.Auth import *

class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.bind()
    
    
    def bind(self):
        #綁定函數
        self.pushButton_OK.clicked.connect(self.ask_LandDescription)

    def ask_LandDescription(self):#fix here
        #取得GUI輸入
        U = self.textEdit_UNIT.toPlainText()#事務所代碼
        S = self.textEdit_SEC.toPlainText()#段代碼
        N = self.textEdit_NO.toPlainText()#地號
        # ID = ''#傳入地政平台帳號
        # SecretCode = ''#傳入地政平台密碼
        # auth = Get_token(ID,SecretCode)#建立驗證物件
        # token = auth.request_token()#取得Token
        token = 1#fix 測試用
        query = LandDescriptionQuery(token=token,UNIT=U,SEC=S,NO=N)

        received_data = query.run()#送回{'土地標示部':formatted_LANDREG}

        if isinstance(received_data, dict):

            tree = self.treeWidget
            items = []
            for key, values in received_data.items():

                item = QTreeWidgetItem([key])
                for value in values:
                    if value == '其他登記事項':
                        child1 = QTreeWidgetItem([value])
                        item.addChild(child1)
                        for oth_key, oth_value in values[value].items():
                            child2 = QTreeWidgetItem([oth_key,oth_value])
                            child1.addChild(child2)


                            item.addChild(child2)

                    else:
                        ext = values[value]
                        child = QTreeWidgetItem([value, ext])
                        item.addChild(child)
                items.append(item)

            tree.insertTopLevelItems(0, items)
        
        else:
            print(received_data)



if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()       