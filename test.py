#用于测试代码
from dbQuery import *
db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='China')#数据库
cursor = db.conn.cursor(as_dict=True)
stno = 1
sql = ("select province,sum(o.gprice*o.gquantity) profits from ruc.orders o,ruc.goods g,ruc.vip v where o.gno=g.gno and v.vipno=o.vipno and stno=%d group by province"
                %(stno))
print(sql)
cursor.execute(sql)
provincesProfits = cursor.fetchall()
provincesProfits = sorted(provincesProfits,key=lambda x:x["province"])
print(provincesProfits)