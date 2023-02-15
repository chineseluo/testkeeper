#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 22:37
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : forms.py
@IDE     : PyCharm
------------------------------------
"""
import wtforms
from wtforms.validators import Email, Length, EqualTo


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=50, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="用户名格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])


class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=5, max=50, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=8, max=200, message="密码格式错误！")])
    code = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    uuid = wtforms.StringField(validators=[Length(min=4, max=4, message="uuid格式错误！")])
