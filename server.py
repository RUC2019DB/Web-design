# coding=utf-8
from flask import Flask,render_template,request,flash,redirect,session
from flask.helpers import url_for
from dbQuery import *
from Form import *
import os

#服务器
app = Flask(__name__)
app.secret_key = "sdfha1561"#数据加密密钥
app.config['JSON_AS_ASCII'] = False

@app.route('/',methods=['GET','POST'])
def home():
    search_Form = searchForm()
    randomItems = db.randomItems(5)
    return render_template('home.html',usertype=session.get('usertype'),username=session.get('username'),
                           search_Form=search_Form,randomItems=randomItems)


@app.route("/signIn",methods=["GET","POST"])
def signIn():
    try:
        session.pop("username")
        session.pop("usertype")
    except:
        pass
    signIn_form = signInForm()
    if request.method == "POST":
        usertype = request.form.get("usertype")
        username = request.form.get("username")
        password = request.form.get("password")
        if signIn_form.validate_on_submit()==False:
            flash("登录信息不能为空")
        else:
            if db.checkPassword(usertype,username,password):
                session["usertype"] = usertype
                session["username"] = username
                return redirect(url_for('home'))
            else:
                flash("用户名或密码不正确")

    return render_template("signIn.html",signIn_form=signIn_form)


@app.route("/vipRegister",methods=["GET","POST"])
def vipRegister():
    vipRegister_Form = vipRegisterForm()
    if request.method == "POST":
        userInfo = request.form.to_dict()
        if vipRegister_Form.validate_on_submit()==False:
            flash("注册信息有误")
        else:
            if db.vipRegister(userInfo):
                return redirect(url_for('signIn'))
            else:
                flash("注册信息有误")

    return render_template("vipRegister.html",vipRegister_Form=vipRegister_Form)
    

@app.route("/storeRegister",methods=["GET","POST"])
def storeRegister():
    storeRegister_Form = storeRegisterForm()
    if request.method == "POST":
        storeInfo = request.form.to_dict()
        if storeRegister_Form.validate_on_submit()==False:
            flash("注册信息有误")
        else:
            if db.storeRegister(storeInfo):
                return redirect(url_for('signIn'))
            else:
                flash("注册信息有误")

    return render_template("storeRegister.html",storeRegister_Form=storeRegister_Form)


@app.route("/searchResult/?<string:searchKeyWord>",methods=["GET","POST"])
def searchResult(searchKeyWord):
    result = db.searchItems(searchKeyWord)
    return render_template("searchResult.html",username=session.get('username'),result=result)


@app.route("/search",methods=["GET","POST"])
def search():
    search_Form = searchForm()
    if (request.method == "POST")&(search_Form.validate_on_submit()):
        searchKeyWord = request.form.get("searchKeyWord")
        return redirect(url_for("searchResult",searchKeyWord=searchKeyWord))
    return render_template('home.html',username=session.get('username'),search_Form=search_Form)


@app.route("/item/?<int:gno>",methods=["GET","POST"])
def item(gno):
    item = db.getItem(gno)
    comments = db.getComments(gno)
    return render_template("item.html",item=item,comments=comments)


@app.route("/postItem",methods=["GET","POST"])
def postItem():
    if request.method == "POST":
        usertype = session.get("usertype")
        username = session.get("username")
        if usertype!='商家':
            flash("商家请先登录")
        else:
            item = request.form.to_dict()
            itempic = request.files.get("itempic")
            if ((item["itemname"]=='')|(item["itemsort"]=='')|(itempic.filename=='')):
                flash("商品信息有误")
            else:
                try:
                    item["itemprice"] = float(item["itemprice"])
                    item["itemsale"] = int(item["itemsale"])
                except:
                    flash("商品信息有误")
                else:
                    if db.postItem(username,item,itempic):
                        itempic.save(os.path.join('static/',itempic.filename))
                        flash("上传成功!")
                    else:
                        flash("上传失败")
    return render_template('postItem.html')


@app.route("/add2cart/?<int:gno>",methods=["GET","POST"])
def add2cart(gno):
    if request.method == "POST":
        usertype = session.get("usertype")
        username = session.get("username")
        if usertype!='VIP':
            flash("请登录VIP账户")
        else:
            try:
                num = int(request.form.get("num"))
            except:
                flash("请输入购买数量")
            else:
                if db.add2cart(username,gno,num)==False:
                    flash("加入购物车的数量不能超过库存数")
    return redirect(url_for('item',gno=gno))


@app.route("/shoppingCart",methods=["GET","POST"])
def shoppingCart():
    cart = None
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!="VIP":
        flash("请登录VIP账户")
    else:
        cart = db.checkCart(username)
    return render_template("shoppingCart.html",cart=cart)


@app.route("/deleteFromCart/?<int:gno>",methods=["GET","POST"])
def deleteFromCart(gno):
    if request.method=="POST":
        username = session.get("username")
        db.deleteFromCart(username,gno)
    return redirect(url_for('shoppingCart'))


@app.route("/pay",methods=["GET","POST"])
def pay():
    usertype = session.get("usertype")
    username = session.get("username")
    allPrice = 0
    allItem = None
    if usertype!="VIP":
        flash("请登录VIP账户")
    else:
        cart = db.checkCart(username)
        for items in cart.values():
            for item in items:
                allPrice += item["gprice"] * item["gquantity"]
        if request.method == 'POST':
            if len(allItem)==0:
                flash("购物车为空")
            else:
                if db.generateOrder(username):
                    return "付款成功"
                else:
                    flash("订单有误,库存量不足")
    return render_template("pay.html",cart=cart,allPrice=allPrice)


if __name__ == '__main__':
    db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='Chinese')#数据库
    if db.ifconn:
        print("数据库连接成功")
        app.run()
    else:
        print("数据库连接失败")
