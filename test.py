#用于测试代码
from dbQuery import *
db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='eStore')#数据库
print(db.randomItems(5))