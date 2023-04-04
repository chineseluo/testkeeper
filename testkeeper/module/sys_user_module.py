#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 16:58
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : sys_user_module.py
@IDE     : PyCharm
------------------------------------
"""
import datetime
import time
from testkeeper.ext import db
from loguru import logger
import json
import jsonpickle

NOW_TIME = datetime.datetime.now().replace(microsecond=0)


# NOW_TIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')


# NOW_TIME = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


class BindAttr:
    @staticmethod
    def bind(instance):
        cls = type(instance)
        for name, obj in cls.__dict__.items():
            """ __dict__ 获取这个对象的所有属性"""
            if type(obj) is BindAttr:
                """如果检测到该 instance 中有BoundClass类属性
                    则设置相同的实例属性。
                """
                # 得到类属性的值
                bound_class_obj = getattr(instance, name)
                # 设置实例属性
                setattr(instance, name, bound_class_obj)


# 用户表
class SysUser(db.Model):
    __tablename__ = "sys_user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    nick_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    avatar_name = db.Column(db.String(100), nullable=True)  # 头像地址
    avatar_path = db.Column(db.String(100), nullable=True)  # 头像真实路径
    password = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.String(10), nullable=True)  # 是否是超级管理员
    enabled = db.Column(db.Boolean, nullable=True)  # 启用/禁用
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    pwd_reset_time = db.Column(db.DateTime, nullable=False)  # 修改密码时间
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期
    update_time = db.Column(db.DateTime, nullable=False)  # 更新日期
    jobs = db.relationship("SysJob", backref="sys_users", secondary="sys_user_job")
    roles = db.relationship("SysRole", backref="sys_users", secondary="sys_user_roles")

    @staticmethod
    def init_sys_user():
        admin_user = SysUser(user_id=1, dept_id=2, user_name="admin", nick_name="超级管理员", gender="男",
                             phone="18383388888", email="848257135@qq.com", avatar_name="avatar-20200806032259161.png",
                             avatar_path="avatar-20200806032259161.png", password="123456", is_admin="true",
                             enabled=True, create_by="admin", update_by="admin",
                             pwd_reset_time=NOW_TIME,
                             create_time=NOW_TIME, update_time=NOW_TIME)
        test_user = SysUser(user_id=2, dept_id=2, user_name="test", nick_name="测试", gender="男",
                            phone="18383388888", email="848257135@qq.com", avatar_name="avatar-20200806032259161.png",
                            avatar_path="avatar-20200806032259161.png", password="123456", is_admin="false",
                            enabled=True, create_by="admin", update_by="admin",
                            pwd_reset_time=NOW_TIME,
                            create_time=NOW_TIME, update_time=NOW_TIME)

        db.session.add_all([admin_user, test_user])
        db.session.commit()

    @staticmethod
    def get_key_map():
        map_data = {
            "id": "user_id",
            "dept": "dept_id",
            "username": "user_name",
            "nickName": "nick_name",
            "gender": "gender",
            "phone": "phone",
            "email": "email",
            "avatarName": "avatar_name",
            "avatarPath": "avatar_path",
            "password": "password",
            "isAdmin": "is_admin",
            "enabled": "enabled",
            "createBy": "create_by",
            "updateBy": "update_by",
            "pwdResetTime": "pwd_reset_time",
            "createTime": "create_time",
            "updateTime": "update_time",
            "jobs": "jobs",
            "roles": "roles"
        }
        return map_data

    def to_dict(self):
        roles = [{"dataScope": role.data_scope, "id": role.role_id, "level": role.level, "name": role.name} for role in
                 self.roles]
        jobs = [{"id": job.job_id, "name": job.name} for job in self.jobs]
        sys_dept = SysDept.query.filter_by(dept_id=self.dept_id).first()
        depts = {"id": sys_dept.dept_id, "name": sys_dept.name}
        user_info = {
            "avatarName": self.avatar_name,
            "avatarPath": self.avatar_path,
            "createTime": self.create_time,
            "email": self.email,
            "enabled": self.enabled,
            "gender": self.gender,
            "id": self.user_id,
            "isAdmin": self.is_admin,
            "nickName": self.nick_name,
            "password": self.password,
            "phone": self.phone,
            "pwdResetTime": self.pwd_reset_time,
            "updateBy": self.update_by,
            "updateTime": self.update_time,
            "username": self.user_name,
            "dept": depts,
            "jobs": jobs,
            "roles": roles
        }
        return user_info

    def from_dict(self, data, new_user=False):
        for field in ['dept_id', 'user_name', 'nick_name', 'gender',
                      'phone', 'email', 'avatar_name', 'avatar_path',
                      'is_admin', 'enabled', 'create_by', 'update_by',
                      'pwd_reset_time', 'password', 'create_time', 'update_time']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def __repr__(self):
        return f'<SysUser {self.user_name}>'

    # def __setattr__(self, key, value):
    #     return self[key]=value

    @staticmethod
    def delete_by_user_id(user_id):
        sys_user = SysUser.query.get(user_id)
        if sys_user is None:
            return "500"
        else:
            db.session.delete(sys_user)
            db.session.commit()


class SysUsersJob(db.Model):
    __tablename__ = "sys_user_job"
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.user_id'), primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('sys_job.job_id'), primary_key=True)

    @staticmethod
    def init_sys_users_job():
        user_jobs_first = SysUsersJob(user_id=1, job_id=1)
        user_jobs_second = SysUsersJob(user_id=2, job_id=2)
        db.session.add_all([user_jobs_first, user_jobs_second])
        db.session.commit()


class SysUserRoles(db.Model):
    __tablename__ = "sys_user_roles"
    user_id = db.Column(db.Integer, db.ForeignKey('sys_user.user_id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('sys_role.role_id'), primary_key=True)

    @staticmethod
    def init_sys_user_roles():
        user_roles_first = SysUserRoles(user_id=1, role_id=1)
        user_roles_second = SysUserRoles(user_id=2, role_id=2)
        db.session.add_all([user_roles_first, user_roles_second])
        db.session.commit()


# 部门表
class SysDept(db.Model):
    __tablename__ = "sys_dept"
    dept_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, nullable=True)  # 上级部门Id
    sub_count = db.Column(db.Integer, nullable=False, default=0)  # 子部门数目
    name = db.Column(db.String(100), nullable=False)  # 部门名称
    dept_sort = db.Column(db.Integer, nullable=False, default=999)  # 排序
    enabled = db.Column(db.Boolean, nullable=True)  # 启用/禁用
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期
    update_time = db.Column(db.DateTime, nullable=False)  # 更新日期

    def from_dict(self, data):
        for field in ['dept_id', 'pid', 'sub_count', 'name',
                      'dept_sort', 'enabled', 'create_by', 'update_by',
                      'create_time', 'update_time']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def get_key_map():
        map_data = {
            "id": "dept_id",
            "pid": "pid",
            "subCount": "sub_count",
            "name": "name",
            "deptSort": "dept_sort",
            "enabled": "enabled",
            "createBy": "create_by",
            "updateBy": "update_by",
            "createTime": "create_time",
            "updateTime": "update_time",
        }
        return map_data

    def to_dict(self):
        sys_dept_dict = {
            "id": self.dept_id,
            "subCount": self.sub_count,
            "name": self.name,
            "deptSort": self.dept_sort,
            "enabled": self.enabled,
            "label": self.name,
            "leaf": True if self.sub_count == 0 else False,
            "hasChildren": False if self.sub_count == 0 else True,
            "createBy": self.create_by,
            "updateBy": self.update_by,
            "createTime": self.create_time,
            "updateTime": self.update_time
        }
        return sys_dept_dict

    def __repr__(self):
        return f'<SysDept {self.name}>'

    @staticmethod
    def init_sys_dept_data():
        """
        初始化部门表数据
        :return:
        """
        rd_dept = SysDept(dept_id=1, pid=None, sub_count=0, name="研发部", dept_sort=1, enabled=True, create_by="admin",
                          update_by="admin", create_time=NOW_TIME,
                          update_time=NOW_TIME)
        op_dept = SysDept(dept_id=2, pid=None, sub_count=0, name="运维部", dept_sort=2, enabled=True, create_by="admin",
                          update_by="admin", create_time=NOW_TIME,
                          update_time=NOW_TIME)
        qa_dept = SysDept(dept_id=3, pid=None, sub_count=0, name="测试部", dept_sort=3, enabled=True, create_by="admin",
                          update_by="admin", create_time=NOW_TIME,
                          update_time=NOW_TIME)
        db.session.add_all([rd_dept, op_dept, qa_dept])
        db.session.commit()


class SysDict(db.Model):
    __tablename__ = "sys_dict"
    dict_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)  # 字典名称
    description = db.Column(db.String(255), nullable=False)  # 字典描述
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期
    update_time = db.Column(db.DateTime, nullable=False)  # 更新日期

    @staticmethod
    def init_sys_dict():
        user_status = SysDict(dict_id=1, name="user_status", description="用户状态", create_by="admin",
                              update_by="admin",
                              create_time=NOW_TIME, update_time=NOW_TIME)
        dept_status = SysDict(dict_id=2, name="dept_status", description="部门状态", create_by="admin",
                              update_by="admin",
                              create_time=NOW_TIME, update_time=NOW_TIME)
        job_status = SysDict(dict_id=3, name="job_status", description="岗位状态", create_by="admin", update_by="admin",
                             create_time=NOW_TIME, update_time=NOW_TIME)
        db.session.add_all([user_status, dept_status, job_status])
        db.session.commit()

    @staticmethod
    def get_key_map():
        map_data = {
            "id": "dict_id",
            "name": "name",
            "description": "description",
            "createBy": "create_by",
            "updateBy": "update_by",
            "createTime": "create_time",
            "updateTime": "update_time",
        }
        return map_data

    def from_dict(self, data):
        for field in ['dict_id', 'name', "description",
                      'create_by', 'update_by',
                      'create_time', 'update_time']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        dict_content = {
            "id": self.dict_id,
            "name": self.name,
            "description": self.description,
            "createTime": self.create_time,
            "dictDetails": [sys_dict_detail.to_dict() for sys_dict_detail in
                            SysDictDetail.query.filter_by(dict_id=self.dict_id).all()]
        }
        return dict_content

    def __repr__(self):
        return f'<SysDict {self.name}>'


class SysDictDetail(db.Model):
    __tablename__ = "sys_dict_detail"
    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dict_id = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(255), nullable=True)  # 字典标签
    value = db.Column(db.String(255), nullable=True)  # 字典值
    dict_sort = db.Column(db.Integer, nullable=False)  # 排序
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期
    update_time = db.Column(db.DateTime, nullable=False)  # 更新日期

    @staticmethod
    def init_sys_dict_detail():
        user_status_enable = SysDictDetail(detail_id=1, dict_id=1, label='激活', value='true', dict_sort=1,
                                           create_by="admin",
                                           update_by="admin",
                                           create_time=NOW_TIME, update_time=NOW_TIME)
        user_status_disable = SysDictDetail(detail_id=2, dict_id=1, label='禁用', value='false', dict_sort=2,
                                            create_by="admin",
                                            update_by="admin",
                                            create_time=NOW_TIME, update_time=NOW_TIME)
        dept_status_start = SysDictDetail(detail_id=3, dict_id=2, label='启用', value='true', dict_sort=1,
                                          create_by="admin",
                                          update_by="admin",
                                          create_time=NOW_TIME, update_time=NOW_TIME)
        dept_status_stop = SysDictDetail(detail_id=4, dict_id=2, label='停用', value='false', dict_sort=2,
                                         create_by="admin",
                                         update_by="admin",
                                         create_time=NOW_TIME, update_time=NOW_TIME)
        job_status_start = SysDictDetail(detail_id=5, dict_id=3, label='启用', value='true', dict_sort=1,
                                         create_by="admin",
                                         update_by="admin",
                                         create_time=NOW_TIME, update_time=NOW_TIME)
        job_status_stop = SysDictDetail(detail_id=6, dict_id=3, label='停用', value='false', dict_sort=2,
                                        create_by="admin",
                                        update_by="admin",
                                        create_time=NOW_TIME, update_time=NOW_TIME)
        db.session.add_all(
            [user_status_enable, user_status_disable, dept_status_start, dept_status_stop, job_status_start,
             job_status_stop])
        db.session.commit()

    @staticmethod
    def get_key_map():
        map_data = {
            "id": "detail_id",
            "dictSort": "dict_sort",
            "label": "label",
            "value": "value",
            "dict_id": "dict_id",
            "createBy": "create_by",
            "updateBy": "update_by",
            "createTime": "create_time",
            "updateTime": "update_time",
        }
        return map_data

    def from_dict(self, data):
        for field in ['detail_id', 'dict_id', "label", "value", "dict_sort",
                      'create_by', 'update_by',
                      'create_time', 'update_time']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        dict_detail_content = {
            "createTime": self.create_time,
            "dictSort": self.dict_sort,
            "id": self.detail_id,
            "label": self.label,
            "value": self.value,
            "dict": {
                "id": self.dict_id
            }
        }
        return dict_detail_content

    def __repr__(self):
        return f'<SysDictDetail {self.name}>'


class SysMenu(db.Model):
    __tablename__ = "sys_menu"
    menu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, nullable=True)  # 上级菜单Id
    sub_count = db.Column(db.Integer, nullable=False, default=0)  # 子菜单数目
    type = db.Column(db.Integer, nullable=True)  # 菜单类型
    title = db.Column(db.String(100), nullable=True)  # 菜单标题
    name = db.Column(db.String(100), nullable=True)  # 组件名称
    component = db.Column(db.String(100), nullable=True)  # 组件
    menu_sort = db.Column(db.Integer, nullable=False)  # 排序
    icon = db.Column(db.String(100), nullable=False)  # 图标
    path = db.Column(db.String(100), nullable=False)  # 图标地址
    i_frame = db.Column(db.String(100), nullable=False)  # 是否外链
    cache = db.Column(db.String(100), nullable=False)  # 是否缓存
    hidden = db.Column(db.String(100), nullable=False)  # 是否隐藏
    permission = db.Column(db.String(100), nullable=True)  # 权限
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期
    update_time = db.Column(db.DateTime, nullable=False)  # 更新日期

    @staticmethod
    def init_sys_menu():
        # 系统管理
        sys_manager = SysMenu(menu_id=1, pid=None, sub_count=7, type=0, title="系统管理", name=None, component=None,
                              menu_sort=1, icon="system", path="system", i_frame='0', cache='0', hidden="0",
                              permission=None, create_by="admin",
                              update_by="admin", create_time=NOW_TIME,
                              update_time=NOW_TIME)
        user_manager = SysMenu(menu_id=2, pid=1, sub_count=3, type=1, title="用户管理", name="User",
                               component="system/user/index",
                               menu_sort=2, icon="peoples", path="user", i_frame='0', cache='0', hidden='user:list',
                               permission=None, create_by="admin",
                               update_by="admin", create_time=NOW_TIME,
                               update_time=NOW_TIME)
        button_user_add = SysMenu(menu_id=24, pid=2, sub_count=0, type=2, title="用户新增", name=None,
                                  component="",
                                  menu_sort=2, icon="", path="", i_frame='0', cache='0', hidden='0',
                                  permission="user:add", create_by="admin",
                                  update_by="admin", create_time=NOW_TIME,
                                  update_time=NOW_TIME)
        button_user_update = SysMenu(menu_id=25, pid=2, sub_count=0, type=2, title="用户编辑", name=None,
                                     component="",
                                     menu_sort=3, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="user:edit", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        button_user_delete = SysMenu(menu_id=26, pid=2, sub_count=0, type=2, title="用户删除", name=None,
                                     component="",
                                     menu_sort=4, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="user:del", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)

        role_manager = SysMenu(menu_id=3, pid=1, sub_count=3, type=1, title="角色管理", name="Role",
                               component="system/role/index",
                               menu_sort=3, icon="role", path="role", i_frame='0', cache='0', hidden='roles:list',
                               permission=None, create_by="admin",
                               update_by="admin", create_time=NOW_TIME,
                               update_time=NOW_TIME)
        button_role_add = SysMenu(menu_id=27, pid=3, sub_count=0, type=2, title="角色创建", name=None,
                                  component="",
                                  menu_sort=2, icon="", path="", i_frame='0', cache='0', hidden='0',
                                  permission="roles:add", create_by="admin",
                                  update_by="admin", create_time=NOW_TIME,
                                  update_time=NOW_TIME)
        button_role_update = SysMenu(menu_id=28, pid=3, sub_count=0, type=2, title="角色修改", name=None,
                                     component="",
                                     menu_sort=3, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="roles:edit", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        button_role_delete = SysMenu(menu_id=29, pid=3, sub_count=0, type=2, title="角色删除", name=None,
                                     component="",
                                     menu_sort=4, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="roles:del", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        menu_manager = SysMenu(menu_id=5, pid=1, sub_count=3, type=1, title="菜单管理", name="Menu",
                               component="system/menu/index",
                               menu_sort=5, icon="menu", path="menu", i_frame='0', cache='0', hidden='menu:list',
                               permission=None, create_by="admin",
                               update_by="admin", create_time=NOW_TIME,
                               update_time=NOW_TIME)
        button_menu_add = SysMenu(menu_id=30, pid=5, sub_count=0, type=2, title="菜单新增", name=None,
                                  component="",
                                  menu_sort=2, icon="", path="", i_frame='0', cache='0', hidden='0',
                                  permission="menu:add", create_by="admin",
                                  update_by="admin", create_time=NOW_TIME,
                                  update_time=NOW_TIME)
        button_menu_update = SysMenu(menu_id=31, pid=5, sub_count=0, type=2, title="菜单编辑", name=None,
                                     component="",
                                     menu_sort=3, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="menu:edit", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        button_menu_delete = SysMenu(menu_id=32, pid=5, sub_count=0, type=2, title="菜单删除", name=None,
                                     component="",
                                     menu_sort=4, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="menu:del", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        dept_manager = SysMenu(menu_id=10, pid=1, sub_count=3, type=1, title='部门管理', name='Dept',
                               component='system/dept/index', menu_sort=6, icon='dept', path='dept', i_frame='0',
                               cache='0', hidden='0',
                               permission='dept:list', create_by="admin", update_by="admin", create_time=NOW_TIME,
                               update_time=NOW_TIME)
        button_dept_add = SysMenu(menu_id=33, pid=10, sub_count=0, type=2, title="部门新增", name=None,
                                  component="",
                                  menu_sort=2, icon="", path="", i_frame='0', cache='0', hidden='0',
                                  permission="dept:add", create_by="admin",
                                  update_by="admin", create_time=NOW_TIME,
                                  update_time=NOW_TIME)
        button_dept_update = SysMenu(menu_id=34, pid=10, sub_count=0, type=2, title="部门编辑", name=None,
                                     component="",
                                     menu_sort=3, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="dept:edit", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        button_dept_delete = SysMenu(menu_id=35, pid=10, sub_count=0, type=2, title="部门删除", name=None,
                                     component="",
                                     menu_sort=4, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="dept:del", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        post_manager = SysMenu(menu_id=11, pid=1, sub_count=3, type=1, title='岗位管理', name='Job',
                               component='system/job/index', menu_sort=7, icon='Steve-Jobs', path='job', i_frame='0',
                               cache='0', hidden='0',
                               permission='job:list',
                               create_by="admin", update_by="admin", create_time=NOW_TIME, update_time=NOW_TIME)
        button_post_add = SysMenu(menu_id=36, pid=11, sub_count=0, type=2, title="岗位新增", name=None,
                                  component="",
                                  menu_sort=2, icon="", path="", i_frame='0', cache='0', hidden='0',
                                  permission="job:add", create_by="admin",
                                  update_by="admin", create_time=NOW_TIME,
                                  update_time=NOW_TIME)
        button_post_update = SysMenu(menu_id=37, pid=11, sub_count=0, type=2, title="岗位编辑", name=None,
                                     component="",
                                     menu_sort=3, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="job:edit", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        button_post_delete = SysMenu(menu_id=38, pid=11, sub_count=0, type=2, title="岗位删除", name=None,
                                     component="",
                                     menu_sort=4, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="job:del", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        dict_manager = SysMenu(menu_id=12, pid=1, sub_count=3, type=1, title='字典管理', name='Dict',
                               component='system/dict/index', menu_sort=8, icon='dictionary', path='dict', i_frame='0',
                               cache='0', hidden='0',
                               permission='dict:list',
                               create_by="admin", update_by="admin", create_time=NOW_TIME, update_time=NOW_TIME)
        button_dict_add = SysMenu(menu_id=39, pid=12, sub_count=0, type=2, title="字典新增", name=None,
                                  component="",
                                  menu_sort=2, icon="", path="", i_frame='0', cache='0', hidden='0',
                                  permission="dict:add", create_by="admin",
                                  update_by="admin", create_time=NOW_TIME,
                                  update_time=NOW_TIME)
        button_dict_update = SysMenu(menu_id=40, pid=12, sub_count=0, type=2, title="字典编辑", name=None,
                                     component="",
                                     menu_sort=3, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="dict:edit", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        button_dict_delete = SysMenu(menu_id=41, pid=12, sub_count=0, type=2, title="字典删除", name=None,
                                     component="",
                                     menu_sort=4, icon="", path="", i_frame='0', cache='0', hidden='0',
                                     permission="dict:del", create_by="admin",
                                     update_by="admin", create_time=NOW_TIME,
                                     update_time=NOW_TIME)
        # 系统监控
        sys_monitor = SysMenu(menu_id=6, pid=None, sub_count=5, type=0, title="系统监控", name=None,
                              component=None,
                              menu_sort=10, icon="monitor", path="monitor", i_frame='0', cache='0', hidden='0',
                              permission=None, create_by="admin",
                              update_by="admin", create_time=NOW_TIME,
                              update_time=NOW_TIME)
        op_log = SysMenu(menu_id=7, pid=6, sub_count=0, type=1, title="操作日志", name="Log",
                         component='monitor/log/index', menu_sort=11, icon="log", path="logs", i_frame='0', cache='1',
                         hidden='0', permission=None, create_by="admin",
                         update_by="admin", create_time=NOW_TIME,
                         update_time=NOW_TIME)
        server_monitor = SysMenu(menu_id=8, pid=6, sub_count=0, type=1, title="服务监控", name="ServerMonitor",
                                 component="monitor/server/index", menu_sort=14, icon="codeConsole", path="server",
                                 i_frame='0', cache='0', hidden='0', permission=None, create_by="admin",
                                 update_by="admin", create_time=NOW_TIME,
                                 update_time=NOW_TIME)
        sql_monitor = SysMenu(menu_id=9, pid=6, sub_count=0, type=1, title="SQL监控", name='Sql',
                              component='monitor/sql/index', menu_sort=18, icon="sqlMonitor", path="druid", i_frame='0',
                              cache='0', hidden='0', permission=None, create_by="admin",
                              update_by="admin", create_time=NOW_TIME,
                              update_time=NOW_TIME)

        online_user_monitor = SysMenu(menu_id=13, pid=6, sub_count=0, type=1, title='在线用户', name='OnlineUser',
                                      component='monitor/online/index', menu_sort=10, icon='Steve-Jobs',
                                      path='online', i_frame='0', cache='0', hidden='0',
                                      permission=None, create_by="admin", update_by="admin", create_time=NOW_TIME,
                                      update_time=NOW_TIME)

        # 运维管理
        devops_manager = SysMenu(menu_id=14, pid=None, sub_count=5, type=0, title='运维管理', name='Mnt', component='',
                                 menu_sort=20, icon='mnt', path='mnt', i_frame='0', cache='0', hidden='0',
                                 permission=None, create_by="admin",
                                 update_by="admin",
                                 create_time=NOW_TIME, update_time=NOW_TIME)

        machine_manager = SysMenu(menu_id=15, pid=14, sub_count=3, type=1, title='服务器', name='ServerDeploy',
                                  component='mnt/server/index', menu_sort=22, icon='server',
                                  path='mnt/serverDeploy', i_frame='0', cache='0',
                                  hidden='0', permission='serverDeploy:list', create_by="admin", update_by="admin",
                                  create_time=NOW_TIME,
                                  update_time=NOW_TIME)

        app_manager = SysMenu(menu_id=16, pid=14, sub_count=3, type=1, title='应用管理', name='App',
                              component='mnt/app/index', menu_sort=23, icon='app', path='mnt/app', cache='0',
                              hidden='0', i_frame='0',
                              permission='app:list', create_by="admin",
                              update_by="admin", create_time=NOW_TIME, update_time=NOW_TIME)

        deploy_manager = SysMenu(menu_id=17, pid=14, sub_count=3, type=1, title='部署管理', name='Deploy',
                                 component='mnt/deploy/index', menu_sort=24, icon='deploy', path='mnt/deploy',
                                 cache='0',
                                 i_frame='0', hidden='0',
                                 permission='deploy:list', create_by="admin", update_by="admin", create_time=NOW_TIME,
                                 update_time=NOW_TIME)

        deploy_backup = SysMenu(menu_id=18, pid=14, sub_count=1, type=1, title='部署备份', name='DeployHistory',
                                component='mnt/deployHistory/index', menu_sort=25, icon='backup',
                                path='mnt/deployHistory',
                                cache='0', i_frame='0', hidden='0', permission='deployHistory:list', create_by="admin",
                                update_by="admin", create_time=NOW_TIME,
                                update_time=NOW_TIME)

        db_manager = SysMenu(menu_id=19, pid=14, sub_count=3, type=1, title='数据库管理', name='Database',
                             component='mnt/database/index', menu_sort=26, icon='database', path='mnt/database',
                             cache='0', i_frame='0',
                             hidden='0', permission='database:list', create_by="admin", update_by="admin",
                             create_time=NOW_TIME, update_time=NOW_TIME)

        # 测试任务管理
        task_manager = SysMenu(menu_id=20, pid=None, sub_count=3, type=0, title='任务管理', name=None, component='',
                               menu_sort=900, icon='menu', path='nested', cache='0', i_frame='0', hidden='0',
                               permission=None, create_by='admin',
                               update_by='admin',
                               create_time=NOW_TIME, update_time=NOW_TIME)

        plan_manager = SysMenu(menu_id=21, pid=20, sub_count=0, type=1, title='计划列表', name=None, component='',
                               menu_sort=999, icon='menu', path='menu1', cache='0', i_frame='0', hidden='0',
                               permission=None, create_by='admin',
                               update_by='admin',
                               create_time=NOW_TIME, update_time=NOW_TIME)

        job_manager = SysMenu(menu_id=22, pid=20, sub_count=0, type=1, title='任务列表', name=None,
                              component='nested/menu2/index', menu_sort=999, icon='menu', path='menu2', cache='0',
                              i_frame='0', hidden='0',
                              permission=None, create_by='admin',
                              update_by='admin', create_time=NOW_TIME, update_time=NOW_TIME)

        execute_manager = SysMenu(menu_id=23, pid=20, sub_count=0, type=1, title='执行列表', name=None,
                                  component='nested/menu2/index', menu_sort=999, icon='menu', path='menu2', cache='0',
                                  i_frame='0', hidden='0',
                                  permission=None, create_by='admin',
                                  update_by='admin', create_time=NOW_TIME, update_time=NOW_TIME)

        #
        # components_manager = SysMenu(menu_id=10, pid=None, sub_count=5, type=0, title="组件管理", name=None,
        #                              component=None, menu_sort=50, icon="zujian", path="components",
        #                              i_frame='0',
        #                              cache='0', hidden='0', permission=None)

        db.session.add_all(
            [sys_manager, user_manager, role_manager, menu_manager, sys_monitor, op_log, server_monitor, sql_monitor,
             dept_manager, post_manager, dict_manager, online_user_monitor, devops_manager, machine_manager,
             app_manager,
             deploy_manager, deploy_backup, db_manager, task_manager, plan_manager, execute_manager, job_manager])
        db.session.commit()

    def to_dict(self):
        menu_info = {
            "id": self.menu_id,
            "cache": False if self.cache == "0" else True,
            "component": self.component,
            "componentName": self.name,
            "hasChildren": False if self.sub_count == 0 else True,
            "hidden": False if self.hidden == "0" else True,
            "iFrame": False if self.i_frame == "0" else True,
            "icon": self.icon,
            "label": self.title,
            "leaf": True if self.sub_count == 0 else False,
            "menuSort": self.menu_sort,
            "path": self.path,
            "permission": self.permission,
            "pid": self.pid,
            "subCount": self.sub_count,
            "title": self.title,
            "type": self.type,
            "createBy": self.create_by,
            "createTime": self.create_time,
            "updateBy": self.update_by,
            "updateTime": self.update_time
        }
        return menu_info

    def __repr__(self):
        return f'<SysMenu {self.name}>'


class SysJob(db.Model):
    __tablename__ = "sys_job"
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)  # 岗位名称
    enabled = db.Column(db.Boolean, nullable=True)  # 启用/禁用
    job_sort = db.Column(db.Integer, nullable=False)  # 排序
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期
    update_time = db.Column(db.DateTime, nullable=False)  # 更新日期

    @staticmethod
    def get_key_map():
        map_data = {
            "id": "job_id",
            "name": "name",
            "jobSort": "job_sort",
            "enabled": "enabled",
            "createBy": "create_by",
            "updateBy": "update_by",
            "createTime": "create_time",
            "updateTime": "update_time",
        }
        return map_data

    def from_dict(self, data):
        for field in ['job_id', 'name', 'job_sort', 'enabled',
                      'create_by', 'update_by',
                      'create_time', 'update_time']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def init_sys_job():
        qa_job = SysJob(job_id=1, name="测试", enabled=True, job_sort=1, create_by="admin",
                        update_by="admin", create_time=NOW_TIME,
                        update_time=NOW_TIME)
        op_job = SysJob(job_id=2, name="运维", enabled=True, job_sort=2, create_by="admin",
                        update_by="admin", create_time=NOW_TIME,
                        update_time=NOW_TIME)
        rd_job = SysJob(job_id=3, name="开发", enabled=True, job_sort=3, create_by="admin",
                        update_by="admin", create_time=NOW_TIME,
                        update_time=NOW_TIME)

        db.session.add_all([qa_job, op_job, rd_job])
        db.session.commit()

    def to_dict(self):
        job_info = {
            "id": self.job_id,
            "name": self.name,
            "enabled": self.enabled,
            "jobSort": self.job_sort,
            "createBy": self.create_by,
            "createTime": self.create_time,
            "updateBy": self.update_by,
            "updateTime": self.update_time
        }
        return job_info

    def __repr__(self):
        return f'<SysJob {self.name}>'


class MntDeploy(db.Model):
    __tablename__ = "mnt_deploy"
    deploy_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_id = db.Column(db.Integer, nullable=False)  # 应用编号
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期
    update_time = db.Column(db.DateTime, nullable=False)  # 更新日期


# 部署历史管理
class MntDeployHistory(db.Model):
    __tablename__ = "mnt_deploy_history"
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_name = db.Column(db.String(100), nullable=True)  # 应用名称
    deploy_date = db.Column(db.DateTime, nullable=False)  # 部署日期
    deploy_user = db.Column(db.String(100), nullable=True)  # 部署用户
    ip = db.Column(db.String(200), nullable=True)  # 部署ip
    deploy_id = db.Column(db.Integer, nullable=True)  # 部署编号


class SysRole(db.Model):
    __tablename__ = "sys_role"
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)  # 角色名称
    level = db.Column(db.Integer, nullable=False)  # 角色级别
    description = db.Column(db.String(255), nullable=True)  # 角色描述
    data_scope = db.Column(db.String(255), nullable=True)  # 数据权限
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期
    update_time = db.Column(db.DateTime, nullable=False)  # 更新日期
    menus = db.relationship("SysMenu", backref="roles", secondary="sys_role_menu")

    @staticmethod
    def get_key_map():
        map_data = {
            "id": "role_id",
            "name": "name",
            "level": "level",
            "dataScope": "data_scope",
            "description": "description",
            "menus": "menus",
            "depts": "depts",
            "createBy": "create_by",
            "updateBy": "update_by",
            "createTime": "create_time",
            "updateTime": "update_time",
        }
        return map_data

    def from_dict(self, data):
        for field in ['role_id', 'name', 'level', 'description', 'data_scope', 'menus',
                      'create_by', 'update_by',
                      'create_time', 'update_time']:
            if field in data:
                if field == "menus" and data['menus'] is None:
                    setattr(self, field, [])
                else:
                    setattr(self, field, data[field])

    @staticmethod
    def init_sys_role():
        # 超级管理员
        admin_role = SysRole(role_id=1, name='超级管理员', level=1, description='超级管理员', data_scope="全部",
                             create_by="admin",
                             update_by="admin",
                             create_time=NOW_TIME, update_time=NOW_TIME)
        # 普通用户
        ordinary_role = SysRole(role_id=2, name='普通用户', level=2, description='普通用户', data_scope="本级",
                                create_by="admin",
                                update_by="admin",
                                create_time=NOW_TIME, update_time=NOW_TIME)
        db.session.add_all([admin_role, ordinary_role])
        db.session.commit()

    def to_dict(self):
        menus = [menu.__repr__() for menu in self.menus]
        role_info = {
            "id": self.role_id,
            "name": self.name,
            "level": self.level,
            "description": self.description,
            "depts": [],
            "menus": menus,
            "dataScope": self.data_scope,
            "createBy": self.create_by,
            "createTime": self.create_time,
            "updateBy": self.update_by,
            "updateTime": self.update_time
        }
        return role_info

    def __repr__(self):
        return f'<SysRole {self.name}>'


class SysRoleDepts(db.Model):
    # 角色部门关联
    __tablename__ = "sys_roles_depts"
    role_id = db.Column(db.Integer, db.ForeignKey('sys_role.role_id'), primary_key=True)  # 角色Id
    dept_id = db.Column(db.Integer, db.ForeignKey('sys_dept.dept_id'), primary_key=True)  # 菜单Id


class MntServer(db.Model):
    __tablename__ = "mnt_server"
    server_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(100), nullable=False)  # 账号
    ip = db.Column(db.String(100), nullable=False)  # ip地址
    name = db.Column(db.String(100), nullable=False)  # 名称
    password = db.Column(db.String(100), nullable=True)  # 密码
    port = db.Column(db.Integer, nullable=False)  # 端口
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.DateTime, nullable=False)  # 创建日期
    update_time = db.Column(db.DateTime, nullable=False)  # 更新日期

    def from_dict(self, data):
        for field in ['server_id', 'account', 'ip', 'name',
                      'password', 'port', 'create_by', 'update_by',
                      'create_time', 'update_time']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def get_key_map():
        map_data = {
            "id": "server_id",
            "account": "account",
            "ip": "ip",
            "name": "name",
            "port": "port",
            "password": "password",
            "createBy": "create_by",
            "updateBy": "update_by",
            "createTime": "create_time",
            "updateTime": "update_time",
        }
        return map_data

    def to_dict(self):
        role_info = {
            "id": self.server_id,
            "account": self.account,
            "ip": self.ip,
            "name": self.name,
            "port": self.port,
            "password": self.password,
            "createBy": self.create_by,
            "createTime": self.create_time,
            "updateBy": self.update_by,
            "updateTime": self.update_time
        }
        return role_info

    def __repr__(self):
        return f'<MntServer {self.name}>'


class SysRoleMenus(db.Model):
    __tablename__ = "sys_role_menu"
    menu_id = db.Column(db.Integer, db.ForeignKey('sys_menu.menu_id'), primary_key=True)  # 菜单Id
    role_id = db.Column(db.Integer, db.ForeignKey('sys_role.role_id'), primary_key=True)  # 角色Id

    @staticmethod
    def init_sys_role_menus():
        menu_role_1 = SysRoleMenus(menu_id=1, role_id=1)
        menu_role_2 = SysRoleMenus(menu_id=2, role_id=1)
        menu_role_3 = SysRoleMenus(menu_id=3, role_id=1)
        menu_role_4 = SysRoleMenus(menu_id=4, role_id=1)
        menu_role_5 = SysRoleMenus(menu_id=5, role_id=1)
        menu_role_6 = SysRoleMenus(menu_id=6, role_id=1)
        menu_role_7 = SysRoleMenus(menu_id=7, role_id=1)
        menu_role_8 = SysRoleMenus(menu_id=8, role_id=1)
        menu_role_9 = SysRoleMenus(menu_id=9, role_id=1)
        menu_role_10 = SysRoleMenus(menu_id=10, role_id=1)
        menu_role_11 = SysRoleMenus(menu_id=11, role_id=1)
        menu_role_12 = SysRoleMenus(menu_id=12, role_id=1)
        menu_role_13 = SysRoleMenus(menu_id=13, role_id=1)
        menu_role_14 = SysRoleMenus(menu_id=14, role_id=1)
        menu_role_15 = SysRoleMenus(menu_id=15, role_id=1)
        menu_role_16 = SysRoleMenus(menu_id=16, role_id=1)
        menu_role_17 = SysRoleMenus(menu_id=17, role_id=1)
        menu_role_18 = SysRoleMenus(menu_id=18, role_id=1)
        menu_role_19 = SysRoleMenus(menu_id=19, role_id=1)
        menu_role_20 = SysRoleMenus(menu_id=20, role_id=1)
        menu_role_21 = SysRoleMenus(menu_id=21, role_id=1)
        menu_role_22 = SysRoleMenus(menu_id=22, role_id=1)
        menu_role_23 = SysRoleMenus(menu_id=23, role_id=1)
        menu_role_second = SysRoleMenus(menu_id=2, role_id=2)
        db.session.add_all(
            [menu_role_1, menu_role_2, menu_role_3, menu_role_4, menu_role_5, menu_role_6, menu_role_7, menu_role_8,
             menu_role_9, menu_role_10, menu_role_11, menu_role_12, menu_role_13, menu_role_14, menu_role_15,
             menu_role_16, menu_role_17, menu_role_18, menu_role_19, menu_role_20, menu_role_21,
             menu_role_22, menu_role_23,
             menu_role_second])
        db.session.commit()


def init_data():
    SysRoleMenus().init_sys_role_menus()
    SysRole().init_sys_role()
    SysJob().init_sys_job()
    SysMenu().init_sys_menu()
    SysDict().init_sys_dict()
    SysDept().init_sys_dept_data()
    SysUser().init_sys_user()
    SysUsersJob().init_sys_users_job()
    SysUserRoles().init_sys_user_roles()
    SysDictDetail().init_sys_dict_detail()


if __name__ == '__main__':
    init_data()