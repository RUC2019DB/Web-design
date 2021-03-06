# coding=utf-8
from flask import Flask,render_template,request,flash,redirect,session
from flask.helpers import url_for
import matplotlib.pyplot as plt
from dbQuery import *
from Form import *
import socket
import os

#服务器
app = Flask(__name__)
app.secret_key = "sdfha1561"#数据加密密钥
app.config['JSON_AS_ASCII'] = False

hostname = socket.gethostname()
serverIP= socket.gethostbyname(hostname)

@app.route('/',methods=['GET','POST'])
def home():
    search_Form = searchForm()
    randomItems = db.randomItems(10)
    if (request.method == "POST")&(search_Form.validate_on_submit()):
        searchKeyWord = request.form.get("searchKeyWord")
        return redirect(url_for("searchResult",searchKeyWord=searchKeyWord,orderby='None',reverse='F'))
    return render_template('home.html',usertype=session.get('usertype'),username=session.get('username'),
                           search_Form=search_Form,randomItems=randomItems)


@app.route("/searchResult/?<string:searchKeyWord>/?<string:orderby>/?<string:reverse>",methods=["GET","POST"])
def searchResult(searchKeyWord,orderby,reverse):
    result = db.searchItems(searchKeyWord,orderby,reverse)
    return render_template("searchResult.html", username=session.get('username'),
                            result=result, searchKeyWord=searchKeyWord)


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


@app.route("/vipPage",methods=["GET","POST"])
def vipPage():
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!='VIP':
        return "请登录VIP账户"
    else:
        vipInfo = db.vipInfo(username)
        return render_template("vip.html",vipInfo=vipInfo)


@app.route("/updateInfo",methods=["GET","POST"])
def updateInfo():
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype=='VIP':
        updateVip_form = vipRegisterForm()
        if request.method=='POST':
            newInfo = request.form.to_dict()
            if db.updateInfo(newInfo,username):
                flash("修改成功")
            else:
                flash("信息有误")
        return render_template("updateInfo.html",updateVip_form=updateVip_form)
    else:
        return "请登录VIP账户"


@app.route("/vipViewOrders/?<string:gstate>",methods=["GET","POST"])
def vipViewOrders(gstate):
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!='VIP':
        return "请登录VIP账户"
    else:
        orders = db.vipViewOrders(username,gstate)
        return render_template("vipViewOrders.html",orders=orders,gstate=gstate)


@app.route("/comfirmReceipt/?<int:orderno>/?<int:gno>",methods=["GET","POST"])
def comfirmReceipt(orderno,gno):
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!='VIP':
        return "请登录VIP账户"
    else:
        if db.comfirmReceipt(username,orderno,gno):
            return "确认成功"
        else:
            return "确认失败"

@app.route("/giveComment/?<int:orderno>/?<int:gno>",methods=["GET","POST"])
def giveComment(orderno,gno):
    comment_form = commentForm()
    if request.method=='POST':
        score = request.form.get("score")
        comment = request.form.get("comment")
        db.giveComment(orderno,gno,score,comment)
        return redirect(url_for('vipPage'))
    return render_template("giveComment.html",comment_form=comment_form)


@app.route("/storePage",methods=["GET","POST"])
def storePage():
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!='商家':
        return "请登录商家账户"
    else:
        storeInfo = db.storeInfo(username)
        items = db.storeViewItems(username)
        return render_template("store.html",storeInfo=storeInfo,items=items)


@app.route("/storeProfits",methods=["GET","POST"])
def storeProfits():
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!='商家':
        return "请登录商家账户"
    else:
        storeInfo = db.storeInfo(username)
        yearsProfits, monthsProfits, provincesProfits = db.storeProfits(username)
        return render_template("storeProfits.html",storeInfo=storeInfo,
                                yearsProfits=yearsProfits, monthsProfits=monthsProfits,
                                provincesProfits=provincesProfits)


@app.route("/storeViewOrders/?<string:gstate>",methods=["GET","POST"])
def storeViewOrders(gstate):
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!='商家':
        return "请登录商家账户"
    else:
        orders = db.storeViewOrders(username,gstate)
        return render_template("storeViewOrders.html",orders=orders,gstate=gstate)


@app.route("/deliver/?<int:orderno>/?<int:gno>",methods=["GET","POST"])
def deliver(orderno,gno):
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!='商家':
        return "请登录商家账户"
    else:
        if db.deliver(username,orderno,gno):
            return "发货成功"
        else:
            return "发货失败"

@app.route("/charge",methods=["GET","POST"])
def charge():
    charge_form = chargeForm()
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!='VIP':
        return "请登录VIP账户"
    else:
        if request.method == 'POST':
            money = int(request.form.get("money"))
            if db.charge(username,money):
                flash("充值成功")
            else:
                flash("充值失败")
        return render_template("charge.html",charge_form=charge_form)


@app.route("/item/?<int:gno>",methods=["GET","POST"])
def item(gno):
    item = db.getItem(gno)
    comments = db.getComments(gno)
    return render_template("item.html",item=item,comments=comments)


@app.route("/postItem/?<int:postgno>",methods=["GET","POST"])
def postItem(postgno):
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!='商家':
        return "商家请先登录"
    else:
        if postgno==0:
            title = "发布商品"
        else:
            title = "更新商品(请填写需要修改的部分)"
        if request.method == "POST":
            item = request.form.to_dict()
            itempic = request.files.get("gpic")
            if postgno == 0:
                if ((item["gname"]=='')|(item["gclass"]=='')|(itempic.filename=='')):
                    flash("商品信息有误")
                else:
                    try:
                        item["gprice"] = float(item["gprice"])
                        item["gstorage"] = int(item["gstorage"])
                    except:
                        flash("商品信息有误")
                    else:
                        if db.postItem(username,item,itempic):
                            itempic.save(os.path.join('static/',itempic.filename))
                            flash("上传成功!")
                        else:
                            flash("上传失败")
            else:
                if db.updateItem(postgno,item,itempic):
                    if len(itempic.filename):
                        itempic.save(os.path.join('static/',itempic.filename))
                    flash("上传成功!")
                else:
                    flash("上传失败")
        return render_template('postItem.html',postgno=postgno,title=title)


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
                else:
                    return "添加成功!"
    return redirect(url_for('item',gno=gno))


@app.route("/deleteFromCart/?<int:gno>",methods=["GET","POST"])
def deleteFromCart(gno):
    if request.method=="POST":
        username = session.get("username")
        db.deleteFromCart(username,gno)
    return redirect(url_for('shoppingCart'))


@app.route("/shoppingCart",methods=["GET","POST"])
def shoppingCart():
    cart = None
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!="VIP":
        return "请登录VIP账户"
    else:
        cart = db.checkCart(username,0)
        return render_template("shoppingCart.html",cart=cart)

@app.route("/add2Order/?<int:gno>",methods=["GET","POST"])
def add2Order(gno):
    if request.method=="POST":
        username = session.get("username")
        db.add2Order(username,gno)
    return redirect(url_for('shoppingCart'))


@app.route("/addAll2Order",methods=["GET","POST"])
def addAll2Order():
    if request.method=="POST":
        username = session.get("username")
        db.addAll2Order(username)
    return redirect(url_for('shoppingCart'))


@app.route("/delAllFromOrder",methods=["GET","POST"])
def delAllFromOrder():
    if request.method=="POST":
        username = session.get("username")
        db.delAllFromOrder(username)
    return redirect(url_for('shoppingCart'))


@app.route("/delFromOrder/?<int:gno>",methods=["GET","POST"])
def delFromOrder(gno):
    if request.method=="POST":
        username = session.get("username")
        db.delFromOrder(username,gno)
    return redirect(url_for('shoppingCart'))


@app.route("/pay",methods=["GET","POST"])
def pay():
    usertype = session.get("usertype")
    username = session.get("username")
    allPrice = 0
    cart = None
    if usertype!="VIP":
        flash("请登录VIP账户")
    else:
        cart = db.checkCart(username,1)
        for items in cart.values():
            for item in items:
                allPrice += item["gprice"] * item["gquantity"]
        if request.method == 'POST':
            if len(cart)==0:
                flash("购物车为空")
            else:
                return db.generateOrder(username)  
    return render_template("pay.html",cart=cart,allPrice=allPrice)


@app.route("/subscribe/?<int:stno>",methods=["GET","POST"])
def subscribe(stno):
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!="VIP":
        return "请登录VIP账户"
    else:
        db.subscribe(username,stno)
        return "关注成功"


@app.route("/mySubscribe",methods=["GET","POST"])
def mySubscribe():
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!="VIP":
        return "请登录VIP账户"
    else:
        subscribeList = db.mySubscribe(username)
        return render_template("mySubscribe.html",subscribeList=subscribeList)


@app.route("/unSubscribe/?<int:stno>",methods=["GET","POST"])
def unSubscribe(stno):
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!="VIP":
        return "请登录VIP账户"
    else:
        db.unSubscribe(username,stno)
        return redirect( url_for('mySubscribe') )


@app.route("/statistic",methods=["GET","POST"])
def statistic():
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype == None:
        return "请登录账户"
    else:
        data = db.statistic()
        return render_template("statistic.html", data=data)


@app.route("/vipHistory",methods=["GET","POST"])
def vipHistory():
    usertype = session.get("usertype")
    username = session.get("username")
    if usertype!="VIP":
        return "请登录VIP账户"
    else:
        myFaItems = db.myFavoriteItems(username)
        return render_template("vipHistory.html",myFaItems=myFaItems)


if __name__ == '__main__':
    db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='China')#数据库
    if db.ifconn:
        print("数据库连接成功")
        app.run(host=serverIP,port='5000')
    else:
        print("数据库连接失败")
