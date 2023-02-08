#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 16:58
@Auth    : luozhongwen
@Email   : luozhongwen@sensorsdata.cn
@File    : sys_user_module.py
@IDE     : PyCharm
------------------------------------
"""
import json
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event
from loguru import logger
from sqlalchemy import Column, String, Integer, DateTime, Text, Table, ForeignKey, BOOLEAN
from sqlalchemy.dialects.sqlite import *
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
from sqlalchemy.orm import relationship, backref, sessionmaker
from testkeeper.util.file_operation import FileOption

Base = declarative_base()


# 用户表
class SysUser(Base):
    __table__ = "sys_user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_id = Column(Integer, nullable=False)
    user_name = Column(String(100), nullable=False)
    nick_name = Column(String(100), nullable=False)
    gender = Column(String(2), nullable=False)
    phone = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    avatar_name = Column(String(100), nullable=True)  # 头像地址
    avatar_path = Column(String(100), nullable=True)  # 头像真实路径
    password = Column(String(100), nullable=True)
    is_admin = Column(String(1), nullable=True)  # 是否是超级管理员
    enable = Column(String(1), nullable=True)  # 启用/禁用
    create_by = Column(String(100), nullable=True)  # 创建者
    update_by = Column(String(100), nullable=True)  # 修改者
    pwd_reset_time = Column(TIMESTAMP, nullable=False)  # 修改密码时间
    create_time = Column(TIMESTAMP, nullable=False)  # 创建日期
    update_time = Column(TIMESTAMP, nullable=False)  # 更新日期


# 部门表
class SysDept(Base):
    __table__ = "sys_dept"
    dept_id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, nullable=False)  # 上级部门Id
    sub_count = Column(Integer, nullable=False)  # 子部门数目
    name = Column(String(100), nullable=False)  # 部门名称
    dept_sort = Column(Integer, nullable=False)  # 排序
    enable = Column(String(1), nullable=True)  # 启用/禁用
    create_by = Column(String(100), nullable=True)  # 创建者
    update_by = Column(String(100), nullable=True)  # 修改者
    create_time = Column(TIMESTAMP, nullable=False)  # 创建日期
    update_time = Column(TIMESTAMP, nullable=False)  # 更新日期


class SysMenu(Base):
    __table__ = "sys_menu"
    menu_id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, nullable=False)  # 上级菜单Id
    sub_count = Column(Integer, nullable=False)  # 子菜单数目
    type = Column(String(11), nullable=True)  # 菜单类型
    title = Column(String(100), nullable=True)  # 菜单标题
    name = Column(String(100), nullable=False)  # 组件名称
    component = Column(String(100), nullable=False)  # 组件
    menu_sort = Column(Integer, nullable=False)  # 排序
    icon = Column(String(100), nullable=False)  # 图标
    path = Column(String(100), nullable=False)  # 图标地址
    i_frame = Column(String(1), nullable=False)  # 是否外链
    cache = Column(String(1), nullable=False)  # 是否缓存
    hidden = Column(String(1), nullable=False)  # 是否隐藏
    permission = Column(String(100), nullable=False)  # 权限
    create_by = Column(String(100), nullable=True)  # 创建者
    update_by = Column(String(100), nullable=True)  # 修改者
    create_time = Column(TIMESTAMP, nullable=False)  # 创建日期
    update_time = Column(TIMESTAMP, nullable=False)  # 更新日期


class MntDeploy(Base):
    __table__ = "mnt_deploy"


# 部署历史管理
class MntDeployHistory(Base):
    __table__ = "mnt_deploy_history"
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    app_name = Column(String(100), nullable=True)  # 应用名称
    deploy_data = Column(TIMESTAMP, nullable=False)  # 部署日期
    deploy_user = Column(String(100), nullable=True)  # 部署用户
    ip = Column(String(100), nullable=True)  # 部署ip
    deploy_id = Column(Integer, nullable=True)  # 部署编号
