# -*- coding: utf-8 -*-
from users.models import User
import re


def verify_username(name):
    name_dic = {}
    msg = ''
    query = User.objects.filter(username=name).values('username')
    if len(name) < 3:
        msg += '用户名长度不能低于3位！'
    elif query:
        msg += '用户名已注册！'
    name_dic['name'] = msg
    return name_dic


def verify_phone(phone):
    msg = ''
    phone_dic = {}
    p2 = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    phone_match = p2.match(phone)
    query = User.objects.filter(mobile=phone).values('mobile')
    if not phone_match:
        msg = msg + '手机格式不对！'
    elif query:
        msg = msg + '手机号已注册！'
    phone_dic['phone'] = msg
    return phone_dic


def verify_pwd(pwd, pwd2):
    pwd_dic = {}
    msg = ''
    if len(str(pwd)) < 6:
        msg = msg + '密码长度小于6位！'
    elif pwd != pwd2:
        msg = msg + '两次密码不一致！'
    pwd_dic['pwd'] = msg
    return pwd_dic


def verify_email(email):
    str = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if re.match(str, email):
        return 'ok'
    else:
        return 'error'
