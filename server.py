from flask import Flask,render_template,request,flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo
from dbQuery import *

#服务器
app = Flask(__name__)
app.secret_key = "sdfha1561"#数据加密密钥

#数据库
db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='eStore')

@app.route('/',methods=['GET','POST'])
def home():
    my_list = [1,2,3,4,5]
    return render_template('home.html',my_list=my_list)


class signInForm(FlaskForm):
    username = StringField('用户名:',validators=[DataRequired()])
    password = PasswordField('密码:',validators=[DataRequired()])
    submit = SubmitField('登录')

@app.route("/signIn",methods=["GET","POST"])
def signIn():
    signIn_form = signInForm()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
    if signIn_form.validate_on_submit()==False:
        flash("用户名或密码不能为空")
    else:
        if db.checkPassword(username,password):
            flash("登录成功")
        else:
            flash("用户名或密码不正确")
    return render_template("signIn.html",signIn_form=signIn_form)

class registerForm(FlaskForm):
    username = StringField('用户名:',validators=[DataRequired()])
    password1 = PasswordField('密码:',validators=[DataRequired()])
    password2 = PasswordField('确认密码:',validators=[DataRequired(),EqualTo('password1')])
    submit = SubmitField('登录')

@app.route("/register",methods=["GET","POST"])
def register():
    register_Form = registerForm()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password1")
    if register_Form.validate_on_submit()==False:
        flash("注册信息有误")
    else:
        if db.checkPassword(username,password):
            flash("登录成功")
        else:
            flash("用户名或密码不正确")
    return render_template("register.html",register_Form=register_Form)
    

@app.route('/orders/<int:order_id>')
def get_order_id(order_id):
    return 'order_id = #%s'%order_id

if __name__ == '__main__':
    app.run()
