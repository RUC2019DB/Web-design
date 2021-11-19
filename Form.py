from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo

class signInForm(FlaskForm):
    username = StringField('用户名:',validators=[DataRequired()])
    password = PasswordField('密码:',validators=[DataRequired()])
    submit = SubmitField('登录')

    
class registerForm(FlaskForm):
    username = StringField('用户名:',validators=[DataRequired()])
    password1 = PasswordField('密码:',validators=[DataRequired()])
    password2 = PasswordField('确认密码:',validators=[DataRequired(),EqualTo('password1')])
    submit = SubmitField('登录')

class searchForm(FlaskForm):
    searchKeyWord = StringField('商品搜索:',validators=[DataRequired()])
    submit = SubmitField('搜索')