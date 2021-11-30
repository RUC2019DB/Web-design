# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,RadioField,IntegerField,FloatField
from wtforms.validators import DataRequired,EqualTo

class signInForm(FlaskForm):
    usertype = RadioField("我是:",choices=[("商家","商家"),("VIP","VIP")],validators=[DataRequired("请选择")])
    username = StringField('用户名:',validators=[DataRequired("用户名不能为空")])
    password = PasswordField('密码:',validators=[DataRequired("密码不能为空")])
    submit = SubmitField('登录')

    
class vipRegisterForm(FlaskForm):
    username = StringField('用户名:',validators=[DataRequired("用户名不能为空")])
    password1 = PasswordField('密码:',validators=[DataRequired("密码不能为空")])
    password2 = PasswordField('确认密码:',validators=[DataRequired("确认密码不能为空"),EqualTo('password1',"密码不一致")])
    birthdate = DateField("出生日期:")
    sex = RadioField("性别:",choices=[('男','男'), ('女','女')])
    province = StringField('省份:')
    address = StringField('地址:')
    phone = StringField("手机号码:",validators=[DataRequired("手机号码不能为空")])
    submit = SubmitField('注册')

class storeRegisterForm(FlaskForm):
    storename = StringField('用户名:',validators=[DataRequired("用户名不能为空")])
    password1 = PasswordField('密码:',validators=[DataRequired("密码不能为空")])
    password2 = PasswordField('确认密码:',validators=[DataRequired("确认密码不能为空"),EqualTo('password1',"密码不一致")])
    address = StringField('地址:')
    submit = SubmitField('注册')


class searchForm(FlaskForm):
    searchKeyWord = StringField('商品搜索:',validators=[DataRequired()])
    submit = SubmitField('搜索')


class payForm(FlaskForm):
    receiver = StringField("收货人",validators=[DataRequired()])
    phone = StringField("手机号码:",validators=[DataRequired()])
    address = StringField('收货地址:',validators=[DataRequired()])
    submit = SubmitField('支付')
