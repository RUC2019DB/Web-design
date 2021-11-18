import hashlib
import pymssql

class dbQuery():
    def __init__(self,dbIP,dbusername,dbpassword,dbname):
        self.db = pymssql.connect(dbIP, dbusername, dbpassword, dbname)
        if self.db:
            print("数据库连接成功")
            self.cursor = self.db.cursor()
        else:
            print("数据库连接失败")
    
    def checkPassword(self,username,password):
        hash = hashlib.md5()
        hash.update(password.encode('utf-8'))
        hashkey = hash.hexdigest()
        sql = "select pswd from dbo.Vip where username='%s'"%(username)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()[0]
        if (result == hashkey):
            return True
        else:
            return False

        
        