#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 16:19
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : views.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
from io import BytesIO
import base64
from flask import Flask, jsonify, render_template, request, make_response, session
from flask_jwt_extended import create_access_token
from testkeeper.webapi.auth import auth_blue
from testkeeper.util.image_operation import ImageCode
from testkeeper.util.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept
from werkzeug.datastructures import ImmutableMultiDict
from testkeeper.util.decode_opeation import decryption
from functools import wraps, update_wrapper


def session_check(func):
    @wraps(func)
    def check(*args, **kwargs):
        if session.get("username"):
            ret = func(*args, **kwargs)
            return ret
        else:
            return 200
    return check

@auth_blue.route("/login", methods=["POST"])
def login():
    form = LoginForm(ImmutableMultiDict(request.json))
    logger.info(request.json)
    logger.info(form.validate())
    if form.validate():
        username = form.username.data
        password = form.password.data
        user = SysUser.query.filter_by(user_name=username).first()
        if not user:
            logger.error(f"用户:{username}未注册!!!")
            return ""
        if user.password == decryption(password):
            session['user_id'] = user.user_id
            session['username'] = username
            session['password'] = password
            session.permanent = True
            logger.info(session['user_id'])
            access_token = create_access_token(identity=user.user_id)
            roles = []
            roles_level_list = ["admin"]
            for role in user.roles:
                role_dict = {"dataScope": role.data_scope, "id": role.role_id, "level": role.level, "name": role.name}
                roles.append(role_dict)
            jobs = []
            for job in user.jobs:
                job_dict = {
                    "id": job.job_id,
                    "name": job.name
                }
                jobs.append(job_dict)
            user_depts = SysDept.query.filter_by(dept_id=user.dept_id).all()
            depts = []
            for dept in user_depts:
                dept_dict = {
                    "id": dept.dept_id,
                    "name": dept.name
                }
                depts.append(dept_dict)
            # role_id = SysUserRoles.query.filter_by(user_id=user.user_id).first()
            # roles = SysRole.query.filter_by(role_id=role_id).all()
            user_info = {
                "token": f"Bearer {access_token}",
                "user": {
                    "user": {
                        "avatarName": user.avatar_name,
                        "avatarPath": user.avatar_path,
                        "createTime": user.create_time,
                        "email": user.email,
                        "enable": user.enable,
                        "gender": user.gender,
                        "id": user.user_id,
                        "isAdmin": user.is_admin,
                        "nickName": user.nick_name,
                        "password": user.password,
                        "phone": user.phone,
                        "pwdResetTime": user.pwd_reset_time,
                        "updateBy": user.update_by,
                        "updateTime": user.update_time,
                        "username": user.user_name,
                        "dept": depts,
                        "jobs": jobs,
                        "roles": roles
                    },
                    "authorities": {
                        "authority": "admin"
                    },
                    "dataScopes": [],
                    "roles": roles_level_list
                }
            }
            logger.info(user_info)
            return jsonify(user_info)
        else:
            logger.error(f"用户:{username}密码不正确!!!")
            return ""
    else:
        logger.error("校验用户名信息失败!!!")
        logger.error(form.errors)
        return ""


@auth_blue.route("/test/", methods=["GET"])
def test():
    logger.info("#########")
    return "test success"


@session_check
@auth_blue.route("/logout", methods=["DELETE"])
def logout():
    session.pop("id", None)
    session.pop("username", None)
    session.pop("password", None)
    return "200"


@auth_blue.route("/code", methods=["GET"])
def code():
    image_code = ImageCode()
    image, code = image_code.getVerifyCode()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'png')
    buf_data = buf.getvalue()
    logger.info(buf_data)
    logger.info(type(buf_data))
    buf_str = base64.b64encode(buf_data).decode('utf-8')
    # response = make_response(buf_str)
    # response.headers['Content-Type'] = 'image/png'
    # session['imageCode'] = code
    # logger.info(code)

    test_dict = {
        "uuid": f"{code}",
        "img": f"data:img/png;base64,{buf_str}"
    }
    return test_dict




if __name__ == '__main__':
    test_str = generate_password_hash("123456")
    print(test_str)
