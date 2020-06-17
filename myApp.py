# #######################################

__author__ = "Yavuz Bektaş & "
__version__ = "1.0"
__email__ = "yavuzbektas@gmail.com"
__linkedin__ = "https://www.linkedin.com/in/yavuz-bekta%C5%9F-28659642/"
__release_date__ = "2020.05.01"
__github__ = "https://github.com/yavuzbektas/Stock_Program"
# #######################################
import sys, os,shutil,datetime
from GUI.mainWindow import Ui_mainwindow
from GUI.logs import Ui_Form as log_dialog
from GUI.login import Ui_Dialog as login_dialog
from GUI.about import Ui_Form as About_window
from PySide2.QtWidgets import QApplication,QMainWindow,QDialog,QPushButton,QMessageBox,QTableWidgetItem,QFileDialog,QStyle,QInputDialog
from PySide2.QtCore import SIGNAL, QObject,QFileInfo,QDateTime,QTranslator
from PySide2.QtGui import QPixmap
from xlsxwriter import Workbook as Wb
import pyqrcode
import db_mysql
import logging,logging.handlers
# ================   SETTINGS     ===================================
BASE_PATH = os.getcwd()
IMAGE_DIR = (BASE_PATH + '\\media\\images\\') # resimler ileride serverda databasein oldugu yerde olacaktır.
FILE_DIR = (BASE_PATH + '\\media\\files\\') #
REPORT_DIR = (BASE_PATH + '\\media\\Reports\\')
SETTING_DIR = (BASE_PATH + '\\staticfiles\\')
SETTING_FILE = "settings.txt"
SERVER_SETTING = {
    "host":"localhost",
    "username":"root",
    "password":"1234567890",
    "DB_NAME":"stockDB"   } # ileride server adresi girilecektir.
LANGUAGE = "turkish"
LANGUAGES_DIR = (BASE_PATH + '\\staticfiles\\languages\\')
LOG_FILENAME = (BASE_PATH + '\\media\\logs\\myapp.log')
print('Resim Dosyaları : {}\n  '
      'Rapor Dosyaları : {}\n   '
      'Diger Dosyaları : {}\n  '
      'klasörlerinde yer almaktadır. '.format(IMAGE_DIR,REPORT_DIR, FILE_DIR))
# =====================================================================================================
#============   table Headers  ====================
headers = ("ID", "Room Name","Description", "Number", "Staff", "Record Date")
headers_cabinet_type = ("ID", "Type Name")
headers_cabinet = ("ID", "Cabinet Code", "Cabinet Type","Room Name")
headers_shelf = ("ID", "Shelf Code","Cabinet Code","Room Name")
headers_material = ("ID", "Type","Name","Code-1","Code-2","Property-1","Property-2","Manufacture","Price","unit","Image Path","Record Date")
headers_material_type = ("ID", "Type Name")
headers_stock = ("ID", "Code", "Material Name","Mat.Code 1" ,"Property-1","Shelf Code",
                 "Cabinet Code","Cabinet Type","Room Name","Qty","Unit","UserID", "Record Date")
headers_logs = ("ID", "Code","Reason","Yourname","Act Qty","Used Qty", "Material Name","Mat.Code 1" ,"Property-1","Shelf Code",
                 "Cabinet Code","Cabinet Type","Room Name","Unit","UserID", "Record Date")
headers_user =  ("ID", "User Name","UserType", "Record Date")


# ================= SETTINGS FILE ==================================================
def pathFind():
    file_path = (SETTING_DIR + SETTING_FILE)
    print(file_path)
    if os.path.isfile(file_path):
        pass
    else:
        f = open(file_path, "a")
        text_wrt = ("""# this is a configuration file.
# please dont change anything manually.
#----------------------------------------
SERVER_SETTING
host:localhost
username:root
password:1234567890
DB_NAME:stockDB
-----------------------------
LANGUAGE:turkish
----------------------------------------------""")
        f.write(text_wrt)
        f.close
    return file_path  # yazdırma işlemi
def read_settins_file():
    file_path = pathFind()
    with open(file_path, "r+") as myfile:
        mylines = []  # Declare an empty list.
        for myline in myfile:  # For each line in the file,
            mylines.append(myline.rstrip('\n'))  # strip newline and add to list.
        # for i in mylines:
        #     print(i)
    return mylines
def read_parameter(line_number=4):
    try:
        parameter= read_settins_file()[line_number].split(':')[1]
        return parameter
    except Exception as err:
        print(err)
        return ""
def write_parameter(line_number=9,value=""):

    mylines = read_settins_file()[:]

    parameter= mylines[line_number]
    mylines[line_number]= parameter.split(':')[0]+":"+value
    write_setting_file(mylines)
def write_setting_file(mylines):
    file_path = pathFind()

    with open(file_path, "r+") as myfile:
        myfile.seek(0)
        for i in range(len(mylines)):

            myfile.writelines(mylines[i]+"\n")
def mylog():

    # create logger
    my_logger = logging.getLogger("Stock-V0")

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=LOG_FILENAME,
                        filemode='a')
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=20, backupCount=5)
    my_logger.addHandler(handler)
    my_logger.info("gdfgsdfgsdfgsd")


LANGUAGE = read_parameter(9)

class MyWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MyWindow, self).__init__(parent)
        self.ui=Ui_mainwindow()
        self.ui.setupUi(self)
        self.db=db_mysql.mydb()
        self.ui.tabWidget.tabBar().setVisible(False)
        self.handle_button()
        self.read_tabs_index()
        self.ui.tabWidget_2.tabBar().setVisible(False)
        self.user_admin_check()
        self.setWindowTitle("Mainwindow - Stock Management  Program V0")
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.tabWidget_4.setCurrentIndex(0)
        self.ui.tabWidget_5.setCurrentIndex(0)
        self.ui.tabWidget_2.setCurrentIndex(0)
        self.ui.tabWidget_3.setCurrentIndex(0)
        self.ui.label_14.setVisible(False)

    def handle_button(self):
        self.ui.actionStock.triggered.connect(self.materials_search_tab)
        self.ui.actionRoom_Setting.triggered.connect(self.stockfield_edit_tab)
        self.ui.actionRoom_Setting.triggered.connect(self.room_edit_tab)
        self.ui.actionCab_net_Setting.triggered.connect(self.stockfield_edit_tab)
        self.ui.actionCab_net_Setting.triggered.connect(self.cabinet_edit_tab)
        self.ui.actionShelf_Setting.triggered.connect(self.stockfield_edit_tab)
        self.ui.actionShelf_Setting.triggered.connect(self.shelf_edit_tab)
        self.ui.actionAdd_Edit_Material.triggered.connect(self.materials_add_tab)
        self.ui.actionSettings.triggered.connect(self.settings_tab)
        self.ui.actionReports.triggered.connect(self.reports_tab)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.open_about)

        self.ui.pushButton.clicked.connect(self.materials_search_tab)
        self.ui.pushButton_2.clicked.connect(self.materials_add_tab)
        self.ui.pushButton_3.clicked.connect(self.stocks_edit_tab)
        self.ui.pushButton_6.clicked.connect(self.stockfield_edit_tab)
        self.ui.pushButton_4.clicked.connect(self.reports_tab)
        self.ui.pushButton_5.clicked.connect(self.settings_tab)
        self.ui.pushButton_23.clicked.connect(self.room_edit_tab)
        self.ui.pushButton_24.clicked.connect(self.cabinettype_edit_tab)
        self.ui.pushButton_15.clicked.connect(self.cabinet_edit_tab)
        self.ui.pushButton_25.clicked.connect(self.shelf_edit_tab)

        self.ui.tabWidget_2.currentChanged.connect(self.read_tabs_index)

        self.ui.pushButton_20.clicked.connect(self.insert_data_room_table)
        self.ui.pushButton_21.clicked.connect(self.clear_room_fields)
        self.ui.pushButton_22.clicked.connect(self.delete_data_room_table)
        self.ui.tableWidget_3.itemClicked.connect(self.callback_data_from_room_table_widget)

        self.ui.pushButton_27.clicked.connect(self.insert_cabinet_type_table)
        self.ui.tableWidget_4.itemClicked.connect(self.callback_data_from_cabinettype_table_widget)
        self.ui.pushButton_29.clicked.connect(self.clear_cabinettype_fields)
        self.ui.pushButton_31.clicked.connect(self.delete_data_cabinettype_table)

        self.ui.pushButton_32.clicked.connect(self.insert_cabinet_table)
        self.ui.tableWidget_5.itemClicked.connect(self.callback_data_from_cabinet_table_widget)
        self.ui.pushButton_33.clicked.connect(self.clear_cabinet_fields)
        self.ui.pushButton_34.clicked.connect(self.delete_data_cabinet_table)
        self.ui.tabWidget_3.close()
        self.ui.pushButton_16.clicked.connect(self.show_cabin_popup)
        self.ui.pushButton_30.clicked.connect(self.filter_cabinet)

        self.ui.tableWidget_6.itemClicked.connect(self.data_from_cabinettype)
        self.ui.tableWidget_7.itemClicked.connect(self.data_from_room)

        self.ui.pushButton_28.clicked.connect(self.show_shelf_popup)
        self.ui.pushButton_11.clicked.connect(self.logout_myapp)
        self.ui.tableWidget_9.itemClicked.connect(self.data_from_cabinet)
        self.ui.pushButton_35.clicked.connect(self.insert_shelf_table)
        self.ui.tableWidget_8.itemClicked.connect(self.callback_from_shelf_table)
        self.ui.pushButton_36.clicked.connect(self.clear_shelf_fields)
        self.ui.pushButton_37.clicked.connect(self.delete_data_shelf_table)
        self.ui.pushButton_46.clicked.connect(self.filter_shelf_table)

        self.ui.pushButton_9.clicked.connect(self.image_file_dialog_open_material)

        self.ui.pushButton_41.clicked.connect(self.insert_material_type_table)
        self.ui.tableWidget_11.itemClicked.connect(self.callback_data_from_material_type_table_widget)
        self.ui.pushButton_42.clicked.connect(self.clear_material_type_fields)
        self.ui.pushButton_43.clicked.connect(self.delete_data_material_type_table)
        self.ui.pushButton_10.clicked.connect(self.material_type_tab)
        self.ui.pushButton_44.clicked.connect(self.data_from_material_type)
        self.ui.pushButton_45.clicked.connect(self.filter_material_type_table)

        self.ui.pushButton_38.clicked.connect(self.insert_material_table)
        self.ui.tableWidget_10.itemClicked.connect(self.callback_from_material_table)
        self.ui.pushButton_39.clicked.connect(self.clear_material_fields)
        self.ui.pushButton_40.clicked.connect(self.delete_data_material_table)
        self.ui.tabWidget_4.currentChanged.connect(self.read_tabs_index)
        self.ui.tabWidget.currentChanged.connect(self.read_tabs_index)
        self.ui.tabWidget_2.currentChanged.connect(self.read_tabs_index)
        self.ui.pushButton_47.clicked.connect(self.filter_material_table)
        self.ui.tabWidget_5.currentChanged.connect(self.read_tabs_index)

        self.ui.lineEdit_65.textChanged.connect(self.final_stockcode_generate)
        self.ui.lineEdit_56.textChanged.connect(self.final_stockcode_generate)
        self.ui.lineEdit_57.textChanged.connect(self.final_stockcode_generate)
        self.ui.lineEdit_58.textChanged.connect(self.final_stockcode_generate)
        self.ui.lineEdit_59.textChanged.connect(self.final_stockcode_generate)


        self.ui.pushButton_58.clicked.connect(self.insert_stock_table)
        self.ui.tableWidget_13.itemClicked.connect(self.callback_from_stock_table)
        self.ui.pushButton_59.clicked.connect(self.clear_stock_fields)
        self.ui.pushButton_60.clicked.connect(self.delete_data_stock_table)
        self.ui.pushButton_53.clicked.connect(self.filter_stock_table)
        self.ui.pushButton_48.clicked.connect(self.stock_material_call_tab)
        self.ui.pushButton_50.clicked.connect(self.stock_room_call_tab)
        self.ui.pushButton_49.clicked.connect(self.stock_cabinet_call_tab)
        self.ui.pushButton_51.clicked.connect(self.stock_shelf_call_tab)

        self.ui.tableWidget_12.itemClicked.connect(self.material_table_clicked)
        self.ui.tableWidget_14.itemClicked.connect(self.room_table_clicked)
        self.ui.tableWidget_15.itemClicked.connect(self.cabinet_table_clicked)
        self.ui.tableWidget_16.itemClicked.connect(self.shelf_table_clicked)
        self.ui.tableWidget.itemClicked.connect(self.stock_search_table_clicked)

        self.ui.pushButton_52.clicked.connect(self.filter_stock_material_table)
        self.ui.pushButton_54.clicked.connect(self.filter_stock_room_table)
        self.ui.pushButton_55.clicked.connect(self.filter_stock_cabinet_table)
        self.ui.pushButton_56.clicked.connect(self.filter_stock_shelf_table)
        self.ui.pushButton_7.clicked.connect(self.filter_stock_search_table)

        self.ui.pushButton_8.clicked.connect(self.log_page_call)
        self.ui.pushButton_64.clicked.connect(self.filter_logs_table)
        self.ui.pushButton_65.clicked.connect(self.export_report)

        self.ui.pushButton_61.clicked.connect(self.filter_user_table)
        self.ui.tableWidget_2.itemClicked.connect(self.callback_from_user_table)
        self.ui.pushButton_18.clicked.connect(self.update_data_user_table)
        self.ui.pushButton_19.clicked.connect(self.delete_data_user_table)
        self.ui.pushButton_62.clicked.connect(self.save_qrcode_png)
        self.ui.pushButton_67.clicked.connect(self.translate)
        self.ui.pushButton_66.clicked.connect(self.translate)
    def update_msjbox(self,text,title):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        return msgBox.exec()
    def delete_msjbox(self,text,title):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
        buttonY = msgBox.button(QMessageBox.Discard)
        buttonY.setText('Delete')
        return msgBox.exec()
    # ================ TABS CONTROL  ===========================================
    def user_admin_check(self):
        if self.ui.lineEdit_82.text()=="Admin":
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton_3.setEnabled(True)
            self.ui.pushButton_6.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.pushButton_4.setEnabled(True)
            self.ui.pushButton_5.setEnabled(True)

            self.ui.actionStock.setEnabled(True)
            self.ui.actionRoom_Setting.setEnabled(True)
            self.ui.actionCab_net_Setting.setEnabled(True)
            self.ui.actionShelf_Setting.setEnabled(True)
            self.ui.actionAdd_Edit_Material.setEnabled(True)
            self.ui.actionSettings.setEnabled(True)
            self.ui.actionReports.setEnabled(True)
        else:
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton_6.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_4.setEnabled(False)
            self.ui.pushButton_5.setEnabled(False)
            self.ui.actionStock.setEnabled(False)
            self.ui.actionRoom_Setting.setEnabled(False)
            self.ui.actionCab_net_Setting.setEnabled(False)
            self.ui.actionShelf_Setting.setEnabled(False)
            self.ui.actionAdd_Edit_Material.setEnabled(False)
            self.ui.actionSettings.setEnabled(False)
            self.ui.actionReports.setEnabled(False)
    def materials_search_tab(self):
        self.ui.tabWidget.setCurrentIndex(0)
        self.toptabs_color(self.ui.tabWidget.currentIndex())
    def materials_add_tab(self):
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.tabWidget_4.setCurrentIndex(0)
        self.read_tabs_index()
    def stocks_edit_tab(self):
        self.ui.tabWidget.setCurrentIndex(2)
        self.ui.tabWidget_5.setCurrentIndex(0)
    def stockfield_edit_tab(self):
        self.ui.tabWidget.setCurrentIndex(3)
    def reports_tab(self):
        self.ui.tabWidget.setCurrentIndex(4)
    def settings_tab(self):
        self.ui.tabWidget.setCurrentIndex(5)
    def material_type_tab(self):
        self.ui.tabWidget_4.setCurrentIndex(1)
        self.read_tabs_index()
    def toptabs_color(self,index):
        if index==0:
            self.ui.pushButton.setStyleSheet("background-color: yellow")
            self.ui.pushButton_3.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_6.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_2.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_4.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_5.setStyleSheet("background-color: #c6c6c6")
        if index==2:
            self.ui.pushButton.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_3.setStyleSheet("background-color: yellow")
            self.ui.pushButton_6.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_2.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_4.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_5.setStyleSheet("background-color: #c6c6c6")
        if index==3:
            self.ui.pushButton.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_3.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_6.setStyleSheet("background-color: yellow")
            self.ui.pushButton_2.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_4.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_5.setStyleSheet("background-color: #c6c6c6")
        if index==1:
            self.ui.pushButton.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_3.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_6.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_2.setStyleSheet("background-color: yellow")
            self.ui.pushButton_4.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_5.setStyleSheet("background-color: #c6c6c6")
        if index==4:
            self.ui.pushButton.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_3.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_6.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_2.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_4.setStyleSheet("background-color: yellow")
            self.ui.pushButton_5.setStyleSheet("background-color: #c6c6c6")
        if index==5:
            self.ui.pushButton.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_3.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_6.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_2.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_4.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_5.setStyleSheet("background-color: yellow")
    def subtabs_color(self,index):

        if index==0:
            self.ui.pushButton_23.setStyleSheet("background-color: yellow")
            self.ui.pushButton_24.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_15.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_25.setStyleSheet("background-color: #c6c6c6")

        if index==1:
            self.ui.pushButton_23.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_24.setStyleSheet("background-color: yellow")
            self.ui.pushButton_15.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_25.setStyleSheet("background-color: #c6c6c6")
        if index==2:
            self.ui.pushButton_23.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_24.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_15.setStyleSheet("background-color: yellow")
            self.ui.pushButton_25.setStyleSheet("background-color: #c6c6c6")
        if index==3:
            self.ui.pushButton_23.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_24.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_15.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_25.setStyleSheet("background-color: yellow")
    def open_about(self):
        self.window3 = Aboutwindow()

        self.window3.setWindowTitle("About Page")
        self.window3.show()


    # ================ SUBTABS CONTROL  ===========================================

    def read_tabs_index(self):
        tab1 = self.ui.tabWidget.currentIndex()
        tab2 = self.ui.tabWidget_2.currentIndex()
        tab4 = self.ui.tabWidget_4.currentIndex()
        tab5 = self.ui.tabWidget_5.currentIndex()
        self.toptabs_color( tab1)
        self.subtabs_color(tab2)
        if tab2==0:
            alldata = self.db.show_all_room()
            self.ui.tableWidget_3.clear()
            self.table3_update(alldata, headers)
            self.ui.tabWidget_3.close()
        elif tab2==1:
            alldata=self.db.showall_cabinet_type()
            self.cabinetype_table_update(alldata, headers_cabinet_type)
            self.ui.tabWidget_3.close()

        elif tab2 == 2:
            alldata = self.db.showall_cabinet()
            self.cabinet_table_update(alldata, headers_cabinet)
            self.ui.tabWidget_3.close()
            self.update_shelf_popup(alldata)
        elif tab2 == 3:
            alldata = self.db.showall_shelf()
            self.shelf_table_update(alldata, headers_shelf)
            self.ui.groupBox_13.close()
            data = self.db.showall_cabinet()
            self.update_shelf_popup(data)
        else:
            self.ui.tableWidget_3.clear()
            self.ui.tabWidget_3.close()

        if tab4 == 0:

            alldata = self.db.showall_material()
            self.material_table_update(alldata, headers_material)

        elif tab4 == 1:
            alldata = self.db.showall_material_type()
            self.material_type_table_update(alldata, headers_material_type)
        else:
            pass

        if tab5 == 0:
            alldata = self.db.showall_stock()
            self.stock_table_update(alldata, headers_stock)
        else:
            pass
    def room_edit_tab(self):
        self.ui.tabWidget_2.setCurrentIndex(0)
    def cabinettype_edit_tab(self):
        self.ui.tabWidget_2.setCurrentIndex(1)
    def cabinet_edit_tab(self):
        self.ui.tabWidget_2.setCurrentIndex(2)
    def shelf_edit_tab(self):
        self.ui.tabWidget_2.setCurrentIndex(3)
    def stock_material_call_tab(self):
        self.ui.tabWidget_5.setCurrentIndex(1)
        data = self.db.showall_material()
        self.table_update(data, headers_material, self.ui.tableWidget_12)
    def stock_room_call_tab(self):
        data = self.db.show_all_room()
        self.table_update(data, headers, self.ui.tableWidget_14)
        self.ui.tabWidget_5.setCurrentIndex(2)
    def stock_cabinet_call_tab(self):
        data = self.db.showfilter_cabinet(filter_value="",room=self.ui.lineEdit_57.text(),)
        self.table_update(data, headers_cabinet, self.ui.tableWidget_15)
        self.ui.tabWidget_5.setCurrentIndex(3)
    def stock_shelf_call_tab(self):
        data = self.db.showfilter_shelf(filter_value="",room=self.ui.lineEdit_57.text(),cabinet=self.ui.lineEdit_58.text())
        self.table_update(data, headers_shelf, self.ui.tableWidget_16)
        self.ui.tabWidget_5.setCurrentIndex(4)
    # ===========================================================

    def read_room_data(self):
        self.room_ID = self.ui.lineEdit_12.text()
        self.roomname = self.ui.lineEdit_13.text()
        self.roomdesc = self.ui.lineEdit_14.text()
        self.roomnumber = self.ui.lineEdit_16.text()
        self.staff_name = self.ui.lineEdit_18.text()
    def check_room(self):
        self.read_room_data()
        data=self.db.check_room((self.roomname,self.roomnumber))
        return data
    def insert_data_room_table(self):
        self.read_room_data()
        if self.room_ID!="":
            self.update_data_room_table()
            return False

        if self.roomname=="" or self.roomnumber =="":
            self.ui.statusbar.showMessage('Please fill the blanks')
            warning = QMessageBox.warning(self, 'Value Error', 'Please fill the blanks', QMessageBox.Ok)
            return False
        data = self.check_room()
        if data!=[]:

            warning = QMessageBox.warning(self, 'Duplicate Error', 'this record has already registered', QMessageBox.Ok)
            self.ui.statusbar.showMessage('Please change your data')
        else:
            self.db.insert_room((self.roomname,self.roomdesc,self.roomnumber,self.staff_name))
            self.ui.statusbar.showMessage('The record added succesefully ')
        self.clear_room_fields()
        alldata = self.db.show_all_room()
        self.table3_update(alldata, headers)
    def update_data_room_table(self):
        self.read_room_data()
        values=(self.roomname,self.roomdesc,self.roomnumber,self.staff_name,int(self.room_ID))
        if self.room_ID!="":
            returnValue = self.update_msjbox(
                text="{} Nolu kayıt güncellenecektir.\nDevam Etmek için Ok tuşuna basın".format(self.room_ID),
                title="DİKKAT - Veriler güncellenecek")

            if returnValue == QMessageBox.Ok:
                self.db.update_room(values)
                self.clear_room_fields()
                alldata = self.db.show_all_room()
                self.table3_update(alldata, headers)
    def delete_data_room_table(self):
        self.read_room_data()
        if self.room_ID != '':
            returnValue = self.delete_msjbox(
                text="{} Nolu kayıt silinecektir.\nDevam Etmek için Delete tuşuna basın".format(self.room_ID),
                title="DİKKAT - Veriler silinecektir")

            if returnValue == QMessageBox.Discard:
                self.db.delete_room(int(self.room_ID))
                self.clear_room_fields()
                alldata = self.db.show_all_room()
                self.table3_update(alldata, headers)
    def clear_room_fields(self):
        self.ui.lineEdit_12.setText("")
        self.ui.lineEdit_13.setText("")
        self.ui.lineEdit_16.setText("")
        self.ui.lineEdit_14.setText("")
        self.ui.lineEdit_18.setText("")
        self.ui.lineEdit_17.setText("")
        self.read_room_data()
    def callback_data_from_room_table_widget(self):
        self.room_id = int(self.ui.tableWidget_3.item(self.ui.tableWidget_3.currentRow(), 0).text())

        data=self.db.calldata_with_id_room(self.room_id)
        if data!=None:
            self.ui.lineEdit_12.setText(str(data[0]))
            self.ui.lineEdit_13.setText(str(data[1]))
            self.ui.lineEdit_16.setText(str(data[3]))
            self.ui.lineEdit_14.setText(str(data[2]))
            self.ui.lineEdit_18.setText(str(data[4]))
            self.ui.lineEdit_17.setText(str(data[5]))
            return True
        else:
            return False
    def table3_update(self,data,headers):
        self.ui.tableWidget_3.clear()
        self.ui.tableWidget_3.setColumnCount(len(headers))
        self.ui.tableWidget_3.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_3.setRowCount(0)
        if data:
            self.ui.tableWidget_3.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_3.rowCount()
                self.ui.tableWidget_3.insertRow(row_pos)

        else:
            self.ui.tableWidget_3.clear()

    # ===========================================================
    def read_cabinet_type(self):
        self.cabinet_type_ID = self.ui.lineEdit_15.text()
        self.cabinet_type_name = self.ui.lineEdit_23.text()

        if self.cabinet_type_name == "":
            self.ui.statusbar.showMessage('Please fill the blanks')
            warning = QMessageBox.warning(self, 'Value Error', 'Please fill the blanks', QMessageBox.Ok)
            return 0
        elif self.cabinet_type_name !="" and self.cabinet_type_ID !="" :
            return 1
        elif self.cabinet_type_name !="" and self.cabinet_type_ID =="":
            return 2
    def insert_cabinet_type_table(self):
        if self.read_cabinet_type()==2:
            data = self.db.check_cabinet_type((self.cabinet_type_name))
            if data != None:

                warning = QMessageBox.warning(self, 'Duplicate Error', 'this record has already registered',
                                              QMessageBox.Ok)
                self.ui.statusbar.showMessage('Please change your data')
            else:
                self.db.insert_cabinet_type((self.cabinet_type_name))
                self.ui.statusbar.showMessage('The record added successfully ')

            alldata = self.db.showall_cabinet_type()
            self.cabinetype_table_update(alldata, headers_cabinet_type)
        elif self.read_cabinet_type()==1:
            self.update_data_cabinet_type_table()
        else:
            return None
    def callback_data_from_cabinettype_table_widget(self):
        self.cabinet_type_ID = int(self.ui.tableWidget_4.item(self.ui.tableWidget_4.currentRow(), 0).text())

        data=self.db.calldata_with_id_cabinet_type(self.cabinet_type_ID)
        if data!=None:
            self.ui.lineEdit_15.setText(str(data[0]))
            self.ui.lineEdit_23.setText(str(data[1]))

            return True
        else:
            return False
    def cabinetype_table_update(self,data,headers):
        self.ui.tableWidget_4.clear()
        self.ui.tableWidget_4.setColumnCount(len(headers))
        self.ui.tableWidget_4.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_4.setRowCount(0)
        if data:
            self.ui.tableWidget_4.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_4.rowCount()
                self.ui.tableWidget_4.insertRow(row_pos)

        else:
            self.ui.tableWidget_4.clear()
    def delete_data_cabinettype_table(self):

        if self.read_cabinet_type() == 1:
            returnValue = self.delete_msjbox(
                text="{} Nolu kayıt silinecektir.\nDevam Etmek için Delete tuşuna basın".format(self.cabinet_type_ID),
                title="DİKKAT - Veriler silinecektir")

            if returnValue == QMessageBox.Discard:
                self.db.delete_cabinet_type(int(self.cabinet_type_ID))
                self.clear_cabinettype_fields()
                alldata = self.db.showall_cabinet_type()
                self.cabinetype_table_update(alldata, headers_cabinet_type)
    def update_data_cabinet_type_table(self):
        self.read_cabinet_type()
        values = (self.cabinet_type_name, int(self.cabinet_type_ID))
        if self.cabinet_type_ID != "":
            returnValue = self.update_msjbox(
                text="{} Nolu kayıt güncellenecektir.\nDevam Etmek için Ok tuşuna basın".format(self.cabinet_type_ID),
                title="DİKKAT - Veriler güncellenecek")

            if returnValue == QMessageBox.Ok:
                self.db.update_cabinet_type(values)
                self.clear_cabinettype_fields()
                alldata = self.db.showall_cabinet_type()
                self.cabinetype_table_update(alldata, headers_cabinet_type)
    def clear_cabinettype_fields(self):
        self.ui.lineEdit_15.setText("")
        self.ui.lineEdit_23.setText("")

# ===========================================================
    def read_cabinet(self):
        self.cabinet_ID = self.ui.lineEdit_19.text()
        self.cabinet_code = self.ui.lineEdit_25.text()
        self.cabinet_type_ID = self.ui.lineEdit_33.text()
        self.cabinet_type_name = self.ui.lineEdit_26.text()
        self.cabinet_room_ID = self.ui.lineEdit_34.text()
        self.cabinet_room_name = self.ui.lineEdit_27.text()

        if self.cabinet_code == "" or self.cabinet_type_ID =="" or self.cabinet_room_ID =="":
            self.ui.statusbar.showMessage('Please fill the blanks')
            warning = QMessageBox.warning(self, 'Value Error', 'Please fill the blanks', QMessageBox.Ok)
            return 0
        elif self.cabinet_code !="" and self.cabinet_ID !="" :
            return 1
        elif self.cabinet_code !="" and self.cabinet_ID =="":
            return 2
    def insert_cabinet_table(self):
        if self.read_cabinet()==2:
            data = self.db.check_cabinet((self.cabinet_code))
            if data != None:

                warning = QMessageBox.warning(self, 'Duplicate Error', 'this record has already registered',
                                              QMessageBox.Ok)
                self.ui.statusbar.showMessage('Please change your data')
            else:
                self.db.insert_cabinet((self.cabinet_code,int(self.cabinet_type_ID),int(self.cabinet_room_ID)))
                self.ui.statusbar.showMessage('The record added successfully ')

            alldata = self.db.showall_cabinet()
            self.cabinet_table_update(alldata, headers_cabinet)
            self.clear_cabinet_fields()


        elif self.read_cabinet()==1:
            self.update_data_cabinet_table()
        else:
            return None
    def callback_data_from_cabinet_table_widget(self):
        self.cabinet_ID = int(self.ui.tableWidget_5.item(self.ui.tableWidget_5.currentRow(), 0).text())

        data=self.db.calldata_with_id_cabinet(self.cabinet_ID)
        if data!=None:
            self.ui.lineEdit_19.setText(str(data[0]))
            self.ui.lineEdit_25.setText(str(data[1]))
            self.ui.lineEdit_33.setText(str(data[4]))
            self.ui.lineEdit_26.setText(str(data[2]))
            self.ui.lineEdit_27.setText(str(data[3]))
            self.ui.lineEdit_34.setText(str(data[5]))
            return True
        else:
            return False
    def cabinet_table_update(self,data,headers):
        self.ui.tableWidget_5.clear()
        self.ui.tableWidget_5.setColumnCount(len(headers))
        self.ui.tableWidget_5.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_5.setRowCount(0)
        if data:
            self.ui.tableWidget_5.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_5.rowCount()
                self.ui.tableWidget_5.insertRow(row_pos)

        else:
            self.ui.tableWidget_5.clear()
    def delete_data_cabinet_table(self):

        if self.read_cabinet() == 1:
            returnValue = self.delete_msjbox(
                text="{} Nolu kayıt silinecektir.\nDevam Etmek için Delete tuşuna basın".format(self.cabinet_ID),
                title="DİKKAT - Veriler silinecektir")

            if returnValue == QMessageBox.Discard:
                self.db.delete_cabinet(int(self.cabinet_ID))
                self.clear_cabinet_fields()
                alldata = self.db.showall_cabinet()
                self.cabinet_table_update(alldata, headers_cabinet)
                self.clear_cabinet_fields()
    def update_data_cabinet_table(self):
        self.read_cabinet()
        values = (self.cabinet_code,int(self.cabinet_type_ID),int(self.cabinet_room_ID), int(self.cabinet_ID))
        if self.cabinet_ID != "":

            returnValue = self.update_msjbox(
                text="{} Nolu kayıt güncellenecektir.\nDevam Etmek için Ok tuşuna basın".format(self.cabinet_ID),
                title="DİKKAT - Veriler güncellenecek")

            if returnValue == QMessageBox.Ok:
                self.db.update_cabinet(values)
                self.clear_cabinet_fields()
                alldata = self.db.showall_cabinet()
                self.cabinet_table_update(alldata, headers_cabinet)
                self.clear_cabinet_fields()
    def clear_cabinet_fields(self):
        self.ui.lineEdit_19.setText("")
        self.ui.lineEdit_25.setText("")
        self.ui.lineEdit_33.setText("")
        self.ui.lineEdit_26.setText("")
        self.ui.lineEdit_27.setText("")
        self.ui.lineEdit_34.setText("")
        self.ui.tabWidget_3.close()
    def show_cabin_popup(self):
        if self.ui.tabWidget_3.isHidden():
            self.ui.tabWidget_3.show()
            self.ui.pushButton_16.setText("Close")
            self.update_cabinet_popup()
            self.update_room_popup()
        else:
            self.ui.tabWidget_3.close()
            self.ui.pushButton_16.setText("Select")
    def update_cabinet_popup(self):
        data = self.db.showall_cabinet_type()

        self.ui.tableWidget_6.clear()
        self.ui.tableWidget_6.setColumnCount(len(headers_cabinet_type))
        self.ui.tableWidget_6.setHorizontalHeaderLabels(headers_cabinet_type)
        self.ui.tableWidget_6.setRowCount(0)
        if data:
            self.ui.tableWidget_6.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_6.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_6.rowCount()
                self.ui.tableWidget_6.insertRow(row_pos)

        else:
            self.ui.tableWidget_6.clear()
    def data_from_cabinettype(self):
        self.cabinet_type_ID = int(self.ui.tableWidget_6.item(self.ui.tableWidget_6.currentRow(), 0).text())

        data=self.db.calldata_with_id_cabinet_type(self.cabinet_type_ID)
        if data!=None:
            self.ui.lineEdit_33.setText(str(data[0]))
            self.ui.lineEdit_26.setText(str(data[1]))

            return True
        else:
            return False

    def update_room_popup(self):
        data = self.db.show_all_room()

        self.ui.tableWidget_7.clear()
        self.ui.tableWidget_7.setColumnCount(len(headers))
        self.ui.tableWidget_7.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_7.setRowCount(0)
        if data:
            self.ui.tableWidget_7.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_7.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_7.rowCount()
                self.ui.tableWidget_7.insertRow(row_pos)

        else:
            self.ui.tableWidget_7.clear()
    def data_from_room(self):
        self.room_ID = int(self.ui.tableWidget_7.item(self.ui.tableWidget_7.currentRow(), 0).text())

        data=self.db.calldata_with_id_room(self.room_ID)
        if data!=None:
            self.ui.lineEdit_34.setText(str(data[0]))
            self.ui.lineEdit_27.setText(str(data[1]))

            return True
        else:
            return False
    def filter_cabinet(self):
        self.filter_val_cabinet=self.ui.lineEdit_24.text()
        self.criteria_val_cabinet = self.ui.comboBox_7.currentIndex()

        data = self.db.showfilter_cabinet(index=self.criteria_val_cabinet,filter_value=self.filter_val_cabinet,room="")
        self.update_shelf_popup(data)
# ===========================================================
    def read_shelf(self):
        self.shelf_ID = self.ui.lineEdit_22.text()
        self.shelf_code = self.ui.lineEdit_28.text()
        self.shelf_cabinet_code = self.ui.lineEdit_29.text()
        self.shelf_cabinet_ID = self.ui.lineEdit_31.text()
        self.shelf_room_ID = self.ui.lineEdit_32.text()
        self.shelf_room_name = self.ui.lineEdit_30.text()

        if self.shelf_code == "" or self.shelf_cabinet_ID == "" or self.shelf_room_ID == "":
            self.ui.statusbar.showMessage('Please fill the blanks')
            warning = QMessageBox.warning(self, 'Value Error', 'Please fill the blanks', QMessageBox.Ok)
            print(0)
            return 0
        elif self.shelf_code != "" and self.shelf_ID != "":
            return 1
        elif self.shelf_code != "" and self.shelf_ID == "":
            return 2
    def insert_shelf_table(self):
        if self.read_shelf()==2:
            data = self.db.check_shelf((self.shelf_code))
            if data != None:

                warning = QMessageBox.warning(self, 'Duplicate Error', 'this record has already registered',
                                              QMessageBox.Ok)
                self.ui.statusbar.showMessage('Please change your data')
            else:
                self.db.insert_shelf((self.shelf_code,int(self.shelf_cabinet_ID)))
                self.ui.statusbar.showMessage('The record added successfully ')

            alldata = self.db.showall_shelf()
            self.shelf_table_update(alldata, headers_shelf)
            self.clear_shelf_fields()


        elif self.read_shelf()==1:
            self.update_data_shelf_table()
        else:
            return None
    def callback_from_shelf_table(self):
        self.shelf_ID = int(self.ui.tableWidget_8.item(self.ui.tableWidget_8.currentRow(), 0).text())

        data=self.db.calldata_with_id_shelf(self.shelf_ID)
        if data!=None:
            self.ui.lineEdit_22.setText(str(data[0]))
            self.ui.lineEdit_28.setText(str(data[1]))
            self.ui.lineEdit_31.setText(str(data[4]))
            self.ui.lineEdit_29.setText(str(data[2]))
            self.ui.lineEdit_30.setText(str(data[3]))
            self.ui.lineEdit_32.setText(str(data[5]))
            return True
        else:
            return False
    def shelf_table_update(self,data,headers):
        self.ui.tableWidget_8.clear()
        self.ui.tableWidget_8.setColumnCount(len(headers))
        self.ui.tableWidget_8.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_8.setRowCount(0)
        if data:
            self.ui.tableWidget_8.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_8.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_8.rowCount()
                self.ui.tableWidget_8.insertRow(row_pos)

        else:
            self.ui.tableWidget_8.clear()
    def delete_data_shelf_table(self):

        if self.read_shelf() == 1:
            returnValue = self.delete_msjbox(
                text="{} Nolu kayıt silinecektir.\nDevam Etmek için Delete tuşuna basın".format(self.shelf_ID),
                title="DİKKAT - Veriler silinecektir")

            if returnValue == QMessageBox.Discard:
                self.db.delete_shelf(int(self.shelf_ID))

                alldata = self.db.showall_shelf()
                self.shelf_table_update(alldata, headers_shelf)
                self.clear_shelf_fields()
    def update_data_shelf_table(self):
        self.read_shelf()
        values = (self.shelf_code,int(self.shelf_cabinet_ID),self.shelf_ID)
        if self.shelf_ID != "":
            returnValue = self.update_msjbox(
                text="{} Nolu kayıt güncellenecektir.\nDevam Etmek için Ok tuşuna basın".format(self.shelf_ID),
                title="DİKKAT - Veriler güncellenecek")

            if returnValue == QMessageBox.Ok:
                self.db.update_shelf(values)

                alldata = self.db.showall_shelf()
                self.shelf_table_update(alldata, headers_shelf)
                self.clear_shelf_fields()

    def clear_shelf_fields(self):
        self.ui.lineEdit_22.setText("")
        self.ui.lineEdit_28.setText("")
        self.ui.lineEdit_29.setText("")
        self.ui.lineEdit_31.setText("")
        self.ui.lineEdit_32.setText("")
        self.ui.lineEdit_30.setText("")
        self.ui.groupBox_13.close()
    def show_shelf_popup(self):
        if self.ui.groupBox_13.isHidden():
            self.ui.groupBox_13.show()
            self.ui.pushButton_28.setText("Close")
            self.update_cabinet_popup()
            self.update_room_popup()
        else:
            self.ui.groupBox_13.close()
            self.ui.pushButton_28.setText("Select")
    def update_shelf_popup(self,data):


        self.ui.tableWidget_9.clear()
        self.ui.tableWidget_9.setColumnCount(len(headers_cabinet))
        self.ui.tableWidget_9.setHorizontalHeaderLabels(headers_cabinet)
        self.ui.tableWidget_9.setRowCount(0)
        if data:
            self.ui.tableWidget_9.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_9.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_9.rowCount()
                self.ui.tableWidget_9.insertRow(row_pos)

        else:
            self.ui.tableWidget_9.clear()
    def data_from_cabinet(self):
        self.shelf_cabinet_ID = int(self.ui.tableWidget_9.item(self.ui.tableWidget_9.currentRow(), 0).text())

        data=self.db.calldata_with_id_cabinet(self.shelf_cabinet_ID)
        if data!=None:
            self.ui.lineEdit_31.setText(str(data[0]))
            self.ui.lineEdit_29.setText(str(data[1]))
            self.ui.lineEdit_30.setText(str(data[3]))
            self.ui.lineEdit_32.setText(str(data[5]))
            return True
        else:
            return False
    def filter_shelf_table(self):
        self.filter_val_shelf=self.ui.lineEdit_54.text()
        alldata = self.db.showfilter_shelf(filter_value=self.filter_val_shelf)
        self.shelf_table_update(alldata, headers_shelf)
# ==========================================================================
    def read_material_type(self):
        self.mat_type_ID = self.ui.lineEdit_46.text()
        self.mat_type_name = self.ui.lineEdit_49.text()
        if self.mat_type_name == "":
            self.ui.statusbar.showMessage('Please fill the blanks')
            warning = QMessageBox.warning(self, 'Value Error', 'Please fill the blanks', QMessageBox.Ok)

            return 0
        elif self.mat_type_name != "" and self.mat_type_ID != "":
            return 1
        elif self.mat_type_name != "" and self.mat_type_ID == "":
            return 2
    def insert_material_type_table(self):
        result=self.read_material_type()
        if result==2:
            data = self.db.check_material_type((self.mat_type_name))
            if data != None:

                warning = QMessageBox.warning(self, 'Duplicate Error', 'this record has already registered',
                                              QMessageBox.Ok)
                self.ui.statusbar.showMessage('Please change your data')
            else:
                self.db.insert_material_type((self.mat_type_name))
                self.ui.statusbar.showMessage('The record added successfully ')

            alldata = self.db.showall_material_type()
            self.material_type_table_update(alldata, headers_material_type)
            self.clear_material_type_fields()

        elif result==1:
            self.update_data_material_type_table()
        else:
            return None
    def callback_data_from_material_type_table_widget(self):
        self.mat_type_ID = int(self.ui.tableWidget_11.item(self.ui.tableWidget_11.currentRow(), 0).text())

        data=self.db.calldata_with_id_material_type(self.mat_type_ID)
        if data!=None:
            self.ui.lineEdit_46.setText(str(data[0]))
            self.ui.lineEdit_49.setText(str(data[1]))

            return True
        else:
            return False
    def material_type_table_update(self,data,headers):
        self.ui.tableWidget_11.clear()
        self.ui.tableWidget_11.setColumnCount(len(headers))
        self.ui.tableWidget_11.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_11.setRowCount(0)
        if data:
            self.ui.tableWidget_11.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_11.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_11.rowCount()
                self.ui.tableWidget_11.insertRow(row_pos)

        else:
            self.ui.tableWidget_11.clear()
    def delete_data_material_type_table(self):

        if self.read_material_type() == 1:
            returnValue = self.delete_msjbox(
                text="{} Nolu kayıt silinecektir.\nDevam Etmek için Delete tuşuna basın".format(self.mat_type_ID),
                title="DİKKAT - Veriler silinecektir")

            if returnValue == QMessageBox.Discard:
                self.db.delete_material_type(int(self.mat_type_ID))
                self.clear_material_type_fields()
                alldata = self.db.showall_material_type()
                self.material_type_table_update(alldata, headers_material_type)
    def update_data_material_type_table(self):
        self.read_material_type()
        values = (self.mat_type_name, int(self.mat_type_ID))
        if self.mat_type_ID != "":
            returnValue = self.update_msjbox(
                text="{} Nolu kayıt güncellenecektir.\nDevam Etmek için Ok tuşuna basın".format(self.mat_type_ID),
                title="DİKKAT - Veriler güncellenecek")

            if returnValue == QMessageBox.Ok:
                self.db.update_material_type(values)
                self.clear_material_type_fields()
                alldata = self.db.showall_material_type()
                self.material_type_table_update(alldata, headers_material_type)
    def clear_material_type_fields(self):
        self.ui.lineEdit_46.setText("")
        self.ui.lineEdit_49.setText("")
    def data_from_material_type(self):


        data=self.db.calldata_with_id_material_type(self.mat_type_ID)
        if data!=None:
            self.ui.lineEdit_52.setText(str(data[0]))
            self.ui.lineEdit_50.setText(str(data[1]))
            self.ui.tabWidget_4.setCurrentIndex(0)

            return True
        else:
            return False
    def filter_material_type_table(self):
        self.filter_val_material_type=self.ui.lineEdit_53.text()
        alldata = self.db.showfilter_material_type(self.filter_val_material_type)
        self.material_type_table_update(alldata, headers_material_type)
# ==========================================================================
    def image_file_dialog_open_material(self):
        if not self.ui.lineEdit_45.text():
            warning = QMessageBox.warning(self, 'Missing Data', ' Please enter "Code-1" before add a picture', QMessageBox.Ok)
            self.statusBar().showMessage('Missing Data')
        else:
            self.filepath, _ = QFileDialog.getOpenFileName(filter='Image File *.png , *.jpg ')
            filename = QFileInfo(self.filepath).fileName()
            if filename =="":
                pass
            else:

                new_file_name = self.ui.lineEdit_45.text()  + '.png'
                self.ui.lineEdit_44.setText(new_file_name)
                picture = QPixmap( self.filepath)
                self.ui.label_49.setPixmap(picture)
                self.ui.label_49.setScaledContents(True)
    def save_image_material(self,oldfilepath,new_file_name):
        try :
            shutil.copyfile(oldfilepath, IMAGE_DIR + new_file_name)
        except Exception as err:
            print(err)

    def load_image_from_location(self):
        picture = QPixmap(IMAGE_DIR+self.ui.lineEdit_44.text())
        self.ui.label_49.setPixmap(picture)
        self.ui.label_49.setScaledContents(True)
        self.filepath =""
    def read_material(self):
        self.material_ID = self.ui.lineEdit_51.text()
        self.material_type_ID = self.ui.lineEdit_52.text()
        self.material_type_name = self.ui.lineEdit_50.text()
        self.material_name = self.ui.lineEdit_41.text()
        self.material_code1 = self.ui.lineEdit_45.text()
        self.material_code2 = self.ui.lineEdit_47.text()
        self.material_image_name = self.ui.lineEdit_44.text()
        self.material_manufacture = self.ui.lineEdit_48.text()
        self.material_price = self.ui.lineEdit_43.text()
        self.material_unit = self.ui.comboBox_8.currentText()
        self.material_property1 = self.ui.textEdit.toPlainText()
        self.material_property2 = self.ui.textEdit_2.toPlainText()

        if self.material_type_ID == "" or self.material_name == "" or self.material_code1 == ""\
                or self.material_property1 =="" :
            self.ui.statusbar.showMessage('Please fill the blanks')
            warning = QMessageBox.warning(self, 'Value Error', 'Please fill the blanks', QMessageBox.Ok)

            return 0
        elif  self.material_ID != "":

            return 1
        elif self.material_ID == "":

            return 2
    def insert_material_table(self):
        result=self.read_material()
        if  result== 2:
            data = self.db.check_material((self.material_name))
            if data != None:

                warning = QMessageBox.warning(self, 'Duplicate Error', 'this record has already registered',
                                              QMessageBox.Ok)
                self.ui.statusbar.showMessage('Please change your data')
            else:
                self.db.insert_material((self.material_type_ID,self.material_name,self.material_code1,
                                         self.material_code2,self.material_property1,self.material_property2,
                                         self.material_manufacture,self.material_price,self.material_unit,self.material_image_name))
                if self.material_image_name!="":
                    self.save_image_material(self.filepath,self.material_image_name)
                self.ui.statusbar.showMessage('The record added successfully ')

            alldata = self.db.showall_material()
            self.material_table_update(alldata, headers_material)
        elif result == 1:
            self.update_data_material_table()
        else:
            return None
    def callback_from_material_table(self):
        self.material_ID = int(self.ui.tableWidget_10.item(self.ui.tableWidget_10.currentRow(), 0).text())

        data = self.db.calldata_with_id_material(self.material_ID)
        if data != None:

            self.ui.lineEdit_51.setText(str(data[0]))
            self.ui.lineEdit_52.setText(str(data[1]))
            self.ui.lineEdit_50.setText(str(data[2]))
            self.ui.lineEdit_41.setText(str(data[3]))
            self.ui.lineEdit_45.setText(str(data[4]))
            self.ui.lineEdit_47.setText(str(data[5]))
            self.ui.lineEdit_44.setText(str(data[11]))
            self.ui.lineEdit_48.setText(str(data[8]))
            self.ui.lineEdit_43.setText(str(data[9]))
            self.ui.comboBox_8.setCurrentText(str(data[10]))
            self.ui.textEdit.setPlainText(str(data[6]))
            self.ui.textEdit_2.setPlainText(str(data[7]))
            self.load_image_from_location()
            return True
        else:
            return False
    def material_table_update(self,data,headers):
        self.ui.tableWidget_10.clear()
        self.ui.tableWidget_10.setColumnCount(len(headers))
        self.ui.tableWidget_10.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_10.setRowCount(0)
        if data:
            self.ui.tableWidget_10.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_10.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_10.rowCount()
                self.ui.tableWidget_10.insertRow(row_pos)

        else:
            self.ui.tableWidget_10.clear()
    def delete_data_material_table(self):

        if self.read_material() == 1:
            returnValue = self.delete_msjbox(
                text="{} Nolu kayıt silinecektir.\nDevam Etmek için Delete tuşuna basın".format(self.material_ID),
                title="DİKKAT - Veriler silinecektir")

            if returnValue == QMessageBox.Discard:
                self.db.delete_material(int(self.material_ID))

                alldata = self.db.showall_material()
                self.material_table_update(alldata, headers_material)
                self.clear_material_fields()
    def update_data_material_table(self):
        self.read_material()
        values = ((self.material_type_ID,self.material_name,self.material_code1,
                                         self.material_code2,self.material_property1,self.material_property2,
                                         self.material_manufacture,self.material_price,self.material_unit,self.material_image_name,self.material_ID))
        if self.material_ID != "":

            returnValue = self.update_msjbox(
                text="{} Nolu kayıt güncellenecektir.\nDevam Etmek için Ok tuşuna basın".format(self.material_ID),
                title="DİKKAT - Veriler güncellenecek")

            if returnValue == QMessageBox.Ok:
                self.db.update_material(values)
                if self.filepath!="" :
                    self.save_image_material(self.filepath,self.material_image_name)
                else:
                   self.save_image_material(IMAGE_DIR+self.material_image_name, self.material_image_name)
                self.clear_material_fields()
                alldata = self.db.showall_material()
                self.material_table_update(alldata, headers_material)
    def clear_material_fields(self):
        self.material_ID = self.ui.lineEdit_51.setText("")
        self.material_type_ID = self.ui.lineEdit_52.setText("")
        self.material_type_name = self.ui.lineEdit_50.setText("")
        self.material_name = self.ui.lineEdit_41.setText("")
        self.material_code1 = self.ui.lineEdit_45.setText("")
        self.material_code2 = self.ui.lineEdit_47.setText("")
        self.material_image_name = self.ui.lineEdit_44.setText("")
        self.material_manufacture = self.ui.lineEdit_48.setText("")
        self.material_price = self.ui.lineEdit_43.setText("")
        self.ui.label_49.setPixmap(None)
        self.material_property1 = self.ui.textEdit.setPlainText("")
        self.material_property2 = self.ui.textEdit_2.setPlainText("")
        self.filepath=""
    def filter_material_table(self):
        self.filter_val_material = self.ui.lineEdit_55.text()
        self.criteria_val_material = self.ui.comboBox_9.currentIndex()

        data = self.db.showfilter_material(self.criteria_val_material, self.filter_val_material )

        self.material_table_update(data, headers_material)


# ================== STOCKS ===============================================
    def read_stock(self):
        self.stock_ID = self.ui.lineEdit_69.text()
        self.stock_code = self.ui.lineEdit_65.text()
        self.finalstock_code = self.ui.lineEdit_68.text()
        self.quantity=self.ui.lineEdit_67.text()
        self.unit=self.ui.comboBox_5.currentText()
        self.stock_material_code = self.ui.lineEdit_56.text()
        self.stock_room_name= self.ui.lineEdit_57.text()
        self.stock_cabinet_code = self.ui.lineEdit_58.text()
        self.stock_shelf_code = self.ui.lineEdit_59.text()
        self.stock_userID = self.ui.lineEdit.text()
        self.stock_shelf_ID =self.ui.lineEdit_73.text()
        self.stock_material_ID =self.ui.lineEdit_70.text()
        self.stock_cabinet_ID =self.ui.lineEdit_72.text()
        self.stock_room_ID =self.ui.lineEdit_71.text()

        if self.stock_code == "" or self.finalstock_code == "" or self.quantity == ""\
                or self.stock_material_code =="" or self.stock_room_name =="" or self.stock_cabinet_code ==""\
                or self.stock_shelf_code =="" :
            self.ui.statusbar.showMessage('Please fill the blanks')
            warning = QMessageBox.warning(self, 'Value Error', 'Please fill the blanks', QMessageBox.Ok)

            return 0
        elif  self.stock_ID != "" :

            return 1
        elif self.stock_ID == "" :

            return 2
    def final_stockcode_generate(self):

        self.ui.lineEdit_68.setText("STK-"+self.ui.lineEdit_65.text()+"-"+self.ui.lineEdit_56.text()+"-"+self.ui.lineEdit_57.text()+"-"+
                                    self.ui.lineEdit_58.text()+"-"+self.ui.lineEdit_59.text())
    def insert_stock_table(self):
        result=self.read_stock()
        print(result)
        if  result== 2:
            data = self.db.check_stock((self.finalstock_code))
            if data != None:

                warning = QMessageBox.warning(self, 'Duplicate Error', 'this record has already registered',
                                              QMessageBox.Ok)
                self.ui.statusbar.showMessage('Please change your data')
            else:
                self.db.insert_stock((self.finalstock_code,self.stock_shelf_ID,self.stock_material_ID,self.quantity,self.unit,self.stock_userID))

                self.ui.statusbar.showMessage('The record added successfully ')

            alldata = self.db.showall_stock()
            self.stock_table_update(alldata, headers_stock)
            self.clear_stock_fields()
        elif result == 1:
            self.update_data_stock_table()
        else:
            return None
    def callback_from_stock_table(self):
        self.stock_ID = int(self.ui.tableWidget_13.item(self.ui.tableWidget_13.currentRow(), 0).text())

        data = self.db.calldata_with_id_stock(self.stock_ID)
        if data != None:
            code=str(data[1]).split(sep="-")
            self.ui.lineEdit_69.setText(str(data[0]))
            self.ui.lineEdit_65.setText(code[1])
            self.ui.lineEdit_68.setText(str(data[1]))
            self.ui.lineEdit_67.setText(str(data[9]))
            self.ui.comboBox_5.setCurrentText(str(data[10]))
            self.ui.lineEdit_56.setText(str(data[3]))
            self.ui.lineEdit_57.setText(str(data[8]))
            self.ui.lineEdit_58.setText(str(data[6]))
            self.ui.lineEdit_59.setText(str(data[5]))
            self.ui.lineEdit_66.setText(str(data[12]))
            self.ui.lineEdit_70.setText(str(data[13]))
            self.ui.lineEdit_71.setText(str(data[14]))
            self.ui.lineEdit_72.setText(str(data[15]))
            self.ui.lineEdit_73.setText(str(data[16]))
            picture = QPixmap(IMAGE_DIR + data[17])
            self.ui.label_62.setPixmap(picture)
            self.ui.label_62.setScaledContents(True)

            return True
        else:
            return False
    def stock_table_update(self,data,headers):
        self.ui.tableWidget_13.clear()
        self.ui.tableWidget_13.setColumnCount(len(headers))
        self.ui.tableWidget_13.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_13.setRowCount(0)
        if data:
            self.ui.tableWidget_13.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    self.ui.tableWidget_13.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = self.ui.tableWidget_13.rowCount()
                self.ui.tableWidget_13.insertRow(row_pos)

        else:
            self.ui.tableWidget_13.clear()
    def delete_data_stock_table(self):

        if self.read_stock() == 1:
            returnValue = self.delete_msjbox(
                text="{} Nolu kayıt siliniecektir.\nDevam Etmek için Delete tuşuna basın".format(self.stock_ID),
                title="DİKKAT - Veri Silinecek")

            if returnValue == QMessageBox.Discard:
                self.db.delete_stock(int(self.stock_ID))

                alldata = self.db.showall_stock()
                self.stock_table_update(alldata, headers_stock)
                self.clear_stock_fields()
    def update_data_stock_table(self):
        self.read_stock()
        values = ((self.finalstock_code,self.stock_shelf_ID,self.stock_material_ID,self.quantity,self.unit,self.stock_userID,self.stock_ID))
        if self.stock_ID != "":
            returnValue = self.update_msjbox(
                text="{} Nolu kayıt güncellenecektir.\nDevam Etmek için Ok tuşuna basın".format(self.stock_ID),
                title="DİKKAT - Veriler güncellenecek")

            if returnValue == QMessageBox.Ok:
                self.db.update_stock(values)

                alldata = self.db.showall_stock()
                self.stock_table_update(alldata, headers_stock)
    def clear_stock_fields(self):
        self.ui.lineEdit_69.setText("")
        self.ui.lineEdit_65.setText("")
        self.ui.lineEdit_66.setText("")

        self.ui.lineEdit_67.setText("")
        self.ui.comboBox_5.setCurrentText("")
        self.ui.lineEdit_56.setText("")
        self.ui.lineEdit_57.setText("")
        self.ui.lineEdit_58.setText("")
        self.ui.lineEdit_59.setText("")

        self.ui.lineEdit_70.setText("")
        self.ui.lineEdit_71.setText("")
        self.ui.lineEdit_72.setText("")
        self.ui.lineEdit_73.setText("")
        self.ui.lineEdit_68.setText("")
        self.ui.label_62.setPixmap(None)
    def filter_stock_table(self):
        self.filter_val_stock = self.ui.lineEdit_61.text()
        self.criteria_val_stock = self.ui.comboBox_11.currentIndex()

        data = self.db.showfilter_stock(self.criteria_val_stock, self.filter_val_stock )

        self.stock_table_update(data, headers_stock)

    def material_table_clicked(self):
        self.ui.lineEdit_70.setText(self.ui.tableWidget_12.item(self.ui.tableWidget_12.currentRow(), 0).text())
        self.ui.lineEdit_56.setText(self.ui.tableWidget_12.item(self.ui.tableWidget_12.currentRow(), 3).text())
        picture = QPixmap(IMAGE_DIR + self.ui.tableWidget_12.item(self.ui.tableWidget_12.currentRow(), 10).text())
        self.ui.label_62.setPixmap(picture)
        self.ui.label_62.setScaledContents(True)
        self.ui.tabWidget_5.setCurrentIndex(2)
        self.ui.lineEdit_57.setText("")
        self.ui.lineEdit_58.setText("")
        self.ui.lineEdit_59.setText("")
        self.ui.lineEdit_71.setText("")
        self.ui.lineEdit_72.setText("")
        self.ui.lineEdit_73.setText("")
        self.filter_stock_room_table()
    def room_table_clicked(self):
        self.ui.lineEdit_71.setText(self.ui.tableWidget_14.item(self.ui.tableWidget_14.currentRow(), 0).text())
        self.ui.lineEdit_57.setText(self.ui.tableWidget_14.item(self.ui.tableWidget_14.currentRow(), 1).text())
        self.ui.tabWidget_5.setCurrentIndex(3)
        self.ui.lineEdit_58.setText("")
        self.ui.lineEdit_59.setText("")
        self.ui.lineEdit_72.setText("")
        self.ui.lineEdit_73.setText("")
        self.filter_stock_cabinet_table()
    def cabinet_table_clicked(self):
        self.ui.lineEdit_72.setText(self.ui.tableWidget_15.item(self.ui.tableWidget_15.currentRow(), 0).text())
        self.ui.lineEdit_58.setText(self.ui.tableWidget_15.item(self.ui.tableWidget_15.currentRow(), 1).text())
        self.ui.lineEdit_57.setText(self.ui.tableWidget_15.item(self.ui.tableWidget_15.currentRow(), 3).text())
        self.ui.tabWidget_5.setCurrentIndex(4)

        self.ui.lineEdit_59.setText("")
        self.filter_stock_shelf_table()
        self.ui.lineEdit_73.setText("")
    def shelf_table_clicked(self):
        self.ui.lineEdit_57.setText(self.ui.tableWidget_16.item(self.ui.tableWidget_16.currentRow(), 3).text())
        self.ui.lineEdit_58.setText(self.ui.tableWidget_16.item(self.ui.tableWidget_16.currentRow(), 2).text())
        self.ui.lineEdit_73.setText(self.ui.tableWidget_16.item(self.ui.tableWidget_16.currentRow(), 0).text())
        self.ui.lineEdit_59.setText(self.ui.tableWidget_16.item(self.ui.tableWidget_16.currentRow(), 1).text())

        self.ui.tabWidget_5.setCurrentIndex(0)

    def filter_stock_material_table(self):
        self.ui.lineEdit_60.text()
        self.ui.comboBox_10.currentIndex()

        data = self.db.showfilter_material(self.ui.comboBox_10.currentIndex(), self.ui.lineEdit_60.text() )

        self.table_update(data, headers_material, self.ui.tableWidget_12)
    def filter_stock_room_table(self):
        self.ui.lineEdit_62.text()
        self.ui.comboBox_12.currentIndex()

        data = self.db.showfilter_room(index=self.ui.comboBox_12.currentIndex(), filter_value=self.ui.lineEdit_62.text() )

        self.table_update(data, headers, self.ui.tableWidget_14)
    def filter_stock_cabinet_table(self):
        self.ui.lineEdit_63.text()
        self.ui.comboBox_13.currentIndex()
        data = self.db.showfilter_cabinet(index=self.ui.comboBox_13.currentIndex(),filter_value= self.ui.lineEdit_63.text(),room=self.ui.lineEdit_57.text() )
        self.table_update(data, headers_cabinet, self.ui.tableWidget_15)
    def filter_stock_shelf_table(self):
        self.ui.lineEdit_64.text()
        self.ui.comboBox_14.currentIndex()

        data = self.db.showfilter_shelf(index=self.ui.comboBox_14.currentIndex(), filter_value=self.ui.lineEdit_64.text(),room=self.ui.lineEdit_57.text(),cabinet=self.ui.lineEdit_58.text() )

        self.table_update(data, headers_shelf, self.ui.tableWidget_16)

    def stock_search_table_clicked(self):
        self.ui.lineEdit_75.setText(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 0).text())

        data = self.db.calldata_with_id_stock(int(self.ui.lineEdit_75.text()))
        if data != None:
            code = str(data[1]).split(sep="-")
            self.ui.lineEdit_77.setText(str(data[1]))
            self.ui.lineEdit_76.setText(code[1])
            self.ui.lineEdit_2.setText(str(data[2]))
            self.ui.lineEdit_42.setText(str(data[9]))
            self.ui.lineEdit_78.setText(str(data[10]))
            self.ui.lineEdit_3.setText(str(data[3]))
            self.ui.lineEdit_35.setText(str(data[8]))
            self.ui.lineEdit_36.setText(str(data[6]))
            self.ui.lineEdit_37.setText(str(data[5]))
            self.ui.lineEdit_80.setText(str(data[12]))
            self.ui.lineEdit_81.setText(str(data[13]))
            self.ui.lineEdit_38.setText(str(data[14]))
            self.ui.lineEdit_39.setText(str(data[15]))
            self.ui.lineEdit_40.setText(str(data[16]))
            picture = QPixmap(IMAGE_DIR + data[17])
            self.ui.label.setPixmap(picture)
            self.ui.label.setScaledContents(True)
            self.ui.lineEdit_7.setText(str(data[18]))
            self.ui.lineEdit_4.setText(str(data[19]))
            self.ui.lineEdit_5.setText(str(data[4]))
            self.ui.lineEdit_6.setText(str(data[20]))
            self.ui.lineEdit_8.setText(str(data[21]))
            self.ui.lineEdit_79.setText(str(data[22]))
            self.ui.lineEdit_74.setText(str(data[23]))

            self.qrcode_gen(code=self.ui.lineEdit_77.text(),label=self.ui.label_71)
            return True
        else:
            return False
    def filter_stock_search_table(self):

        data = self.db.showfilter_stock(self.ui.comboBox_15.currentIndex(), self.ui.lineEdit_9.text())
        self.table_update(data, headers_stock,self.ui.tableWidget)
    def log_page_call(self):
        if self.ui.lineEdit_75.text()!="":
            self.window2 = logwindow()
            self.window2.ui.lineEdit_75.setText(self.ui.lineEdit_75.text())
            self.window2.ui.lineEdit_7.setText(self.ui.lineEdit.text())

            self.window2.show()
            self.window2.stock_data_call()
        else:
            warning = QMessageBox.warning(self, 'Data Error', 'Please select a stock before do it',
                                          QMessageBox.Ok)
            self.ui.statusbar.showMessage('Please select a stock')
    def logout_myapp(self):
        self.window = Login()

        self.close()
        self.window.show()
    def filter_logs_table(self):
        data = self.db.showfilter_logs(self.ui.comboBox_16.currentIndex(), self.ui.lineEdit_83.text())
        self.table_update(data, headers_logs,self.ui.tableWidget_17)
    def table_update(self,data,headers,sender):
        sender.clear()
        sender.setColumnCount(len(headers))
        sender.setHorizontalHeaderLabels(headers)
        sender.setRowCount(0)
        if data:
            sender.insertRow(0)
            # self.ui.tableWidget_3.insertColumn(0)

            for row, form in enumerate(data):

                for column, item in enumerate(form):
                    sender.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_pos = sender.rowCount()
                sender.insertRow(row_pos)

        else:
            sender.clear()

    # ================== export ===============================================
    def export_report(self):
        start = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh-mm-ss")
        finish = self.ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh-mm-ss")
        try:
            data = self.db.show_betweendate_logs(start=start, finish=finish)

        except Exception as err:
            print(err)
            warning = QMessageBox.warning(self, 'Data Error', 'Error is {}'.format(err), QMessageBox.Ok)
            self.ui.statusbar.showMessage('Error is {}'.format(err))

        if data!=[]:
            wb = Wb(REPORT_DIR + '\\report_{}.xlsx'.format(datetime.date.today()), )
            sheet1 = wb.add_worksheet()
            for i in range(len(headers_logs)):
                sheet1.write(0, i, headers_logs[i])




            row_number = 1
            for row in data:
                column_num = 0
                for item in row:
                    sheet1.write(row_number, column_num, str(item))
                    column_num += 1
                row_number += 1

            wb.close()
            information = QMessageBox.information(self, 'Export has been done', 'plesae check the excel file :{} '.format(
                (REPORT_DIR + '\\report_{}.xlsx'.format(datetime.date.today())),),QMessageBox.Ok)
            self.ui.statusbar.showMessage('Export has been done')
        else:
            warning = QMessageBox.warning(self, 'Data Error', 'Please change your date', QMessageBox.Ok)

            self.ui.statusbar.showMessage('Please change your date')
    # ================== user ===============================================
    def read_user_data(self):
        self.userID = self.ui.lineEdit_10.text()
        self.username=self.ui.lineEdit_11.text()
        self.psw1 = self.ui.lineEdit_86.text()
        self.psw2 = self.ui.lineEdit_87.text()
        self.usertype=self.ui.comboBox_4.currentText()

        if self.username=="" or self.psw1=="" or self.psw2=="" :
            self.ui.statusbar.showMessage('Please fill the blanks')
            warning = QMessageBox.warning(self, 'Value Error', 'Please fill the blanks', QMessageBox.Ok)
            return 0
        elif self.userID!="" and  self.psw1== self.psw2 :
            return 1
        elif self.userID!="" and  (self.psw1!= self.psw2 ):
            self.ui.statusbar.showMessage('Password Error')
            warning = QMessageBox.warning(self, 'Wrong password', 'Please re-enter passwords', QMessageBox.Ok)
            return 2
        else :
            return 3
    def clear_user_fields(self):
        self.ui.lineEdit_10.setText("")
        self.ui.lineEdit_11.setText("")
        self.ui.lineEdit_86.setText("")
        self.ui.lineEdit_87.setText("")
        self.ui.comboBox_4.setCurrentText("")
    def callback_from_user_table(self):
        self.userID = int(self.ui.tableWidget_2.item(self.ui.tableWidget_2.currentRow(), 0).text())

        data = self.db.calldata_with_id_user(self.userID)
        if data != None:
            self.ui.lineEdit_10.setText(str(data[0]))
            self.ui.lineEdit_11.setText(str(data[1]))
            self.ui.lineEdit_86.setText(str(data[2]))
            self.ui.comboBox_4.setCurrentText(data[3])
            return True
        else:
            return False
    def filter_user_table(self):
        data = self.db.showfilter_user(self.ui.lineEdit_88.text())

        self.table_update(data, headers_user, self.ui.tableWidget_2)
    def delete_data_user_table(self):

        if self.read_user_data() == 1:
            returnValue = self.delete_msjbox(text="{} Nolu kayıt silinecektir.\nDevam Etmek için Delete tuşuna basın".format(self.userID),
                                             title="DİKKAT - Veri Silinecek")

            if returnValue == QMessageBox.Discard:
                self.db.delete_user(int(self.userID))

                data = self.db.showall_user()
                self.table_update(data, headers_user, self.ui.tableWidget_2)
                self.clear_user_fields()
    def update_data_user_table(self):
        if self.read_user_data()==1:

            values = (( self.username,self.psw1,self.usertype,self.userID))
            returnValue = self.update_msjbox(text="{} adlı kayıt güncellenecektir.\nDevam Etmek için Ok tuşuna basın".format(self.username),
                               title="DİKKAT - Veriler güncellenecek")

            if returnValue == QMessageBox.Ok:
                self.db.update_user(values)

                data = self.db.showall_user()
                self.table_update(data, headers_user, self.ui.tableWidget_2)
                self.clear_user_fields()

    def qrcode_gen(self,code,label):
        qrcode=pyqrcode.create(code,mode='binary')
        label.setText(str(qrcode))
        qrcode.png('code.png', scale=6)
        picture = QPixmap('code.png')
        label.setPixmap(picture)
        label.setScaledContents(True)
        return picture
    def save_qrcode_png(self):
        cqrcode = self.qrcode_gen(code=self.ui.lineEdit_77.text(), label=self.ui.label_71)
        name,_ = QFileDialog.getSaveFileName(self,"Save File",dir="code.png")
        shutil.copyfile("code.png", name)
    # ================== language ===============================================
    def translate(self):

        if self.sender().objectName()=="pushButton_67":
            self.ui.pushButton_67.setStyleSheet("background-color: yellow")
            self.ui.pushButton_66.setStyleSheet("background-color: #c6c6c6")

            write_parameter(9, "turkish")
        elif self.sender().objectName()=="pushButton_66":
            self.ui.pushButton_66.setStyleSheet("background-color: yellow")
            self.ui.pushButton_67.setStyleSheet("background-color: #c6c6c6")
            write_parameter(9,"english")
        else:
            self.ui.pushButton_67.setStyleSheet("background-color: #c6c6c6")
            self.ui.pushButton_66.setStyleSheet("background-color: #c6c6c6")
            self.ui.label_14.setVisible(False)
        self.change_setting_file()

    def change_setting_file(self):
        self.ui.label_14.setVisible(True)
class Login(QDialog):
    def __init__(self,parent=None):
        super(Login, self).__init__(parent)
        self.ui=login_dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Login Page")
        self.db=db_mysql.mydb()


        self.handle_button()
    def handle_button(self):

        self.ui.pb_cancel.clicked.connect(self.pushbutton_pressed)
        self.ui.pb_cancel2.clicked.connect(self.pushbutton_pressed)
        self.ui.pb_login.clicked.connect(self.pushbutton_pressed)
        self.ui.pb_save.clicked.connect(self.pushbutton_pressed)
    def pushbutton_pressed(self):
        sender = self.sender()
        if sender.objectName()=="pb_cancel" or sender.objectName()=="pb_cancel2":
            self.close()
        elif sender.objectName()=="pb_login":
            self.login_check()
        elif  sender.objectName()=="pb_save":
            self.add_user()
        else:
            print("nothing")
    def login_check(self):
        username = self.ui.lineEdit.text()
        password =self.ui.lineEdit_2.text()
        data = self.db.check_user((username,password))

        if data!=None:
            self.window = MyWindow()
            self.window.ui.lineEdit.setText(data[1])
            self.window.ui.lineEdit_82.setText(data[3])
            self.window.user_admin_check()
            self.close()
            self.window.show()


        else:
            warning = QMessageBox.warning(self, 'Data Error', 'Please check your data', QMessageBox.Ok)
            self.ui.label_6.setText('Please check your data')
            print("User error")
    def add_user(self):
        username = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_4.text()
        re_password = self.ui.lineEdit_5.text()
        usertype = self.ui.comboBox.currentText()

        data = self.db.check_username((username,))

        if data != None:
            print("This user is already registered")
            self.ui.label_6.setText("This user is already registered")
        else:
            if password==re_password and password!="":
                self.db.insert_user((username,password,usertype))
                self.ui.label_6.setText("This user has been registered successfully")
            else:
                self.ui.label_6.setText("Passwords don't match")
                print("Passwords don't match")
class logwindow(QMainWindow):
    def __init__(self,parent=None):
        super(logwindow, self).__init__(parent)
        self.ui = log_dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Log Page")
        self.db = db_mysql.mydb()
        self.handle_button()
    def handle_button(self):
        self.ui.pushButton_8.clicked.connect(self.insert_logs)
    def stock_data_call(self):
        data = self.db.calldata_with_id_stock(int(self.ui.lineEdit_75.text()))
        if data != None:
            code = str(data[1]).split(sep="-")
            self.ui.lineEdit_77.setText(str(data[1]))
            self.ui.lineEdit_76.setText(code[1])
            self.ui.lineEdit_2.setText(str(data[2]))
            self.ui.lineEdit_42.setText(str(data[9]))
            self.ui.lineEdit_79.setText(str(data[10]))
            self.ui.lineEdit_3.setText(str(data[3]))
            self.ui.lineEdit_35.setText(str(data[8]))
            self.ui.lineEdit_36.setText(str(data[6]))
            self.ui.lineEdit_37.setText(str(data[5]))
            self.ui.lineEdit_80.setText(str(data[12]))
            self.ui.lineEdit_81.setText(str(data[13]))
            self.ui.lineEdit_38.setText(str(data[14]))
            self.ui.lineEdit_39.setText(str(data[15]))
            self.ui.lineEdit_40.setText(str(data[16]))
            picture = QPixmap(IMAGE_DIR + data[17])
            self.ui.label_10.setPixmap(picture)
            self.ui.label_10.setScaledContents(True)
            self.ui.lineEdit_9.setText(str(data[18]))
            self.ui.lineEdit_4.setText(str(data[19]))
            self.ui.lineEdit_5.setText(str(data[4]))
            self.ui.lineEdit_6.setText(str(data[20]))
            self.ui.lineEdit_8.setText(str(data[21]))
            self.ui.lineEdit_79.setText(str(data[22]))
            self.ui.lineEdit_74.setText(str(data[23]))
            return True
        else:
            return False
    def read_logs(self):
        self.ui.userID = self.ui.lineEdit_7.text()
        self.ui.yourname=self.ui.lineEdit_10.text()
        self.ui.reason = self.ui.textEdit.toPlainText()
        self.ui.qty = self.ui.lineEdit.text()
        self.ui.stockID=self.ui.lineEdit_75.text()
        if self.ui.yourname=="" or self.ui.reason =="" or self.ui.qty=="":
            warning = QMessageBox.warning(self, 'Data Error', 'Please fill the blanks', QMessageBox.Ok)
            print("fill blanks")
            return 0
        else:
            if int(self.ui.lineEdit.text())>int(self.ui.lineEdit_42.text()):
                warning = QMessageBox.warning(self, 'Quantity Error', 'Please check your qty, it can not be more then the current',
                                              QMessageBox.Ok)
                print("qty error")
            elif self.ui.lineEdit.text()==0:
                warning = QMessageBox.warning(self, 'Zero Quantity ',
                                              'Yo cannot take any item from this stock. Please change your stock',
                                              QMessageBox.Ok)
                return 0
            else:

                return 1
    def insert_logs(self):
        result = self.read_logs()

        if result == 1:
            self.db.insert_logs(( self.ui.stockID,self.ui.qty, self.ui.reason, self.ui.yourname,self.ui.userID ))

            last_current=int(self.ui.lineEdit_42.text())-int(self.ui.qty)
            value = ( last_current,self.ui.stockID)
            self.db.update_qty_stock( value)
            self.close()
            return True
        else:
            pass
class Aboutwindow(QMainWindow):
    def __init__(self,parent=None):
        super(Aboutwindow, self).__init__(parent)
        self.ui = About_window()
        self.ui.setupUi(self)
# ================ SHOW PAGES ================================================
def show_LoginPage():

    app = QApplication(sys.argv)
    translator1 = QTranslator()
    translator2 = QTranslator()
    translator3 = QTranslator()
    # =======================================
    if LANGUAGE=="turkish":

        translator1.load(LANGUAGES_DIR + 'login_tr.qm')
        app.installTranslator(translator1)
        translator2.load(LANGUAGES_DIR + 'logs_tr.qm')
        app.installTranslator(translator2)
        translator3.load(LANGUAGES_DIR + 'main_tr.qm')
        app.installTranslator(translator3)

    else:
        pass

    # =======================================

    # window = MyWindow() # bu login ile değiştirilecek
    # window.ui.lineEdit_82.setText("Admin")
    # window.user_admin_check()

    window = Login()

    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
if __name__ == "__main__":
    try:
        
        show_LoginPage()

    except Exception as err:
        print(err)