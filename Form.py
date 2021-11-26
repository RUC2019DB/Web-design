# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,RadioField,IntegerField
from wtforms.validators import DataRequired,EqualTo

class signInForm(FlaskForm):
    username = StringField('用户名:',validators=[DataRequired()])
    password = PasswordField('密码:',validators=[DataRequired()])
    submit = SubmitField('登录')

    
class registerForm(FlaskForm):
    username = StringField('用户名:',validators=[DataRequired()])
    password1 = PasswordField('密码:',validators=[DataRequired()])
    password2 = PasswordField('确认密码:',validators=[DataRequired(),EqualTo('password1')])
    birthdate = DateField("出生日期:")
    sex = RadioField("性别:",choices=[('男','男'), ('女','女')])
    province = StringField('省份:')
    address = StringField('地址:')
    phone = IntegerField("手机号码:",validators=[DataRequired()])
    submit = SubmitField('注册')

class searchForm(FlaskForm):
    searchKeyWord = StringField('商品搜索:',validators=[DataRequired()])
    submit = SubmitField('搜索')