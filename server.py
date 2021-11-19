from flask import Flask,render_template,request,flash,redirect,session
from flask.helpers import url_for
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo
from dbQuery import *
from Form import *

#服务器
app = Flask(__name__)
app.secret_key = "sdfha1561"#数据加密密钥

@app.route('/',methods=['GET','POST'])
def home():
    search_Form = searchForm()
    return render_template('home.html',username=session.get('username'),search_Form=search_Form)


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
        username = request.form.get("username")
        password = request.form.get("password1")
        if register_Form.validate_on_submit()==False:
            flash("注册信息有误")
        else:
            if db.register(username,password):
                return redirect(url_for('signIn'))
            else:
                flash("注册信息有误")

    return render_template("register.html",register_Form=register_Form)
    

@app.route("/search",methods=["GET","POST"])
def search():
    search_Form = searchForm()
    if request.method == "POST":
        searchKeyWord = request.form.get("searchKeyWord")
        if search_Form.validate_on_submit():
            searchResult = db.searchItems(searchKeyWord)
            return render_template("searchResult.html",username=session.get('username'),searchResult=searchResult)

    return render_template('home.html',username=session.get('username'),search_Form=search_Form)


if __name__ == '__main__':
    db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='eStore')#数据库
    if db.ifconn:
        print("数据库连接成功")
        app.run()
    else:
        print("数据库连接失败")
