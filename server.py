# coding=utf-8
from flask import Flask,render_template,request,flash,redirect,session
from flask.helpers import url_for
from dbQuery import *
from Form import *

#服务器
app = Flask(__name__)
app.secret_key = "sdfha1561"#数据加密密钥
app.config['JSON_AS_ASCII'] = False

@app.route('/',methods=['GET','POST'])
def home():
    search_Form = searchForm()
    randomItems = db.randomItems(5)
    return render_template('home.html',username=session.get('username'),search_Form=search_Form,randomItems=randomItems)


@app.route("/signIn",methods=["GET","POST"])
def signIn():
    try:
        session.pop("username")
    except:
        pass
    signIn_form = signInForm()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if signIn_form.validate_on_submit()==False:
            flash("用户名或密码不能为空")
        else:
            if db.checkPassword(username,password):
                session["username"] = username
                return redirect(url_for('home'))
            else:
                flash("用户名或密码不正确")

    return render_template("signIn.html",signIn_form=signIn_form)


@app.route("/register",methods=["GET","POST"])
def register():
    register_Form = registerForm()
    if request.method == "POST":
        userInfo = request.form.to_dict()
        if register_Form.validate_on_submit()==False:
            flash("注册信息有误")
        else:
            if db.register(userInfo):
                return redirect(url_for('signIn'))
            else:
                flash("注册信息有误")

    return render_template("register.html",register_Form=register_Form)
    

@app.route("/searchResult/?<string:searchKeyWord>",methods=["GET","POST"])
def searchResult(searchKeyWord):
    result = db.searchItems(searchKeyWord)
    return render_template("searchResult.html",username=session.get('username'),result=result)


@app.route("/search/",methods=["GET","POST"])
def search():
    search_Form = searchForm()
    if (request.method == "POST")&(search_Form.validate_on_submit()):
        searchKeyWord = request.form.get("searchKeyWord")
        return redirect(url_for("searchResult",searchKeyWord=searchKeyWord))
    return render_template('home.html',username=session.get('username'),search_Form=search_Form)


@app.route("/item/?<int:gno>",methods=["GET","POST"])
def item(gno):
    itemInfo = db.getItem(gno)
    return render_template("item.html",itemInfo=itemInfo)

if __name__ == '__main__':
    db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='eStore')#数据库
    if db.ifconn:
        print("数据库连接成功")
        app.run()
    else:
        print("数据库连接失败")
