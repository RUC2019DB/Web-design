# coding=utf-8
import hashlib
import pymssql

from Form import searchForm

class dbQuery():
    def __init__(self,dbIP,dbusername,dbpassword,dbname):
        self.conn = pymssql.connect(dbIP, dbusername, dbpassword, dbname, autocommit = True)
        try:
            self.conn = pymssql.connect(dbIP, dbusername, dbpassword, dbname, autocommit = True)#自动commit sql命令
        except:
            self.ifconn = False
        else:
            self.ifconn = True
            self.cursor = self.conn.cursor(as_dict=True)#查询结果设置为字典形式
            

    def __hash(self,str):#哈希函数，用于密码加密
        hash = hashlib.md5()
        hash.update(str.encode('utf-8'))
        hashkey = hash.hexdigest()
        return hashkey

    def __toZH(self,str):#解决数据库查询时中文显示乱码的问题
        return str.encode('latin-1').decode('gbk')

    def register(self,userInfo):#注册
        hashkey = self.__hash(userInfo["password1"])
        sql = "select count(*) vipnum from ruc.vip"
        self.cursor.execute(sql)
        vipnum = self.cursor.fetchone()["vipnum"]
        sql = ("insert into ruc.vip values('%s',%d,'%s','%s','%s','%s','%s','%s')"
                %(userInfo["username"],vipnum+1,hashkey,
                  userInfo["birthdate"],userInfo["sex"],
                  userInfo["province"],userInfo["address"],
                  userInfo["phone"]))
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True

    def checkPassword(self,username,password):#密码验证
        hashkey = self.__hash(password)
        sql = "select vipkey from ruc.vip where vipname='%s'"%(username)
        try:
            self.cursor.execute(sql)
        except:
            return False
        result = self.cursor.fetchone()["vipkey"]
        if (result == hashkey):
            return True
        else:
            return False

    def randomItems(self,num):
        sql = "select top %d * from ruc.goods order by newid()"%(num)
        try:
            self.cursor.execute(sql)
        except:
            return False
        result = self.cursor.fetchall()
        for i in range(len(result)):
            result[i]["gname"] = self.__toZH(result[i]["gname"])
            result[i]["gsort"] = self.__toZH(result[i]["gsort"])
        return result

    def searchItems(self,searchKeyWord):#搜索商品
        sql = "select * from ruc.goods where gname like \'" + '%' + "%s"%(searchKeyWord) + "%\'"
        try:
            self.cursor.execute(sql)
        except:
            return False
        searchResult = self.cursor.fetchall()
        for i in range(len(searchResult)):
            searchResult[i]["gname"] = self.__toZH(searchResult[i]["gname"])
            searchResult[i]["gsort"] = self.__toZH(searchResult[i]["gsort"])
        return searchResult


    def getItem(self,gno):#获取编号为gno的商品信息
        sql = "select * from ruc.goods where gno=%d"%(gno)
        try:
            self.cursor.execute(sql)
        except:
            return False
        itemInfo = self.cursor.fetchone()
        itemInfo["gname"] = self.__toZH(itemInfo["gname"])
        itemInfo["gsort"] = self.__toZH(itemInfo["gsort"])
        return itemInfo


        
        