# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,RadioField,IntegerField,SelectField
from wtforms.validators import DataRequired,EqualTo

class signInForm(FlaskForm):
    usertype = RadioField("我 是:",choices=[("商家","商家"),("VIP","VIP")],validators=[DataRequired("请选择")])
    username = StringField('用户名:',validators=[DataRequired("用户名不能为空")])
    password = PasswordField('密 码:',validators=[DataRequired("密码不能为空")])
    submit = SubmitField('登录')

    
class vipRegisterForm(FlaskForm):
    username = StringField('用 户 名:',validators=[DataRequired("用户名不能为空")])
    password1 = PasswordField('密 码:',validators=[DataRequired("密码不能为空")])
    password2 = PasswordField('确认密码:',validators=[DataRequired("确认密码不能为空"),EqualTo('password1',"密码不一致")])
    birthdate = DateField("出生日期:")
    sex = RadioField("性 别:",choices=[('男','男'), ('女','女')])
    province = StringField('省 份:')
    address = StringField('地 址:')
    phone = StringField("手机号码:",validators=[DataRequired("手机号码不能为空")])
    submit = SubmitField('确认')

class storeRegisterForm(FlaskForm):
    storename = StringField('用 户 名:',validators=[DataRequired("用户名不能为空")])
    password1 = PasswordField('密 码:',validators=[DataRequired("密码不能为空")])
    password2 = PasswordField('确认密码:',validators=[DataRequired("确认密码不能为空"),EqualTo('password1',"密码不一致")])
    address = StringField('地 址:')
    submit = SubmitField('确认')


class searchForm(FlaskForm):
    searchKeyWord = StringField('商品搜索:',validators=[DataRequired()])
    submit = SubmitField('搜索')


class chargeForm(FlaskForm):
    money = IntegerField("充值金额",validators=[DataRequired()])
    cardID = IntegerField("银行卡号",validators=[DataRequired()])
    password = PasswordField('密 码:',validators=[DataRequired("密码不能为空")])
    submit = SubmitField('充值')


class commentForm(FlaskForm):
    score = SelectField("评分",validators=[DataRequired('请选择')],
                               render_kw={'class':'form-control'},
                               choices=[(1,1),(2,2),(3,3),(4,4),(5,5)],
                               default = 3,
                               coerce=int)
    comment = StringField("评论",validators=[DataRequired()])
    submit = SubmitField('提交')

