import hashlib
import pymssql

class dbQuery():
    def __init__(self,dbIP,dbusername,dbpassword,dbname):
        try:
            self.conn = pymssql.connect(dbIP, dbusername, dbpassword, dbname, autocommit = True)
        except:
            self.ifconn = False
        else:
            self.ifconn = True
            self.cursor = self.conn.cursor()
            

    def __hash(self,str):
        hash = hashlib.md5()
        hash.update(str.encode('utf-8'))
        hashkey = hash.hexdigest()
        return hashkey

    def register(self,username,password):
        hashkey = self.__hash(password)
        sql = "insert into dbo.Vip values('%s','%s')"%(username,hashkey)
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True

    def checkPassword(self,username,password):
        hashkey = self.__hash(password)
        sql = "select pswd from dbo.Vip where username='%s'"%(username)
        try:
            self.cursor.execute(sql)
        except:
            return False
        result = self.cursor.fetchone()[0]
        if (result == hashkey):
            return True
        else:
            return False

    def searchItem(searchKeyWord):
        searchResult = {}
        searchResult["item"] = searchKeyWord
        return searchResult

        
        