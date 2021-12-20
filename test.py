#用于测试代码
from dbQuery import *
db = dbQuery(dbIP='127.0.0.1',dbusername='sa',dbpassword='123456',dbname='Chinese')#数据库

province_list = [('河北省', '河北省'), ('山西省', '山西省'), ('辽宁省', '辽宁省'), ('吉林省', '吉林省'), 
                     ('黑龙江省', '黑龙江省'), ('江苏省', '江苏省'), ('浙江省', '浙江省'), ('安徽省', '安徽省'), 
                     ('福建省', '福建省'), ('江西省', '江西省'), ('山东省', '山东省'), ('河南省', '河南省'), 
                     ('湖北省', '湖北省'), ('湖南省', '湖南省'), ('广东省', '广东省'), ('海南省', '海南省'), 
                     ('四川省', '四川省'), ('贵州省', '贵州省'), ('云南省', '云南省'), ('陕西省', '陕西省'), 
                     ('甘肃省', '甘肃省'), ('青海省', '青海省'), ('台湾省', '台湾省'), ('内蒙古自治区', '内蒙古自治区'), 
                     ('广西壮族自治区', '广西壮族自治区'), ('西藏自治区', '西藏自治区'), ('宁夏回族自治区', '宁夏回族自治区'), 
                     ('新疆维吾尔自治区', '新疆维吾尔自治区'), ('北京市', '北京市'), ('天津市', '天津市'), ('上海市', '上海市'), 
                     ('重庆市', '重庆市'), ('香港特别行政区', '香港特别行政区'), ('澳门特别行政区', '澳门特别行政区')]
province_list = sorted(province_list,key=lambda x:x)
print(province_list[0][0])