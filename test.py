#用于测试代码
from dbQuery import *
db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='China')#数据库
cursor = db.conn.cursor(as_dict=True)
sql = "update ruc.orders set gstate='待收货' where orderno=1 and gno=439 and gno in (select gno from ruc.goods where stno=1)"
cursor.execute(sql)
re = cursor.rowcount
print(re)