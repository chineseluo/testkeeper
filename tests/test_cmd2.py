#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 15:09
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : test_cmd2.py
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

    def test_plan_status_show_id_is_none(self):
        sys.argv = ["Tk", "plan_status_show", "-limit", "20"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_plan_status_delete(self):
        sys.argv = ["Tk", "plan_status_delete", "-plan_status_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)
        sys.argv = ["Tk", "plan_status_delete", "-plan_status_id", "2"]
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

    def test_plan_stop(self):
        sys.argv = ["Tk", "plan_stop", "-plan_status_id", "1"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_job_stop(self):
        sys.argv = ["Tk", "job_stop", "-job_status_id", "2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_step_stop(self):
        sys.argv = ["Tk", "step_stop", "-step_status_id", "2"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)

    def test_show_testkeeper_machine_info(self):
        sys.argv = ["Tk", "show_testkeeper_machine_info"]
        with self.assertRaises(SystemExit) as cm:
            entry()
        self.assertEqual(cm.exception.code, 0)


