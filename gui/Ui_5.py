# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '5.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

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
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton_QLD = QPushButton(self.centralwidget)
        self.pushButton_QLD.setObjectName(u"pushButton_QLD")
        self.pushButton_QLD.setGeometry(QRect(580, 40, 91, 51))
        self.pushButton_Clear = QPushButton(self.centralwidget)
        self.pushButton_Clear.setObjectName(u"pushButton_Clear")
        self.pushButton_Clear.setGeometry(QRect(690, 100, 91, 51))
        self.treeWidget = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(40, 250, 721, 311))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(270, 60, 258, 101))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.textEdit_UNIT = QTextEdit(self.layoutWidget)
        self.textEdit_UNIT.setObjectName(u"textEdit_UNIT")
        self.textEdit_UNIT.setTabChangesFocus(True)

        self.verticalLayout_2.addWidget(self.textEdit_UNIT)

        self.textEdit_SEC = QTextEdit(self.layoutWidget)
        self.textEdit_SEC.setObjectName(u"textEdit_SEC")
        self.textEdit_SEC.setTabChangesFocus(True)

        self.verticalLayout_2.addWidget(self.textEdit_SEC)

        self.textEdit_NO = QTextEdit(self.layoutWidget)
        self.textEdit_NO.setObjectName(u"textEdit_NO")
        self.textEdit_NO.setTabChangesFocus(True)

        self.verticalLayout_2.addWidget(self.textEdit_NO)

        self.pushButton_QLOwn = QPushButton(self.centralwidget)
        self.pushButton_QLOwn.setObjectName(u"pushButton_QLOwn")
        self.pushButton_QLOwn.setGeometry(QRect(580, 100, 91, 51))
        self.pushButton_QLOR = QPushButton(self.centralwidget)
        self.pushButton_QLOR.setObjectName(u"pushButton_QLOR")
        self.pushButton_QLOR.setGeometry(QRect(580, 160, 91, 51))
        self.label_NO = QLabel(self.centralwidget)
        self.label_NO.setObjectName(u"label_NO")
        self.label_NO.setGeometry(QRect(190, 140, 38, 24))
        self.label_NO.setCursor(QCursor(Qt.ArrowCursor))
        self.label_NO.setFrameShape(QFrame.NoFrame)
        self.label_NO.setAlignment(Qt.AlignCenter)
        self.label_NO.setWordWrap(False)
        self.label_SEC = QLabel(self.centralwidget)
        self.label_SEC.setObjectName(u"label_SEC")
        self.label_SEC.setGeometry(QRect(180, 100, 57, 24))
        self.label_SEC.setCursor(QCursor(Qt.ArrowCursor))
        self.label_SEC.setFrameShape(QFrame.NoFrame)
        self.label_SEC.setAlignment(Qt.AlignCenter)
        self.label_SEC.setWordWrap(False)
        self.label_BA = QLabel(self.centralwidget)
        self.label_BA.setObjectName(u"label_BA")
        self.label_BA.setGeometry(QRect(160, 60, 95, 24))
        self.label_BA.setCursor(QCursor(Qt.ArrowCursor))
        self.label_BA.setFrameShape(QFrame.NoFrame)
        self.label_BA.setAlignment(Qt.AlignCenter)
        self.label_BA.setWordWrap(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_QLD.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8a62\u6a19\u793a\u90e8", None))
        self.pushButton_Clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u7d50\u679c", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u9805\u76ee", None));
        self.pushButton_QLOwn.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8a62\u6240\u6709\u6b0a\u90e8", None))
        self.pushButton_QLOR.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8a62\u4ed6\u9805\u6b0a\u5229", None))
        self.label_NO.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">\u5730\u865f</span></p></body></html>", None))
        self.label_SEC.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">\u6bb5\u4ee3\u78bc</span></p></body></html>", None))
        self.label_BA.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">\u4e8b\u52d9\u6240\u4ee3\u78bc</span></p></body></html>", None))
    # retranslateUi

