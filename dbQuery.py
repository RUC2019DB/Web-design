# coding=utf-8
import hashlib
import pymssql
from werkzeug.utils import secure_filename
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

    def vipRegister(self,userInfo):#注册vip
        hashkey = self.__hash(userInfo["password1"])
        sql = "select count(*) vipnum from ruc.vip"
        self.cursor.execute(sql)
        vipnum = self.cursor.fetchone()["vipnum"]
        sql = ("insert into ruc.vip values('%s',%d,'%s','%s','%s','%s','%s','%s')"
                %(userInfo["username"], vipnum+1, hashkey,
                  userInfo["birthdate"], userInfo["sex"],
                  userInfo["province"], userInfo["address"],
                  userInfo["phone"]))
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True

    
    def storeRegister(self,storeInfo):#注册商店
        hashkey = self.__hash(storeInfo["password1"])
        sql = "select count(*) storenum from ruc.store"
        self.cursor.execute(sql)
        storenum = self.cursor.fetchone()["storenum"]
        sql = ("insert into ruc.store(stname,stno,stkey,staddress) values('%s',%d,'%s','%s')"
                %(storeInfo["storename"], storenum+1, hashkey, storeInfo["address"]))
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True


    def checkPassword(self,usertype,username,password):#密码验证
        hashkey = self.__hash(password)
        if usertype=='VIP':
            sql = "select vipkey from ruc.vip where vipname='%s'"%(username)
            key = "vipkey"
        else:
            sql = "select stkey from ruc.store where stname='%s'"%(username)
            key = "stkey"
        try:
            self.cursor.execute(sql)
        except:
            return False
        result = self.cursor.fetchone()[key]
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
            result[i]["gpic"] = self.__toZH(result[i]["gpic"])
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
            searchResult[i]["gpic"] = self.__toZH(searchResult[i]["gpic"])
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
        itemInfo["gpic"] = self.__toZH(itemInfo["gpic"])
        return itemInfo


    def postItem(self,username,item,itempic):
        sql = "select count(*) itemnum from ruc.goods"
        self.cursor.execute(sql)
        itemnum = self.cursor.fetchone()["itemnum"]
        sql = "select stno from ruc.store where stname='%s'"%(username)
        self.cursor.execute(sql)
        stno = self.cursor.fetchone()["stno"]
        sql = ("insert into ruc.goods values('%s',%d,'%s',%f,%d,%d,'%s')"
               %(item['itemname'], itemnum+1, item['itemsort'],
                 item['itemprice'], stno, item['itemsale'],
                 itempic.filename))
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True
            


        
