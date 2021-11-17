from flask import Flask,render_template
import pymssql

def dbconnect():
    connect = pymssql.connect('127.0.0.1', 'sa', '123456', 'TPCH')
    if connect:
        print("连接成功!")
    return connect

#服务器
app = Flask(__name__) 

#数据库
db = dbconnect()
cursor = db.cursor()

@app.route('/',methods=['GET','POST'])
def home():
    my_list = [1,2,3,4,5]
    return render_template('home.html',my_list=my_list)

@app.route('/orders/<int:order_id>')
def get_order_id(order_id):
    return 'order_id = #%s'%order_id

if __name__ == '__main__':
    cursor.execute("select count(*) from Sales.Nation")
    result = cursor.fetchone()
    print(result)
    app.run()
