#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:11
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : views.py
@IDE     : PyCharm
------------------------------------
"""
from testkeeper.webapi.menu import menu_blue
from loguru import logger
from testkeeper.module.sys_user_module import SysMenu, SysUser
from flask import Flask, jsonify, render_template, request, make_response, session


@menu_blue.route("/build", methods=["GET"])
def build():
    logger.info("##########")
    menu_list = []
    children = {
        "alwaysShow": True,
        "children": []
    }
    # 获取用户
    user_id = session.get('user_id')
    logger.info(f'user_id:{user_id}')
    user = SysUser.query.filter_by(user_id=user_id).first()

    # 获取用户的角色
    real_meun_list = []
    for role in user.roles:
        for menu in role.menus:
            # 先查出根菜单
            # 再查出子菜单
            if not menu.pid:
                root_menu = {
                    "alwaysShow": True,
                    "component": "Layout",
                    "hidden": False,
                    "meta": {
                        "icon": menu.icon,
                        "noCache": True if menu.cache == "0" else False,
                        "title": menu.title
                    },
                    "name": menu.title,
                    "path": f'/{menu.path}',
                    "redirect": "noredirect",
                    "children": []
                }
                for other_meun in role.menus:
                    if other_meun.pid == menu.menu_id:
                        children_menu = {
                            "component": other_meun.component,
                            "hidden": False,
                            "meta": {
                                "icon": other_meun.icon,
                                "noCache": True if other_meun.cache == "0" else False,
                                "title": other_meun.title
                            },
                            "name": other_meun.name,
                            "path": other_meun.path
                        }
                        root_menu['children'].append(children_menu)
                real_meun_list.append(root_menu)

    # 更具角色获取用户具有哪些菜单权限
    logger.info(real_meun_list)
    return real_meun_list
