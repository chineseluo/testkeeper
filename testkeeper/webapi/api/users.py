#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 18:24
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : users.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
from io import BytesIO
import base64
from flask import Flask, jsonify, render_template, request, make_response, session
from flask_jwt_extended import create_access_token
from testkeeper.webapi.api import api_blue
from testkeeper.util.image_operation import ImageCode
from testkeeper.util.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept
from werkzeug.datastructures import ImmutableMultiDict
from testkeeper.util.decode_opeation import decryption
from functools import wraps, update_wrapper


@api_blue.route("/users", methods=["GET"])
def get_users():
    page = request.args["page"]
    size = request.args["size"]
    sort = request.args["sort"]
    try:
        deptId = request.args["deptId"]
    except Exception as e:
        deptId = None
    content_dict = {
        "content": []
    }
    users = SysUser.query.all()
    if deptId is None:
        logger.info("查询所有user用户")
        for user in users:
            roles = []
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
            }
            content_dict["content"].append(user_info)
    else:
        for user in users:
            roles = []
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
            }
            content_dict["content"].append(user_info)
    content_dict.update({"totalElements": len(users)})
    return content_dict
