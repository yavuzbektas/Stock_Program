# #######################################
__name__ = "db_mysql.py"
__author__ = "Yavuz Bektaş & "
__version__ = "1.0"
__email__ = "yavuzbektas@gmail.com"
__linkedin__ = "https://www.linkedin.com/in/yavuz-bekta%C5%9F-28659642/"
__release_date__ = "2020.05.01"
__github__ = ""
# #######################################
db_type ="sqlite"
if db_type == "mysql":
    import mysql.connector

    TABLES = {}
    TABLES['users'] = ("CREATE TABLE `users` "
                       "(`id` INT NOT NULL AUTO_INCREMENT,"
                       "`username` VARCHAR(30) NOT NULL,"
                       "`password` VARCHAR(30) NOT NULL,"
                       "`usertype` VARCHAR(30) NOT NULL,"
                       "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
                       "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
    TABLES['storage_room'] = ("CREATE TABLE `storage_room` ("
                              "`id` INT NOT NULL AUTO_INCREMENT,"
                              "`name` VARCHAR(30) NOT NULL UNIQUE,"
                              "`describes` VARCHAR(50) NOT NULL,"
                              "`number` INT NULL UNIQUE,"
                              "`userID` VARCHAR(30),"
                              "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
                              "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
    TABLES['cabinet_type'] = ("CREATE TABLE cabinet_type ("
                              "`id` INT NOT NULL AUTO_INCREMENT,"
                              "`name` VARCHAR(30) NOT NULL UNIQUE,"
                              "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
    TABLES['cabinet'] = ("CREATE TABLE cabinet ("
                         "`id` INT NOT NULL AUTO_INCREMENT,"

                         "`code` VARCHAR(50) NOT NULL UNIQUE,"
                         "`typeID` INT NOT NULL,"
                         "`roomID` INT NOT NULL,"
                         "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
    TABLES['shelf'] = ("CREATE TABLE shelf ("
                       "`id` INT NOT NULL AUTO_INCREMENT,"
                       "`code` VARCHAR(30) NOT NULL UNIQUE,"
                       "`cabinetID` INT NOT NULL ,"
                       "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
    TABLES['material_type'] = ("CREATE TABLE material_type ("
                               "`id` INT NOT NULL AUTO_INCREMENT,"
                               "`name` VARCHAR(30) NOT NULL UNIQUE,"
                               "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
    TABLES['material'] = ("CREATE TABLE `material` ("
                          "`id` INT NOT NULL AUTO_INCREMENT,"
                          "`type_ID` INT NOT NULL,"
                          "`name` VARCHAR(50) NOT NULL ,"
                          "`code1` VARCHAR(50) NOT NULL UNIQUE,"
                          "`code2` VARCHAR(50) ,"
                          "`property1` TEXT NOT NULL,"
                          "`property2` TEXT,"
                          "`manufacture` VARCHAR(30) NOT NULL,"
                          "`price` REAL,"
                          "`price_unitID` VARCHAR(10),"
                          "`image_path` TEXT,"
                          "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
                          "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
    TABLES['unit_type'] = ("CREATE TABLE unit_type ("
                           "`id` INT NOT NULL AUTO_INCREMENT,"
                           "`name` VARCHAR(30) NOT NULL UNIQUE,"
                           "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
    TABLES['stock'] = ("CREATE TABLE `stock` ("
                       "`id` INT NOT NULL AUTO_INCREMENT,"
                       "`code` VARCHAR(60) NOT NULL UNIQUE,"
                       "`shelf_ID` INT NOT NULL,"
                       "`material_ID` INT NOT NULL,"
                       "`quantity` INT,"
                       "`unitID` VARCHAR(15),"
                       "`userID` TEXT NOT NULL,"
                       "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
                       "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
    TABLES['logs'] = ("CREATE TABLE `logs` ("
                               "`id` INT NOT NULL AUTO_INCREMENT,"
                               "`stock_ID` INT NOT NULL,"
                               "`used_quantity` INT,"
                               "`usefor_reason` TEXT,"
                               "`yourname` TEXT,"
                               "`userID` TEXT NOT NULL,"
                               "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
                               "PRIMARY KEY (`id`), UNIQUE KEY `id` (`id`))")
else :
    import sqlite3

    TABLES = {}
    TABLES['users'] = ("CREATE TABLE `users` "
                       "(`id` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,"
                       "`username` VARCHAR(30) NOT NULL,"
                       "`password` VARCHAR(30) NOT NULL,"
                       "`usertype` VARCHAR(30) NOT NULL,"
                       "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP )")

    TABLES['storage_room'] = ("CREATE TABLE `storage_room` ("
                              "`id` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,"
                              "`name` VARCHAR(30) NOT NULL UNIQUE,"
                              "`describes` VARCHAR(50) NOT NULL,"
                              "`number` INT NULL UNIQUE,"
                              "`userID` VARCHAR(30),"
                              "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP )")
    TABLES['cabinet_type'] = ("CREATE TABLE cabinet_type ("
                              "`id` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,"
                              "`name` VARCHAR(30) NOT NULL UNIQUE )")
    TABLES['cabinet'] = ("CREATE TABLE cabinet ("
                         "`id` INTEGER NOT NULL UNIQUE PRIMARY KEY  AUTOINCREMENT,"

                         "`code` VARCHAR(50) NOT NULL UNIQUE,"
                         "`typeID` INT NOT NULL,"
                         "`roomID` INT NOT NULL)")
    TABLES['shelf'] = ("CREATE TABLE shelf ("
                       "`id` INTEGER NOT NULL  UNIQUE PRIMARY KEY  AUTOINCREMENT,"
                       "`code` VARCHAR(30) NOT NULL UNIQUE,"
                       "`cabinetID` INT NOT NULL )")
    TABLES['material_type'] = ("CREATE TABLE material_type ("
                               "`id` INTEGER NOT NULL UNIQUE  PRIMARY KEY AUTOINCREMENT,"
                               "`name` VARCHAR(30) NOT NULL UNIQUE)")
    TABLES['material'] = ("CREATE TABLE `material` ("
                          "`id` INTEGER NOT NULL  UNIQUE PRIMARY KEY AUTOINCREMENT,"
                          "`type_ID` INT NOT NULL,"
                          "`name` VARCHAR(50) NOT NULL ,"
                          "`code1` VARCHAR(50) NOT NULL UNIQUE,"
                          "`code2` VARCHAR(30) ,"
                          "`property1` TEXT NOT NULL,"
                          "`property2` TEXT,"
                          "`manufacture` VARCHAR(30) NOT NULL,"
                          "`price` REAL,"
                          "`price_unitID` VARCHAR(10),"
                          "`image_path` TEXT,"
                          "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP)")
    TABLES['unit_type'] = ("CREATE TABLE unit_type ("
                           "`id` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,"
                           "`name` VARCHAR(30) NOT NULL UNIQUE)")
    TABLES['stock'] = ("CREATE TABLE `stock` ("
                       "`id` INTEGER NOT NULL UNIQUE PRIMARY KEY  AUTOINCREMENT,"
                       "`code` VARCHAR(60) NOT NULL UNIQUE,"
                       "`shelf_ID` INT NOT NULL,"
                       "`material_ID` INT NOT NULL,"
                       "`quantity` INT,"
                       "`unitID` VARCHAR(15),"
                       "`userID` TEXT NOT NULL,"
                       "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP)")
    TABLES['logs'] = ("CREATE TABLE `logs` ("
                               "`id` INTEGER NOT NULL UNIQUE PRIMARY KEY  AUTOINCREMENT,"
                               "`stock_ID` INT NOT NULL,"
                               "`used_quantity` INT,"
                               "`reason` TEXT,"
                               "`yourname` TEXT,"
                               "`userID` TEXT NOT NULL,"
                               "`record_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP)")
# "O:\TEKNIK_DERSLER\EETA-EOTA\ORTAK\STOK Programı\stockDB"
class mydb():
    def __init__(self,host="localhost",username="root",password="1234567890",DB_NAME="O:\TEKNIK_DERSLER\EETA-EOTA\ORTAK\STOK Programı\stockDB"):
        self.host=host
        self.username=username
        self.password=password
        self.db_name=DB_NAME
        self.connect_db()
        self.create_tables()
    def connect_db(self):
        try:
            if db_type=="mysql":
                self.db = mysql.connector.connect(
                    host=self.host,
                    user=self.username,
                    passwd=self.password
            )
            else:
                self.db = sqlite3.connect(database=self.db_name)

        except Exception as error:
            print(error)

        self.cursor = self.db.cursor()
        if db_type=="mysql":
            try:
                self.cursor.execute("USE {}".format(self.db_name))
            except Exception as err:
                print("Database {} does not exists.".format(self.db_name))
                print(err)
                exit(1)
    def create_db(self,cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT COLLATE 'utf8_turkish_ci'".format(self.db_name))
            self.create_tables()
        except Exception as err:
            print("Failed creating database: {}".format(err))
            exit(1)
    def create_tables(self):

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:

                self.cursor.execute(table_description)
                print("Creating table {}: ".format(table_name), end='')
            except Exception as err:
                    print("Error Code  : ", err)

        self.cursor.close()
        self.db.close()
    def search_data(self,query,values):
        self.connect_db()
        self.cursor.execute(query,(values))
        data = self.cursor.fetchall()
        self.cursor.close()
        self.db.close()
        return data
    def fetchall(self,query):
        self.connect_db()
        self.cursor.execute(query)
        try:
            data = self.cursor.fetchall()
        except Exception as err:
            print(err)
        finally:
            self.cursor.close()
            self.db.close()
        if data == None:
            return None
        else:
            return data
    def fetchone(self,query):
        self.connect_db()
        self.cursor.execute(query)
        try:
            data = self.cursor.fetchone()

        except Exception as err:
            print(err)
        finally:
            self.cursor.close()
            self.db.close()
        if data == None:
            return None
        else:
            return data
    def commit_db(self,query):
        self.connect_db()
        try:
            self.cursor.execute(query)
            self.db.commit()
        except Exception as err:
            print(err)
            return err
        finally:
            self.cursor.close()
            self.db.close()
    # =========== USER ==========================
    def check_user(self,values):
        self.connect_db()
        query = "SELECT id,username,password,usertype FROM users WHERE username='%s' AND password='%s'" % (values)
        data = self.fetchone(query)
        return data
    def check_username(self,values):
        query = "SELECT id,username,password,usertype FROM users WHERE username='%s'" % values
        data = self.fetchone(query)
        return data
    def insert_user(self,values):
        query = "INSERT INTO users (username,password,usertype ) VALUES ( '%s','%s','%s')" % values
        data = self.commit_db(query)
        return data
    def calldata_with_id_user(self,id):
        query =  "SELECT id,username,password,usertype,record_date FROM users WHERE users.id = '%s'" % (id,)
        data = self.fetchone(query)
        return data
    def delete_user(self,value):
        query = "DELETE FROM users WHERE id='%s'" % (value,)
        data = self.commit_db(query)
        return data
    def update_user(self,value):
        query = "UPDATE  users SET " \
                "username='%s',password='%s',usertype='%s' " \
                "WHERE id='%s'" % (value)
        data = self.commit_db(query)
        return data
    def showall_user(self):
        query = "SELECT id,username,usertype,record_date,password  FROM users "
        data = self.fetchall(query)
        return data
    def showfilter_user(self,filter_value):
        query = "SELECT id,username,usertype,record_date,password  FROM users WHERE username LIKE '{}%'".format(filter_value)
        data = self.fetchall(query)
        return data
    # =========== room ==========================
    def check_room(self,values):
        query = "SELECT * FROM storage_room WHERE name='%s' or number='%s'" % (values)
        data = self.fetchall(query)
        return data
    def insert_room(self,values):
        query = "INSERT INTO storage_room (name,describes,number,userID) VALUES ( '%s','%s','%s','%s')" % (values)
        data = self.commit_db(query)
        return data
    def show_all_room(self):
        query = "SELECT * FROM storage_room "
        data = self.fetchall(query)
        return data
    def delete_room(self,value):
        query = "DELETE FROM storage_room WHERE id='%s'" % (value,)
        data = self.commit_db(query)
        return data
    def calldata_with_id_room(self,id):
        query = "SELECT * FROM storage_room WHERE id='%s'" % (id,)
        data = self.fetchone(query)
        return data
    def update_room(self,values):
        query = "UPDATE  storage_room SET name='%s',describes='%s',number='%s',userID='%s' WHERE id='%s'" % (values)
        data = self.commit_db(query)
        return data
    def showfilter_room(self,filter_value,index=0):
        if index==0:
            criteria="storage_room.name"
        elif index==1:
            criteria = "storage_room.number"
        elif index==2:
            criteria = "storage_room.userID"
        elif index==3:
            criteria = "storage_room.ID"
        else:
            criteria = ""

        query = "SELECT * FROM storage_room WHERE {} LIKE '{}%'".format(criteria,filter_value)
        data = self.fetchall(query)
        return data

    # =========== cabinet type ==========================
    def check_cabinet_type(self,value):

        query = "SELECT * FROM cabinet_type WHERE name='%s'" %(value,)
        data=self.fetchone(query)
        return data
    def insert_cabinet_type(self,value):
        query = "INSERT INTO cabinet_type (name) VALUES ('%s')" %(value,)
        data = self.commit_db(query)
        return data
    def delete_cabinet_type(self,value):
        query = "DELETE FROM cabinet_type WHERE id='%s'" % (value,)
        data = self.commit_db(query)
        return data
    def update_cabinet_type(self,value):
        query = "UPDATE  cabinet_type SET name='%s' WHERE id='%s'" % (value)
        data = self.commit_db(query)
        return data
    def showall_cabinet_type(self):
        query = "SELECT * FROM cabinet_type "
        data = self.fetchall(query)
        return data
    def calldata_with_id_cabinet_type(self,id):
        query = "SELECT * FROM cabinet_type WHERE id='%s'" % (id,)
        data = self.fetchone(query)
        return data
# =========== cabinet  ==========================
    def check_cabinet(self,value):
        query = "SELECT * FROM cabinet WHERE code='%s'" %(value,)
        data = self.fetchone(query)
        return data
    def insert_cabinet(self,value):
        query = "INSERT INTO cabinet (code,typeID,roomID) VALUES ('%s','%s','%s')" % (value)
        data = self.commit_db(query)
        return data
    def delete_cabinet(self,value):
        query = "DELETE FROM cabinet WHERE id='%s'" % (value,)
        data = self.commit_db(query)
        return data
    def update_cabinet(self,value):
        query = "UPDATE  cabinet SET code='%s',typeID='%s',roomID='%s' WHERE id='%s'" % (value)
        data = self.commit_db(query)
        return data
    def showall_cabinet(self):
        query = "SELECT cabinet.ID,cabinet.code,cabinet_type.name,storage_room.name,cabinet.ID,cabinet_type.ID,storage_room.ID " \
                "FROM cabinet " \
                "INNER JOIN cabinet_type " \
                "ON cabinet.typeID=cabinet_type.ID  " \
                "INNER JOIN storage_room " \
                "ON cabinet.roomID=storage_room.ID"
        data = self.fetchall(query)
        return data
    def calldata_with_id_cabinet(self,id):
        query = "SELECT cabinet.ID,cabinet.code,cabinet_type.name,storage_room.name,cabinet.typeID,storage_room.ID " \
                "FROM cabinet " \
                "INNER JOIN cabinet_type " \
                "ON cabinet.typeID=cabinet_type.ID  " \
                "INNER JOIN storage_room " \
                "ON cabinet.roomID=storage_room.ID " \
                "WHERE cabinet.ID = '%s'" % (id,)
        data = self.fetchone(query)
        return data
    def showfilter_cabinet(self,room,filter_value="",index=0):
        if index==0:
            criteria="cabinet_type.name"
        elif index==1:
            criteria = "cabinet.code"
        elif index==2:
            criteria = "storage_room.name"
        elif index==3:
            criteria = "cabinet.ID"
        else:
            criteria = ""
        if room=="":

            query = "SELECT cabinet.ID,cabinet.code,cabinet_type.name,storage_room.name,cabinet.typeID,storage_room.ID " \
                    "FROM cabinet " \
                    "INNER JOIN cabinet_type " \
                    "ON cabinet.typeID=cabinet_type.ID  " \
                    "INNER JOIN storage_room " \
                    "ON cabinet.roomID=storage_room.ID " \
                    "WHERE {} LIKE '{}%' ".format(criteria,filter_value)
        else:
            query = "SELECT cabinet.ID,cabinet.code,cabinet_type.name,storage_room.name,cabinet.typeID,storage_room.ID " \
                    "FROM cabinet " \
                    "INNER JOIN cabinet_type " \
                    "ON cabinet.typeID=cabinet_type.ID  " \
                    "INNER JOIN storage_room " \
                    "ON cabinet.roomID=storage_room.ID " \
                    "WHERE {} LIKE '{}%' AND storage_room.name='{}' ".format(criteria, filter_value, room)
        data = self.fetchall(query)
        return data
# =========== shelf  ==========================
    def check_shelf(self,value):
        query = "SELECT * FROM shelf WHERE code='%s'" %  (value,)
        data = self.fetchone(query)
        return data
    def insert_shelf(self,value):
        query = "INSERT INTO shelf (code,cabinetID) VALUES ('%s','%s')" %(value)
        data = self.commit_db(query)
        return data
    def delete_shelf(self,value):
        query = "DELETE FROM shelf WHERE id='%s'" % (value,)
        data = self.commit_db(query)
        return data
    def update_shelf(self,value):
        query = "UPDATE  shelf SET code='%s',cabinetID='%s' WHERE id='%s'" %  (value)
        data = self.commit_db(query)
        return data
    def showall_shelf(self):
        query = "SELECT shelf.id,shelf.code,cabinet.code,storage_room.name,cabinet.id,storage_room.id " \
                "FROM shelf " \
                "INNER JOIN cabinet " \
                "ON cabinet.id=shelf.cabinetID  " \
                "INNER JOIN storage_room " \
                "ON cabinet.roomID=storage_room.id"
        data = self.fetchall(query)
        return data
    def calldata_with_id_shelf(self,id):
        query = "SELECT shelf.id,shelf.code,cabinet.code,storage_room.name,cabinet.id,storage_room.id " \
                "FROM shelf " \
                "INNER JOIN cabinet " \
                "ON cabinet.id=shelf.cabinetID  " \
                "INNER JOIN storage_room " \
                "ON cabinet.roomID=storage_room.id "\
                "WHERE shelf.id = '%s'" %(id,)

        data = self.fetchone(query)
        return data
    def showfilter_shelf(self,room,cabinet,filter_value="",index=0):
        if index==0:
            criteria="shelf.code"
        elif index==1:
            criteria="cabinet.code"
        elif index == 2:
            criteria = "storage_room.name"
        elif index==3:
            criteria="shelf.id"
        else:
            criteria=""
        query = "SELECT shelf.id,shelf.code,cabinet.code,storage_room.name,cabinet.id,storage_room.id " \
                "FROM shelf " \
                "INNER JOIN cabinet " \
                "ON cabinet.id=shelf.cabinetID  " \
                "INNER JOIN storage_room " \
                "ON cabinet.roomID=storage_room.id " \
                "WHERE {} LIKE '{}%' AND cabinet.code='{}' AND storage_room.name='{}'".format(criteria,filter_value,cabinet,room)
        data = self.fetchall(query)
        return data
# =========== cabinet type ==========================
    def check_material_type(self,value):
        query = "SELECT * FROM material_type WHERE name='%s'" % (value)
        data = self.fetchone(query)
        return data
    def insert_material_type(self,value):
        query = "INSERT INTO material_type (name) VALUES ('%s')" %(value,)
        data = self.commit_db(query)
        return data
    def delete_material_type(self,value):
        query = "DELETE FROM material_type WHERE id='%s'" % (value,)
        data = self.commit_db(query)
        return data
    def update_material_type(self,value):
        query = "UPDATE  material_type SET name='%s' WHERE id='%s'" %(value)
        data = self.commit_db(query)
        return data
    def showall_material_type(self):
        query = "SELECT * FROM material_type "
        data = self.fetchall(query)
        return data
    def calldata_with_id_material_type(self,id):
        query = "SELECT * FROM material_type WHERE id=%s" %  (id,)
        data = self.fetchone(query)
        return data
    def showfilter_material_type(self,filter_value):
        query = "SELECT * FROM material_type WHERE name LIKE '{}%'".format(filter_value)
        data = self.fetchall(query)
        return data
# =========== Material  ==========================
    def check_material(self,value):
        query = "SELECT * FROM material WHERE name='%s'" % (value,)
        data = self.fetchone(query)
        return data
    def insert_material(self,value):
        query = "INSERT INTO material " \
                "(type_ID,name,code1,code2,property1,property2,manufacture,price,price_unitID,image_path) " \
                "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % value
        data = self.commit_db(query)
        return data
    def delete_material(self,value):
        query = "DELETE FROM material WHERE id=%s" % (value,)
        data = self.commit_db(query)
        return data
    def update_material(self,value):
        query = "UPDATE  material SET " \
                "type_ID='%s',name='%s',code1='%s',code2='%s',property1='%s',property2='%s',manufacture='%s'," \
                "price='%s',price_unitID='%s',image_path='%s' " \
                "WHERE id='%s'" % value
        data = self.commit_db(query)
        return data
    def showall_material(self):
        query = "SELECT material.id,material_type.name,material.name,material.code1,material.code2," \
                "material.property1,material.property2,material.manufacture,material.price," \
                "material.price_unitID,material.image_path " \
                "FROM material " \
                "INNER JOIN material_type " \
                "ON material_type.id=material.type_ID "
        data = self.fetchall(query)
        return data
    def calldata_with_id_material(self,id):
        query = "SELECT material.id,material.type_ID,material_type.name,material.name,material.code1,material.code2," \
                "material.property1,material.property2,material.manufacture,material.price,material.price_unitID,material.image_path " \
                "FROM material " \
                "INNER JOIN material_type " \
                "ON material_type.id=material.type_ID " \
                "WHERE material.id = %s" % (id,)
        data = self.fetchone(query)
        return data
    def showfilter_material(self,index,filter_value):
        if index==0:
            criteria="material_type.name"
        elif index==1:
            criteria="material.name"
        elif index==2:
            criteria="material.code1"
        elif index==3:
            criteria="material.code2"
        elif index==4:
            criteria="material.property1"
        elif index==5:
            criteria="material.property2"
        elif index==6:
            criteria="material.manufacture"
        else:
            criteria = ""

        query = "SELECT material.id,material_type.name,material.name,material.code1,material.code2," \
                "material.property1,material.property2,material.manufacture,material.price," \
                "material.price_unitID,material.image_path " \
                "FROM material " \
                "INNER JOIN material_type " \
                "ON material_type.id=material.type_ID" \
                " WHERE {} LIKE '{}%'".format(criteria,filter_value)
        data = self.fetchall(query)
        return data

# =========== Stock  ==========================
    def check_stock(self,value):
        query = "SELECT * FROM stock WHERE code='%s'" % (value,)
        data = self.fetchone(query)
        return data
    def insert_stock(self,value):
        query = "INSERT INTO stock " \
                "(code,shelf_ID,material_ID,quantity,unitID,userID) " \
                "VALUES ('%s','%s','%s','%s','%s','%s')" % (value)
        data = self.commit_db(query)
        return data
    def delete_stock(self,value):
        query = "DELETE FROM stock WHERE id='%s'" % (value,)
        data = self.commit_db(query)
        return data
    def update_stock(self,value):
        query = "UPDATE  stock SET " \
                "code='%s',shelf_ID='%s',material_ID='%s',quantity='%s',unitID='%s',userID='%s' " \
                "WHERE id='%s'" % (value)
        data = self.commit_db(query)
        return data
    def update_qty_stock(self,value):
        query = "UPDATE  stock SET " \
                "quantity='%s'" \
                "WHERE id='%s'" % (value)
        data = self.commit_db(query)
        return data
    def showall_stock(self):
        query = "SELECT stock.id,stock.code,material.name,material.code1,material.property1," \
                "shelf.code,cabinet.code,cabinet_type.name,storage_room.name,stock.quantity,stock.unitID,stock.userID," \
                "stock.record_date, stock.material_ID,cabinet.roomID ,shelf.cabinetID ,stock.shelf_ID "\
                "FROM stock " \
                "INNER JOIN material " \
                "ON material.id=stock.material_ID " \
                "INNER JOIN shelf " \
                "ON shelf.id=stock.shelf_ID " \
                "INNER JOIN cabinet " \
                "ON cabinet.id=shelf.cabinetID " \
                "INNER JOIN cabinet_type " \
                "ON cabinet_type.id=cabinet.typeID " \
                "INNER JOIN storage_room " \
                "ON storage_room.id=cabinet.roomID "
        data = self.fetchall(query)
        return data
    def calldata_with_id_stock(self,id):
        query =  "SELECT stock.id,stock.code,material.name,material.code1,material.property1," \
                "shelf.code,cabinet.code,cabinet_type.name,storage_room.name,stock.quantity,stock.unitID,stock.userID," \
                "stock.record_date, stock.material_ID,cabinet.roomID ,shelf.cabinetID ,stock.shelf_ID,material.image_path," \
                 "material.manufacture, material.code2,material.property2,material.price,material.price_unitID,material_type.name "\
                "FROM stock " \
                "INNER JOIN material " \
                "ON material.id=stock.material_ID " \
                 "INNER JOIN material_type " \
                 "ON material_type.id=material.type_ID " \
                 "INNER JOIN shelf " \
                "ON shelf.id=stock.shelf_ID " \
                "INNER JOIN cabinet " \
                "ON cabinet.id=shelf.cabinetID " \
                "INNER JOIN cabinet_type " \
                "ON cabinet_type.id=cabinet.typeID " \
                "INNER JOIN storage_room " \
                "ON storage_room.id=cabinet.roomID "\
                "WHERE stock.id = '%s'" % (id,)
        data = self.fetchone(query)
        return data
    def showfilter_stock(self,index,filter_value):

        if index==0:
            criteria="stock.code"
        elif index==1:
            criteria="material.name"
        elif index==2:
            criteria="material.code1"
        elif index==3:
            criteria="storage_room.name"
        elif index==4:
            criteria="cabinet.code"
        elif index==5:
            criteria="shelf.code"
        elif index==6:
            criteria="stock.userID"
        elif index==7:
            criteria="stock.id"
        else:
            criteria = ""

        query =  "SELECT stock.id,stock.code,material.name,material.code1,material.property1," \
                "shelf.code,cabinet.code,cabinet_type.name,storage_room.name,stock.quantity,stock.unitID,stock.userID," \
                "stock.record_date, stock.material_ID,cabinet.roomID ,shelf.cabinetID ,stock.shelf_ID "\
                "FROM stock " \
                "INNER JOIN material " \
                "ON material.id=stock.material_ID " \
                "INNER JOIN shelf " \
                "ON shelf.id=stock.shelf_ID " \
                "INNER JOIN cabinet " \
                "ON cabinet.id=shelf.cabinetID " \
                "INNER JOIN cabinet_type " \
                "ON cabinet_type.id=cabinet.typeID " \
                "INNER JOIN storage_room " \
                "ON storage_room.id=cabinet.roomID "\
                " WHERE {} LIKE '{}%'".format(criteria,filter_value)
        data = self.fetchall(query)
        return data

# =========== logs  ==========================
    def insert_logs(self,value):
        query = "INSERT INTO logs " \
                "(stock_id,used_quantity,reason,yourname,userID) " \
                "VALUES ('%s','%s','%s','%s','%s')" % (value)
        data = self.commit_db(query)
        return data
    def delete_logs(self,value):
        query = "DELETE FROM logs WHERE id='%s'" % (value,)
        data = self.commit_db(query)
        return data
    def showall_logs(self):
        query = "SELECT stock.id,stock.code,material.name,material.code1,material.property1," \
                "shelf.code,cabinet.code,cabinet_type.name,storage_room.name,stock.quantity,stock.unitID,stock.userID," \
                "stock.record_date, stock.material_ID,cabinet.roomID ,shelf.cabinetID ,stock.shelf_ID,logs.used_quantity,logs.reason,logs.yourname "\
                "FROM stock " \
                "INNER JOIN material " \
                "ON material.id=stock.material_ID " \
                "INNER JOIN shelf " \
                "ON shelf.id=stock.shelf_ID " \
                "INNER JOIN cabinet " \
                "ON cabinet.id=shelf.cabinetID " \
                "INNER JOIN cabinet_type " \
                "ON cabinet_type.id=cabinet.typeID " \
                "INNER JOIN storage_room " \
                "ON storage_room.id=cabinet.roomID " \
                "INNER JOIN logs " \
                "ON stock.id=logs.stock_id "
        data = self.fetchall(query)
        return data
    def showfilter_logs(self,index,filter_value):

        if index==0:
            criteria="stock.code"
        elif index==1:
            criteria="logs.yourname"
        elif index==2:
            criteria="logs.reason"
        elif index==3:
            criteria="logs.record_date"
        elif index==4:
            criteria="logs.id"
        elif index==5:
            criteria="material.name"
        elif index==6:
            criteria="material.code1"
        elif index==7:
            criteria="storage_room.name"
        elif index==8:
            criteria="cabinet.code"
        elif index==9:
            criteria="shelf.code"
        elif index==10:
            criteria="logs.userID"

        else:
            criteria = ""

        query = "SELECT logs.id,stock.code,logs.reason,logs.yourname,stock.quantity,logs.used_quantity,material.name,material.code1,material.property1," \
                "shelf.code,cabinet.code,cabinet_type.name,storage_room.name,stock.unitID,logs.userID," \
                "logs.record_date, stock.material_ID,cabinet.roomID ,shelf.cabinetID ,stock.shelf_ID "\
                "FROM stock " \
                "INNER JOIN material " \
                "ON material.id=stock.material_ID " \
                "INNER JOIN shelf " \
                "ON shelf.id=stock.shelf_ID " \
                "INNER JOIN cabinet " \
                "ON cabinet.id=shelf.cabinetID " \
                "INNER JOIN cabinet_type " \
                "ON cabinet_type.id=cabinet.typeID " \
                "INNER JOIN storage_room " \
                "ON storage_room.id=cabinet.roomID " \
                "INNER JOIN logs " \
                "ON stock.id=logs.stock_id "\
                " WHERE {} LIKE '{}%'".format(criteria,filter_value)
        data = self.fetchall(query)
        return data
    def show_betweendate_logs(self,start,finish):


        query = "SELECT logs.id,stock.code,logs.reason,logs.yourname,stock.quantity,logs.used_quantity,material.name,material.code1,material.property1," \
                "shelf.code,cabinet.code,cabinet_type.name,storage_room.name,stock.unitID,logs.userID," \
                "logs.record_date, stock.material_ID,cabinet.roomID ,shelf.cabinetID ,stock.shelf_ID "\
                "FROM stock " \
                "INNER JOIN material " \
                "ON material.id=stock.material_ID " \
                "INNER JOIN shelf " \
                "ON shelf.id=stock.shelf_ID " \
                "INNER JOIN cabinet " \
                "ON cabinet.id=shelf.cabinetID " \
                "INNER JOIN cabinet_type " \
                "ON cabinet_type.id=cabinet.typeID " \
                "INNER JOIN storage_room " \
                "ON storage_room.id=cabinet.roomID " \
                "INNER JOIN logs " \
                "ON stock.id=logs.stock_id "\
                " WHERE logs.record_date BETWEEN '{}' AND '{}'".format(start,finish)
        data = self.fetchall(query)
        return data