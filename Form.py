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
    province_list = [('河北省', '河北省'), ('山西省', '山西省'), ('辽宁省', '辽宁省'), ('吉林省', '吉林省'), 
                     ('黑龙江省', '黑龙江省'), ('江苏省', '江苏省'), ('浙江省', '浙江省'), ('安徽省', '安徽省'), 
                     ('福建省', '福建省'), ('江西省', '江西省'), ('山东省', '山东省'), ('河南省', '河南省'), 
                     ('湖北省', '湖北省'), ('湖南省', '湖南省'), ('广东省', '广东省'), ('海南省', '海南省'), 
                     ('四川省', '四川省'), ('贵州省', '贵州省'), ('云南省', '云南省'), ('陕西省', '陕西省'), 
                     ('甘肃省', '甘肃省'), ('青海省', '青海省'), ('台湾省', '台湾省'), ('内蒙古自治区', '内蒙古自治区'), 
                     ('广西壮族自治区', '广西壮族自治区'), ('西藏自治区', '西藏自治区'), ('宁夏回族自治区', '宁夏回族自治区'), 
                     ('新疆维吾尔自治区', '新疆维吾尔自治区'), ('北京市', '北京市'), ('天津市', '天津市'), ('上海市', '上海市'), 
                     ('重庆市', '重庆市'), ('香港特别行政区', '香港特别行政区'), ('澳门特别行政区', '澳门特别行政区')]
    username = StringField('用 户 名:',validators=[DataRequired("用户名不能为空")])
    password1 = PasswordField('密 码:',validators=[DataRequired("密码不能为空")])
    password2 = PasswordField('确认密码:',validators=[DataRequired("确认密码不能为空"),EqualTo('password1',"密码不一致")])
    birthdate = DateField("出生日期:")
    sex = SelectField("性 别:", choices = [('男','男'), ('女','女')],
                                validators=[DataRequired('请选择')],
                                render_kw={'class':'form-control'},
                                coerce=str)
    province = SelectField('省 份:',choices = province_list,
                                    validators=[DataRequired('请选择')],
                                    render_kw={'class':'form-control'},
                                    coerce=str)
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

