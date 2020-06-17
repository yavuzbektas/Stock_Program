# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

import icons_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(17, 38, 370, 211))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(40, 40, 81, 16))
        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(110, 40, 181, 24))
        self.lineEdit_2 = QLineEdit(self.tab)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(110, 70, 181, 24))
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 70, 81, 16))
        self.horizontalLayoutWidget = QWidget(self.tab)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(190, 150, 169, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pb_login = QPushButton(self.horizontalLayoutWidget)
        self.pb_login.setObjectName(u"pb_login")

        self.horizontalLayout.addWidget(self.pb_login)

        self.pb_cancel2 = QPushButton(self.horizontalLayoutWidget)
        self.pb_cancel2.setObjectName(u"pb_cancel2")

        self.horizontalLayout.addWidget(self.pb_cancel2)

        icon = QIcon()
        icon.addFile(u":/staticfiles/icons/Users.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tab, icon, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.lineEdit_3 = QLineEdit(self.tab_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(140, 60, 181, 24))
        self.label_3 = QLabel(self.tab_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 90, 81, 16))
        self.label_4 = QLabel(self.tab_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(50, 60, 81, 16))
        self.lineEdit_4 = QLineEdit(self.tab_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(140, 90, 181, 24))
        self.lineEdit_4.setMaxLength(20)
        self.lineEdit_4.setEchoMode(QLineEdit.Password)
        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(50, 120, 81, 16))
        self.lineEdit_5 = QLineEdit(self.tab_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(140, 120, 181, 24))
        self.lineEdit_5.setEchoMode(QLineEdit.Password)
        self.comboBox = QComboBox(self.tab_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(140, 30, 181, 24))
        self.pb_save = QPushButton(self.tab_2)
        self.pb_save.setObjectName(u"pb_save")
        self.pb_save.setGeometry(QRect(187, 153, 80, 25))
        self.pb_cancel = QPushButton(self.tab_2)
        self.pb_cancel.setObjectName(u"pb_cancel")
        self.pb_cancel.setGeometry(QRect(277, 153, 80, 25))
        icon1 = QIcon()
        icon1.addFile(u":/staticfiles/icons/login.png", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tab_2, icon1, "")
        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(47, 8, 341, 31))
        self.label_7.setFrameShape(QFrame.StyledPanel)
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(17, 258, 371, 31))
        self.label_6.setFrameShape(QFrame.Box)
        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(14, 7, 31, 31))
        self.label_8.setPixmap(QPixmap(u":/staticfiles/icons/stock6.png"))
        self.label_8.setScaledContents(True)

        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"User Name", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.pb_login.setText(QCoreApplication.translate("Dialog", u"Login", None))
        self.pb_cancel2.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Log In", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("Dialog", u"username", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"User Name", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("Dialog", u"password", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Re-Password", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("Dialog", u"re-password", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"Standart", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Admin", None))

        self.pb_save.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.pb_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Sign In", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Login Page - Stock Program v0</span></p></body></html>", None))
        self.label_6.setText("")
        self.label_8.setText("")
    # retranslateUi

