# coding=utf-8
import hashlib
import pymssql
from werkzeug.utils import secure_filename
from Form import searchForm
import time

class dbQuery():
    def __init__(self,dbIP,dbusername,dbpassword,dbname):
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

    def __getvipno(self,username):#给定用户名，查询用户编号
        vipno = 0
        sql = "select vipno from ruc.vip where vipname='%s'"%(username)
        try:
            self.cursor.execute(sql)
        except:
            vipno = -1
        else:
            vipno = self.cursor.fetchone()["vipno"]
        return vipno

    def __getstno(self,username):#给定店铺名，查询用户编号
        stno = 0
        sql = "select stno from ruc.store where stname='%s'"%(username)
        try:
            self.cursor.execute(sql)
        except:
            stno = -1
        else:
            stno = self.cursor.fetchone()["stno"]
        return stno


    def vipRegister(self,userInfo):#注册vip
        hashkey = self.__hash(userInfo["password1"])
        sql = "select count(*) vipnum from ruc.vip"
        self.cursor.execute(sql)
        vipnum = self.cursor.fetchone()["vipnum"]
        sql = ("insert into ruc.vip values(%d,'%s','%s','%s','%s','%s','%s','%s',%d)"
                %(vipnum+1, userInfo["username"], hashkey,
                  userInfo["birthdate"], userInfo["sex"],
                  userInfo["province"], userInfo["address"],
                  userInfo["phone"], 0))
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

    
    def vipInfo(self,username):
        sql = "select vipname,vipdate,vipsex,province,address,vipphone,vipmoney from ruc.vip where vipname='%s'"%(username)
        self.cursor.execute(sql)
        vipInfo = self.cursor.fetchone()
        vipInfo["vipsex"] = self.__toZH(vipInfo["vipsex"])
        vipInfo["province"] = self.__toZH(vipInfo["province"])
        vipInfo["address"] = self.__toZH(vipInfo["address"])
        return vipInfo


    def storeInfo(self,username):
        stno = self.__getstno(username)
        sql = "select stname,staddress from ruc.store where stname='%s'"%(username)
        self.cursor.execute(sql)
        storeInfo = self.cursor.fetchone()
        sql = ("select sum(o.gprice*o.gquantity) profits from ruc.orders o,ruc.goods g where o.gno=g.gno and stno=%d and gstate='已完成'"
                %(stno))
        self.cursor.execute(sql)
        profits = self.cursor.fetchone()["profits"]
        if profits==None:
            storeInfo["profits"] = 0
        else:
            storeInfo["profits"] = profits
        storeInfo["stname"] = self.__toZH(storeInfo["stname"])
        storeInfo["staddress"] = self.__toZH(storeInfo["staddress"])
        return storeInfo

    
    def storeViewItems(self,username):
        stno = self.__getstno(username)
        sql = "select * from ruc.goods where stno=%d"%(stno)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for i in range(len(result)):
            result[i]["gclass"] = self.__toZH(result[i]["gclass"])
            result[i]["gpic"] = self.__toZH(result[i]["gpic"])
            result[i]["gname"] = self.__toZH(result[i]["gname"])
        return result

    
    def updateItem(self,gno,item,itempic):
        item["gpic"] = itempic.filename
        try:
            for k,v in item.items():
                if len(v)>0:
                    if (k=='gprice')|(k=='gstorage'):
                        sql = "update ruc.goods set %s=%s where gno=%d"%(k,v,gno)
                    else:
                        sql = "update ruc.goods set %s='%s' where gno=%d"%(k,v,gno)
                    self.cursor.execute(sql)
        except:
            return False
        else:
            return True


    def updateInfo(self,newInfo,username):
        sql = ("update ruc.vip set vipdate='%s',vipsex='%s',province='%s',address='%s',vipphone='%s' where vipname='%s'"
                %(newInfo["birthdate"], newInfo["sex"], 
                    newInfo["province"], newInfo["address"], 
                    newInfo["phone"], username))
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True

    
    def vipViewOrders(self,username,gstate):
        vipno = self.__getvipno(username)
        sql = ("select * from ruc.orders o,ruc.goods g where o.gno=g.gno and vipno=%d and gstate='%s' order by orderdate"
                %(vipno,gstate))
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for i in range(len(result)):
            result[i]["gstate"] = self.__toZH(result[i]["gstate"])
            result[i]["gpic"] = self.__toZH(result[i]["gpic"])
            result[i]["gname"] = self.__toZH(result[i]["gname"])
            if result[i]["ascomment"]!=None:
                result[i]["ascomment"] = self.__toZH(result[i]["ascomment"])
        return result


    def storeViewOrders(self,username,gstate):
        stno = self.__getstno(username)
        if gstate=='待发货':
            sql = ("select * from ruc.orders o,ruc.goods g,ruc.vip v where o.vipno=v.vipno and o.gno=g.gno and stno=%d and gstate='待发货' order by orderdate"
                    %(stno))
        else:
            sql = ("select * from ruc.orders o,ruc.goods g,ruc.vip v where o.vipno=v.vipno and o.gno=g.gno and stno=%d and gstate<>'待发货' order by orderdate"
                    %(stno))
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for i in range(len(result)):
            result[i]["vipname"] = self.__toZH(result[i]["vipname"])
            result[i]["gstate"] = self.__toZH(result[i]["gstate"])
            result[i]["gpic"] = self.__toZH(result[i]["gpic"])
            result[i]["gname"] = self.__toZH(result[i]["gname"])
            if result[i]["ascomment"] != None:
                result[i]["ascomment"] = self.__toZH(result[i]["ascomment"])
        return result
    

    def comfirmReceipt(self,username,orderno,gno):
        vipno = self.__getvipno(username)
        sql = "update ruc.orders set gstate='待评价' where orderno=%d and gno=%d and vipno=%d"%(orderno,gno,vipno)
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True

    def deliver(self,username,orderno,gno):
        stno = self.__getstno(username)
        sql = ("update ruc.orders set gstate='待收货' where orderno=%d and gno=%d and gno in (select gno from ruc.goods where stno=%d)"
                %(orderno,gno,stno))
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True
    

    def giveComment(self,orderno,gno,score,comment):
        asdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        score = int(score)
        sql = ("update ruc.orders set gstate='已完成',asdate='%s',ascomment='%s',asscore=%d where orderno=%d and gno=%d"
               %(asdate,comment,score,orderno,gno))
        self.cursor.execute(sql)

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

    
    def charge(self,username,money):#充值
        vipno = self.__getvipno(username)
        sql = "update ruc.vip set vipmoney=vipmoney+%d where vipno=%d"%(money,vipno)
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True

    def randomItems(self,num):#随机选择一批商品
        sql = "select top %d * from ruc.goods order by newid()"%(num)
        try:
            self.cursor.execute(sql)
        except:
            return False
        result = self.cursor.fetchall()
        for i in range(len(result)):
            result[i]["gname"] = self.__toZH(result[i]["gname"])
            result[i]["gclass"] = self.__toZH(result[i]["gclass"])
            result[i]["gpic"] = self.__toZH(result[i]["gpic"])
        return result


    def searchItems(self,searchKeyWord):#搜索商品
        sql = ("select * from ruc.goods g,ruc.store s where g.stno=s.stno and (gname like \'"+'%'+"%s"%(searchKeyWord)+"%\'" + 
                " or gclass like \'"+'%'+"%s"%(searchKeyWord)+"%\'" + " or stname like \'"+'%'+"%s"%(searchKeyWord)+"%\')")
        try:
            self.cursor.execute(sql)
        except:
            return False
        searchResult = self.cursor.fetchall()
        for i in range(len(searchResult)):
            searchResult[i]["gname"] = self.__toZH(searchResult[i]["gname"])
            searchResult[i]["gclass"] = self.__toZH(searchResult[i]["gclass"])
            searchResult[i]["gpic"] = self.__toZH(searchResult[i]["gpic"])
        return searchResult


    def getItem(self,gno):#获取编号为gno的商品信息
        sql = "select * from ruc.goods g, ruc.store s where g.stno=s.stno and gno=%d"%(gno)
        try:
            self.cursor.execute(sql)
        except:
            return False
        itemInfo = self.cursor.fetchone()
        itemInfo["gname"] = self.__toZH(itemInfo["gname"])
        itemInfo["gclass"] = self.__toZH(itemInfo["gclass"])
        itemInfo["gpic"] = self.__toZH(itemInfo["gpic"])
        itemInfo["stname"] = self.__toZH(itemInfo["stname"])
        #均分
        sql = "select avg(asscore) avgscore from ruc.orders where gno=%d and asscore is not NULL"%(gno)
        self.cursor.execute(sql)
        itemInfo["avgscore"] = self.cursor.fetchone()["avgscore"]
        if itemInfo["avgscore"] == None: itemInfo["avgscore"] = '无'
        #销量
        sql = "select sum(gquantity) sale from ruc.orders where gno=%d"%(gno)
        self.cursor.execute(sql)
        itemInfo["sale"] = self.cursor.fetchone()["sale"]
        if itemInfo["sale"] == None: itemInfo["sale"] = 0
        return itemInfo


    def getComments(self,gno):#获取编号为gno的商品的评论
        sql = "select vipname,ascomment,asscore,asdate from ruc.orders o,ruc.vip p where o.vipno=p.vipno and gno=%d and ascomment is not NULL"%(gno)
        self.cursor.execute(sql)
        comments = self.cursor.fetchall()
        if len(comments)>0:
            for i in range(len(comments)):
                comments[i]["ascomment"] = self.__toZH(comments[i]["ascomment"])
        return comments


    def postItem(self,username,item,itempic):#发布商品
        sql = "select count(*) itemnum from ruc.goods"
        self.cursor.execute(sql)
        itemnum = self.cursor.fetchone()["itemnum"]
        sql = "select stno from ruc.store where stname='%s'"%(username)
        self.cursor.execute(sql)
        stno = self.cursor.fetchone()["stno"]
        sql = ("insert into ruc.goods values('%s',%d,'%s',%f,%d,%d,'%s')"
               %(item['gname'], itemnum+1, item['gclass'],
                 item['gprice'], stno, item['gstorage'],
                 itempic.filename))
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True

    
    def add2cart(self,username,gno,num):#添加商品至购物车
        vipno = self.__getvipno(username)

        sql = "select gstorage from ruc.goods where gno=%d"%(gno)
        self.cursor.execute(sql)
        storage = self.cursor.fetchone()["gstorage"]

        sql = "select * from ruc.cart where vipno=%d and gno=%d"%(vipno,gno)
        self.cursor.execute(sql)
        exist = self.cursor.fetchall()
        if len(exist)>0:#该用户的购物车已有这个商品
            if num+exist[0]["gquantity"]>storage: #加入购物车的数量不能超过库存数
                return False
            else:
                sql = "update ruc.cart set gquantity=gquantity+%d where vipno=%d and gno=%d"%(num,vipno,gno)
        else:#该用户的购物车没有这个商品
            if num>storage:#加入购物车的数量不能超过库存数
                return False
            else:
                sql = "insert into ruc.cart values(%d,%d,%d)"%(gno,vipno,num)
        try:
            self.cursor.execute(sql)
        except:
            return False
        else:
            return True


    def deleteFromCart(self,username,gno):#从购物车删除商品
        vipno = self.__getvipno(username)
        sql = "delete from ruc.cart where vipno=%d and gno=%d"%(vipno,gno)
        self.cursor.execute(sql)

    
    def checkCart(self,username):#查看购物车
        vipno = self.__getvipno(username)
        sql = "select gname,g.gno,gclass,gprice,s.stno,gstorage,gpic,vipno,gquantity,stname from ruc.goods g, ruc.cart c, ruc.store s where g.gno=c.gno and g.stno=s.stno and vipno=%d"%(vipno)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        groupResult = {}
        for i in range(len(result)):
            result[i]["gname"] = self.__toZH(result[i]["gname"])
            result[i]["gclass"] = self.__toZH(result[i]["gclass"])
            result[i]["stname"] = self.__toZH(result[i]["stname"])
            result[i]["gpic"] = self.__toZH(result[i]["gpic"])
            groupResult[result[i]["stname"]] = []
        for i in range(len(result)):
            groupResult[result[i]["stname"]].append(result[i])
        return groupResult


    def generateOrder(self,username):#生成订单
        cart = self.checkCart(username)
        cost = 0
        for items in cart.values():
            for item in items:
                cost += item["gquantity"] * item["gprice"]
                if item["gquantity"]>item["gstorage"]:
                    return "库存量不足"
        sql = "update ruc.vip set vipmoney=vipmoney-%d where vipname='%s'"%(cost,username)
        try:
            self.cursor.execute(sql)
        except:
            return "您的余额不足"
        vipno = self.__getvipno(username)
        ordertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "select orderno from ruc.orders group by orderno"
        self.cursor.execute(sql)
        orderno = len(self.cursor.fetchall())
        for items in cart.values():
            orderno += 1 #购物车中属于同一个商家的商品生成一个订单
            for item in items:
                #生成订单到orders表
                sql = ("insert into ruc.orders(orderno, orderdate, vipno, gno, gprice, gstate, gquantity,asscore,asdate) values(%d,'%s',%d,%d,%f,'%s',%d,%d,'%s')"
                        %(orderno,ordertime,vipno,item["gno"],item["gprice"],"待发货",item["gquantity"],1,''))
                self.cursor.execute(sql)
                #更新goods表中的库存量
                sql = "update ruc.goods set gstorage=gstorage-%d where gno=%d"%(item["gquantity"],item["gno"])
                self.cursor.execute(sql)
        #删除购物车中的商品
        sql = "delete from ruc.cart where vipno=%d"%(vipno)
        self.cursor.execute(sql)
        return "购买成功"


    def subscribe(self,username,stno):
        vipno = self.__getvipno(username)
        sql = "insert into ruc.subscribe values(%d,%d)"%(vipno,stno)
        try:
            self.cursor.execute(sql)
        except:
            pass


    def mySubscribe(self,username):
        vipno = self.__getvipno(username)
        sql = "select * from ruc.store st, ruc.subscribe sub where st.stno=sub.stno and sub.vipno=%d"%(vipno)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for i in range(len(result)):
            result[i]["stname"] = self.__toZH(result[i]["stname"])
        return result

    
    def unSubscribe(self,username,stno):
        vipno = self.__getvipno(username)
        sql = "delete from ruc.subscribe where vipno=%d and stno=%d"%(vipno,stno)
        try:
            self.cursor.execute(sql)
        except:
            pass
