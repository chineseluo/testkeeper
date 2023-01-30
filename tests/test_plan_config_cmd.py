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


@ddt
class TestPlanConfigCmd(unittest.TestCase):
    def setUp(self):
        # 初始化mock数据
        logger.info("开始初始化sqlite mock测试数据......")
        db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "testkeeper/db")
        logger.info(db_path)
        db_name = "testkeeper.db"
        md = MockData(db_path, db_name)
        md.insertTestJobTableData(2, 3, 3, 2)
        logger.info("初始化sqlite mock测试数据结束......")

    def tearDown(self):
        # 清理mock数据
        logger.info("开始清理sqlite mock测试数据......")
        sys.argv = ["Tk", "plan_delete", "-plan_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)
        sys.argv = ["Tk", "plan_status_delete", "-plan_status_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)
        logger.info("清理sqlite mock测试数据结束......")

    def test_show_test_plan_config(self):
        sys.argv = ["Tk", "plan_show"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)
