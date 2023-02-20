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
from testkeeper.ext import db
from loguru import logger
import json


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
    enable = db.Column(db.String(10), nullable=True)  # 启用/禁用
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    pwd_reset_time = db.Column(db.TIMESTAMP, nullable=False)  # 修改密码时间
    create_time = db.Column(db.TIMESTAMP, nullable=False)  # 创建日期
    update_time = db.Column(db.TIMESTAMP, nullable=False)  # 更新日期
    jobs = db.relationship("SysJob", backref="sys_users", secondary="sys_user_job")
    roles = db.relationship("SysRole", backref="sys_users", secondary="sys_user_roles")

    @staticmethod
    def init_sys_user():
        admin_user = SysUser(user_id=1, dept_id=2, user_name="admin", nick_name="超级管理员", gender="男",
                             phone="admin_phone", email="848257135@qq.com", avatar_name="avatar-20200806032259161.png",
                             avatar_path="avatar-20200806032259161.png", password="123456", is_admin="true",
                             enable="true", create_by="admin", update_by="admin",
                             pwd_reset_time=datetime.datetime.now(),
                             create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        test_user = SysUser(user_id=2, dept_id=2, user_name="test", nick_name="测试", gender="男",
                            phone="test_phone", email="848257135@qq.com", avatar_name="avatar-20200806032259161.png",
                            avatar_path="avatar-20200806032259161.png", password="123456", is_admin="false",
                            enable="true", create_by="admin", update_by="admin",
                            pwd_reset_time=datetime.datetime.now(),
                            create_time=datetime.datetime.now(), update_time=datetime.datetime.now())

        db.session.add_all([admin_user, test_user])
        db.session.commit()

    def __str__(self):
        roles = [{"dataScope": role.data_scope, "id": role.role_id, "level": role.level, "name": role.name} for role in
                 self.roles]
        jobs = [{"id": job.job_id, "name": job.name} for job in self.jobs]

        depts = [{"id": dept.dept_id, "name": dept.name} for dept in
                 SysDept.query.filter_by(dept_id=self.dept_id).all()]
        user_info = {
            "avatarName": self.avatar_name,
            "avatarPath": self.avatar_path,
            "createTime": self.create_time,
            "email": self.email,
            "enable": self.enable,
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

    def __repr__(self):
        return self.__str__()

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
    sub_count = db.Column(db.Integer, nullable=False)  # 子部门数目
    name = db.Column(db.String(100), nullable=False)  # 部门名称
    dept_sort = db.Column(db.Integer, nullable=False)  # 排序
    enable = db.Column(db.Boolean, nullable=True)  # 启用/禁用
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.TIMESTAMP, nullable=False)  # 创建日期
    update_time = db.Column(db.TIMESTAMP, nullable=False)  # 更新日期

    def __repr__(self):
        sys_dept_dict = {
            "id": self.dept_id,
            "subCount": self.sub_count,
            "name": self.name,
            "deptSort": self.dept_sort,
            "enable": self.enable,
            "label": self.name,
            "leaf": True,
            "hasChildren": False if self.sub_count == 0 else True,
            "createBy": self.create_by,
            "updateBy": self.update_by,
            "createTime": self.create_time,
            "updateTime": self.update_time
        }
        return sys_dept_dict

    @staticmethod
    def init_sys_dept_data():
        """
        初始化部门表数据
        :return:
        """
        rd_dept = SysDept(dept_id=1, pid=None, sub_count=0, name="研发部", dept_sort=1, enable=True, create_by="admin",
                          update_by="admin", create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        op_dept = SysDept(dept_id=2, pid=None, sub_count=0, name="运维部", dept_sort=2, enable=True, create_by="admin",
                          update_by="admin", create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        qa_dept = SysDept(dept_id=3, pid=None, sub_count=0, name="测试部", dept_sort=3, enable=True, create_by="admin",
                          update_by="admin", create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        db.session.add_all([rd_dept, op_dept, qa_dept])
        db.session.commit()


class SysDict(db.Model):
    __tablename__ = "sys_dict"
    dict_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)  # 字典名称
    description = db.Column(db.String(255), nullable=False)  # 字典描述
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.TIMESTAMP, nullable=False)  # 创建日期
    update_time = db.Column(db.TIMESTAMP, nullable=False)  # 更新日期

    @staticmethod
    def init_sys_dict():
        user_status = SysDict(dict_id=1, name="user_status", description="用户状态", create_by="admin", update_by="admin",
                              create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        dept_status = SysDict(dict_id=4, name="dept_status", description="部门状态", create_by="admin", update_by="admin",
                              create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        job_status = SysDict(dict_id=5, name="job_status", description="岗位状态", create_by="admin", update_by="admin",
                             create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        db.session.add_all([user_status, dept_status, job_status])
        db.session.commit()


class SysDictDetail(db.Model):
    __tablename__ = "sys_dict_detail"
    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dict_id = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(255), nullable=True)  # 字典标签
    value = db.Column(db.String(255), nullable=True)  # 字典值
    dict_sort = db.Column(db.Integer, nullable=False)  # 排序
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.TIMESTAMP, nullable=False)  # 创建日期
    update_time = db.Column(db.TIMESTAMP, nullable=False)  # 更新日期

    @staticmethod
    def init_sys_dict_detail():
        enable = SysDictDetail(detail_id=1, dict_id=1, label='激活', value='true', dict_sort=1, create_by="admin",
                               update_by="admin",
                               create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        disable = SysDictDetail(detail_id=2, dict_id=1, label='禁用', value='false', dict_sort=2, create_by="admin",
                                update_by="admin",
                                create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        start = SysDictDetail(detail_id=3, dict_id=4, label='启用', value='true', dict_sort=1, create_by="admin",
                              update_by="admin",
                              create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        stop = SysDictDetail(detail_id=4, dict_id=4, label='停用', value='false', dict_sort=2, create_by="admin",
                             update_by="admin",
                             create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        db.session.add_all([enable, disable, start, stop])
        db.session.commit()


class SysMenu(db.Model):
    __tablename__ = "sys_menu"
    menu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, nullable=True)  # 上级菜单Id
    sub_count = db.Column(db.Integer, nullable=False)  # 子菜单数目
    type = db.Column(db.Integer, nullable=True)  # 菜单类型
    title = db.Column(db.String(100), nullable=True)  # 菜单标题
    name = db.Column(db.String(100), nullable=True)  # 组件名称
    component = db.Column(db.String(100), nullable=True)  # 组件
    menu_sort = db.Column(db.Integer, nullable=False)  # 排序
    icon = db.Column(db.String(100), nullable=False)  # 图标
    path = db.Column(db.String(100), nullable=False)  # 图标地址
    i_frame = db.Column(db.String(1), nullable=False)  # 是否外链
    cache = db.Column(db.String(100), nullable=False)  # 是否缓存
    hidden = db.Column(db.String(100), nullable=False)  # 是否隐藏
    permission = db.Column(db.String(100), nullable=True)  # 权限
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.TIMESTAMP, nullable=False)  # 创建日期
    update_time = db.Column(db.TIMESTAMP, nullable=False)  # 更新日期

    @staticmethod
    def init_sys_menu():
        sys_manager = SysMenu(menu_id=1, pid=None, sub_count=7, type=0, title="系统管理", name=None, component=None,
                              menu_sort=1, icon="system", path="system", i_frame='0', cache='0', hidden="0",
                              permission=None, create_by="admin",
                              update_by="admin", create_time=datetime.datetime.now(),
                              update_time=datetime.datetime.now())
        user_manager = SysMenu(menu_id=2, pid=1, sub_count=3, type=1, title="用户管理", name="User",
                               component="system/user/index",
                               menu_sort=2, icon="peoples", path="user", i_frame='0', cache='0', hidden='user:list',
                               permission=None, create_by="admin",
                               update_by="admin", create_time=datetime.datetime.now(),
                               update_time=datetime.datetime.now())
        role_manager = SysMenu(menu_id=3, pid=1, sub_count=3, type=1, title="角色管理", name="Role",
                               component="system/role/index",
                               menu_sort=3, icon="role", path="role", i_frame='0', cache='0', hidden='roles:list',
                               permission=None, create_by="admin",
                               update_by="admin", create_time=datetime.datetime.now(),
                               update_time=datetime.datetime.now())
        menu_manager = SysMenu(menu_id=5, pid=1, sub_count=3, type=1, title="菜单管理", name="Menu",
                               component="system/menu/index",
                               menu_sort=5, icon="menu", path="menu", i_frame='0', cache='0', hidden='menu:list',
                               permission=None, create_by="admin",
                               update_by="admin", create_time=datetime.datetime.now(),
                               update_time=datetime.datetime.now())

        sys_monitor = SysMenu(menu_id=6, pid=None, sub_count=5, type=0, title="系统监控", name=None,
                              component=None,
                              menu_sort=10, icon="monitor", path="monitor", i_frame='0', cache='0', hidden='0',
                              permission=None, create_by="admin",
                              update_by="admin", create_time=datetime.datetime.now(),
                              update_time=datetime.datetime.now())
        op_log = SysMenu(menu_id=7, pid=6, sub_count=0, type=1, title="操作日志", name="Log",
                         component='monitor/log/index', menu_sort=11, icon="log", path="logs", i_frame='0', cache='1',
                         hidden='0', permission=None, create_by="admin",
                         update_by="admin", create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        server_monitor = SysMenu(menu_id=8, pid=6, sub_count=0, type=1, title="服务监控", name="ServerMonitor",
                                 component="monitor/server/index", menu_sort=14, icon="codeConsole", path="server",
                                 i_frame='0', cache='0', hidden='0', permission=None, create_by="admin",
                                 update_by="admin", create_time=datetime.datetime.now(),
                                 update_time=datetime.datetime.now())
        sql_monitor = SysMenu(menu_id=9, pid=6, sub_count=0, type=1, title="SQL监控", name='Sql',
                              component='monitor/sql/index', menu_sort=18, icon="sqlMonitor", path="druid", i_frame='0',
                              cache='0', hidden='0', permission=None, create_by="admin",
                              update_by="admin", create_time=datetime.datetime.now(),
                              update_time=datetime.datetime.now())

        #
        # components_manager = SysMenu(menu_id=10, pid=None, sub_count=5, type=0, title="组件管理", name=None,
        #                              component=None, menu_sort=50, icon="zujian", path="components",
        #                              i_frame='0',
        #                              cache='0', hidden='0', permission=None)

        db.session.add_all(
            [sys_manager, user_manager, role_manager, menu_manager, sys_monitor, op_log, server_monitor, sql_monitor])
        db.session.commit()

    def __str__(self):
        menu_info = {
            "id": self.menu_id,
            "cache": self.cache,
            "component": self.component,
            "componentName": self.name,
            "hasChildren": False,
            "hidden": self.hidden,
            "iFrame": self.i_frame,
            "icon": self.icon,
            "lable": self.name,
            "leaf": False,
            "menuSort": self.menu_sort,
            "path": self.path,
            "permission": self.permission,
            "pid": self.pid,
            "subCount": self.sub_count,
            "title": self.name,
            "type": self.type,
            "createBy": self.create_by,
            "createTime": self.create_time,
            "updateBy": self.update_by,
            "updateTime": self.update_time
        }
        return menu_info

    def __repr__(self):
        return self.__str__()


class SysJob(db.Model):
    __tablename__ = "sys_job"
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)  # 岗位名称
    enable = db.Column(db.Boolean, nullable=True)  # 启用/禁用
    job_sort = db.Column(db.Integer, nullable=False)  # 排序
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.TIMESTAMP, nullable=False)  # 创建日期
    update_time = db.Column(db.TIMESTAMP, nullable=False)  # 更新日期

    @staticmethod
    def init_sys_job():
        qa_job = SysJob(job_id=1, name="测试", enable=True, job_sort=1, create_by="admin",
                        update_by="admin", create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        op_job = SysJob(job_id=2, name="运维", enable=True, job_sort=2, create_by="admin",
                        update_by="admin", create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        rd_job = SysJob(job_id=3, name="开发", enable=True, job_sort=3, create_by="admin",
                        update_by="admin", create_time=datetime.datetime.now(), update_time=datetime.datetime.now())

        db.session.add_all([qa_job, op_job, rd_job])
        db.session.commit()

    def __str__(self):
        job_info = {
            "id": self.job_id,
            "name": self.name,
            "enable": self.enable,
            "jobSort": self.job_sort,
            "createBy": self.create_by,
            "createTime": self.create_time,
            "updateBy": self.update_by,
            "updateTime": self.update_time
        }
        return job_info

    def __repr__(self):
        return self.__str__()


class MntDeploy(db.Model):
    __tablename__ = "mnt_deploy"
    deploy_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_id = db.Column(db.Integer, nullable=False)  # 应用编号
    create_by = db.Column(db.String(100), nullable=True)  # 创建者
    update_by = db.Column(db.String(100), nullable=True)  # 修改者
    create_time = db.Column(db.TIMESTAMP, nullable=False)  # 创建日期
    update_time = db.Column(db.TIMESTAMP, nullable=False)  # 更新日期


# 部署历史管理
class MntDeployHistory(db.Model):
    __tablename__ = "mnt_deploy_history"
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_name = db.Column(db.String(100), nullable=True)  # 应用名称
    deploy_data = db.Column(db.TIMESTAMP, nullable=False)  # 部署日期
    deploy_user = db.Column(db.String(100), nullable=True)  # 部署用户
    ip = db.Column(db.String(100), nullable=True)  # 部署ip
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
    create_time = db.Column(db.TIMESTAMP, nullable=False)  # 创建日期
    update_time = db.Column(db.TIMESTAMP, nullable=False)  # 更新日期
    menus = db.relationship("SysMenu", backref="roles", secondary="sys_role_menu")

    @staticmethod
    def init_sys_role():
        # 超级管理员
        admin_role = SysRole(role_id=1, name='超级管理员', level=1, description='超级管理员', data_scope="全部", create_by="admin",
                             update_by="admin",
                             create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        # 普通用户
        ordinary_role = SysRole(role_id=2, name='普通用户', level=2, description='普通用户', data_scope="本级",
                                create_by="admin",
                                update_by="admin",
                                create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
        db.session.add_all([admin_role, ordinary_role])
        db.session.commit()

    def __str__(self):
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
        return self.__str__()


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
        menu_role_second = SysRoleMenus(menu_id=2, role_id=2)
        db.session.add_all(
            [menu_role_1, menu_role_2, menu_role_3, menu_role_4, menu_role_5, menu_role_6, menu_role_7, menu_role_8,
             menu_role_9,
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
