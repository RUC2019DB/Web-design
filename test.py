#用于测试代码
from dbQuery import *
db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='Chinese')#数据库

username='配饰工程师旗舰店'
sql = "select stkey from ruc.store where stname='%s'"%(username)
db.cursor.execute(sql)
result = db.cursor.fetchone()
print(result)
