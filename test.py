#用于测试代码
from dbQuery import *
db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='eStore')#数据库
sql = "select vipkey from ruc.vip where vipname='%s'"%('ysy')
db.cursor.execute(sql)
result = db.cursor.fetchone()

p = 2=='2'
print(p)
