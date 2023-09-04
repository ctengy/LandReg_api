# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSplitter,
    QStatusBar, QWidget)

class Ui_LogInWindow(object):
    def setupUi(self, LogInWindow):
        if not LogInWindow.objectName():
            LogInWindow.setObjectName(u"LogInWindow")
        LogInWindow.resize(399, 233)
        self.centralwidget = QWidget(LogInWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        font = QFont()
        font.setPointSize(10)
        self.centralwidget.setFont(font)
        self.frame_login = QFrame(self.centralwidget)
        self.frame_login.setObjectName(u"frame_login")
        self.frame_login.setGeometry(QRect(10, 10, 381, 201))
        self.frame_login.setFont(font)
        self.frame_login.setFrameShape(QFrame.StyledPanel)
        self.frame_login.setFrameShadow(QFrame.Raised)
        self.frame_login.setLineWidth(1)
        self.label_return = QLabel(self.frame_login)
        self.label_return.setObjectName(u"label_return")
        self.label_return.setGeometry(QRect(150, 150, 91, 21))
        font1 = QFont()
        font1.setPointSize(15)
        self.label_return.setFont(font1)
        self.pushButton_login = QPushButton(self.frame_login)
        self.pushButton_login.setObjectName(u"pushButton_login")
        self.pushButton_login.setGeometry(QRect(250, 90, 81, 31))
        self.splitter_3 = QSplitter(self.frame_login)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setGeometry(QRect(20, 80, 172, 52))
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.splitter = QSplitter(self.splitter_3)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.label_account = QLabel(self.splitter)
        self.label_account.setObjectName(u"label_account")
        self.label_account.setFont(font1)
        self.label_account.setFrameShape(QFrame.NoFrame)
        self.label_account.setAlignment(Qt.AlignCenter)
        self.splitter.addWidget(self.label_account)
        self.label_password = QLabel(self.splitter)
        self.label_password.setObjectName(u"label_password")
        self.label_password.setFont(font1)
        self.label_password.setFrameShape(QFrame.NoFrame)
        self.label_password.setAlignment(Qt.AlignCenter)
        self.splitter.addWidget(self.label_password)
        self.splitter_3.addWidget(self.splitter)
        self.splitter_2 = QSplitter(self.splitter_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.lineEdit_account = QLineEdit(self.splitter_2)
        self.lineEdit_account.setObjectName(u"lineEdit_account")
        self.splitter_2.addWidget(self.lineEdit_account)
        self.lineEdit_password = QLineEdit(self.splitter_2)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.splitter_2.addWidget(self.lineEdit_password)
        self.splitter_3.addWidget(self.splitter_2)
        LogInWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(LogInWindow)
        self.statusbar.setObjectName(u"statusbar")
        LogInWindow.setStatusBar(self.statusbar)
        LogInWindow.setWindowFlags(Qt.FramelessWindowHint)

        self.retranslateUi(LogInWindow)

        QMetaObject.connectSlotsByName(LogInWindow)
    # setupUi

    def retranslateUi(self, LogInWindow):
        LogInWindow.setWindowTitle(QCoreApplication.translate("LogInWindow", u"MainWindow", None))
        self.label_return.setText("")
        self.pushButton_login.setText(QCoreApplication.translate("LogInWindow", u"\u767b\u9678", None))
        self.label_account.setText(QCoreApplication.translate("LogInWindow", u"\u5e33\u865f", None))
        self.label_password.setText(QCoreApplication.translate("LogInWindow", u"\u5bc6\u78bc", None))
    # retranslateUi

