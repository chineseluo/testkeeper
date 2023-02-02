#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:48
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : test_plan_config_cmd.py
@IDE     : PyCharm
------------------------------------
"""
import sys
import os
import unittest
from ddt import ddt, data
from loguru import logger
from testkeeper.client import entry
from testkeeper.mock.mock import MockData
from testkeeper.service.plan_service import PlanService
from testkeeper.service.plan_status_service import PlanStatusService


@ddt
class TestPlanConfigCmd(unittest.TestCase):
    def setUp(self):
        # 初始化mock数据
        logger.info("开始初始化sqlite mock测试数据......")
        db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))),
                               "testkeeper/db")
        db_name = "testkeeper.db"
        md = MockData(db_path, db_name)
        md.insertTestJobTableData(2, 3, 3, 2)
        logger.info("初始化sqlite mock测试数据结束......")

    def tearDown(self):
        # 清理mock数据
        logger.info("开始清理sqlite mock测试数据......")
        plan_service = PlanService()
        plan_service.limit = 100
        plan_service.project_name = "测试项目21"
        plan_list = plan_service.get_test_plan_list()
        for plan in plan_list:
            sys.argv = ["Tk", "plan_delete", "-plan_id", str(plan['planId'])]
            with self.assertRaises(SystemExit) as cm:
                entry()
            self.assertEqual(cm.exception.code, 0)
        logger.info("清理sqlite mock测试数据结束......")

    def test_show_test_plan_config(self):
        # 测试 TK plan_show
        sys.argv = ["Tk", "plan_show"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_show_test_plan_config_by_project_name(self):
        # 测试 TK plan_show -project_name xxx
        plan_service = PlanService()
        plan_service.limit = 100
        plan_service.project_name = "测试项目21"
        project_name = plan_service.get_test_plan_list()[0]["projectName"]
        sys.argv = ["Tk", "plan_show", "-project_name", str(project_name)]
        with self.assertRaises(SystemExit) as cm:
            entry()
        sys.argv = ["Tk", "plan_show", "-p", str(project_name)]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_show_test_plan_config_by_project_name_exception(self):
        # 测试 TK plan_show -project_name xxx
        # project_name 参数传递异常情况
        sys.argv = ["Tk", "plan_show", "-project_name", "不存在的项目名称"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_show_test_plan_config_by_project_name_and_limit(self):
        # 测试 TK plan_show -project_name xxx -limit xxx
        plan_service = PlanService()
        project_name = plan_service.get_test_plan_list("测试项目21", 100)[0]["projectName"]
        sys.argv = ["Tk", "plan_show", "-project_name", str(project_name), "-limit", "2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        sys.argv = ["Tk", "plan_show", "-p", str(project_name), "-l", "2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_show_test_plan_config_by_project_name_and_limit_exception(self):
        # 测试 TK plan_show -project_name xxx -limit xxx
        # limit参数异常情况
        plan_service = PlanService()
        project_name = plan_service.get_test_plan_list("测试项目21", 100)[0]["projectName"]
        sys.argv = ["Tk", "plan_show", "-project_name", str(project_name), "-limit", "cc"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        sys.argv = ["Tk", "plan_show", "-p", str(project_name), "-l", "-1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)
