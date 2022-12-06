#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 22:43
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : test_cmd.py
@IDE     : PyCharm
------------------------------------
"""
import sys
import os
import unittest
from ddt import ddt, data
from testkeeper.client import entry


@ddt
class TestCmd(unittest.TestCase):
    def test_show_version(self):
        sys.argv = ["Tk", "-V"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_load_help(self):
        sys.argv = ["Tk", "plan_load", "-h"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show_help(self):
        sys.argv = ["Tk", "plan_show", "-h"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show_all(self):
        sys.argv = ["Tk", "plan_show"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show_by_limit(self):
        sys.argv = ["Tk", "plan_show", "-l", "10"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show(self):
        sys.argv = ["Tk", "plan_show", "-p", "测试项目1", "-l", "10"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_show_project_is_none(self):
        sys.argv = ["Tk", "plan_show", "-l"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_job_show(self):
        sys.argv = ["Tk", "job_show", "-p_id", "2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_status_show_id_is_none(self):
        sys.argv = ["Tk", "plan_status_show"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_job_status_show(self):
        sys.argv = ["Tk", "job_status_show", "-plan_status_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_step_status_show(self):
        sys.argv = ["Tk", "step_status_show", "-job_status_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_step_show(self):
        sys.argv = ["Tk", "step_show", "-job_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_delete_plan(self):
        sys.argv = ["Tk", "plan_delete", "-plan_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_update_plan(self):
        sys.argv = ["Tk", "plan_update", "-plan_id", "9", "-name", "messagePushMethod", "-value",
                    "微信"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_update_job(self):
        sys.argv = ["Tk", "job_update", "-job_id", "1", "-name", "executeScriptCmd", "-value",
                    "echo test2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_update_plan_status(self):
        sys.argv = ["Tk", "plan_status_update", "-plan_status_id", "15", "-name", "executeStatus", "-value",
                    "SKIPPED"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_update_job_status(self):
        sys.argv = ["Tk", "job_status_update", "-job_status_id", "1", "-name", "executeStatus", "-value",
                    "SKIPPED"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_update_step_status(self):
        sys.argv = ["Tk", "step_status_update", "-step_status_id", "1", "-name", "executeStatus", "-value",
                    "SKIPPED"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_update_step(self):
        sys.argv = ["Tk", "step_update", "-step_id", "1", "-name", "executeScriptCmd", "-value",
                    "echo test2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_job_plan_id_is_none(self):
        sys.argv = ["Tk", "job_show"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_start(self):
        sys.argv = ["Tk", "plan_start", "-plan_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_job_start(self):
        sys.argv = ["Tk", "job_start", "-job_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_step_start(self):
        sys.argv = ["Tk", "step_start", "-step_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_job_delete(self):
        sys.argv = ["Tk", "job_delete", "-job_id", "2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_step_delete(self):
        sys.argv = ["Tk", "step_delete", "-step_id", "2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_job_status_delete(self):
        sys.argv = ["Tk", "job_status_delete", "-job_status_id", "2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_step_status_delete(self):
        sys.argv = ["Tk", "step_status_delete", "-step_status_id", "2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_add(self):
        sys.argv = ["Tk", "plan_load", "-file", "test_plan_templates.yml"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)
