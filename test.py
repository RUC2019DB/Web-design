#用于测试代码
from dbQuery import *
db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='eStore')#数据库
mycart = db.checkCart('ysy')
print(mycart)

import time


# 格式化成2016-03-20 11:45:39形式
print (thistime)
print(type(thistime))