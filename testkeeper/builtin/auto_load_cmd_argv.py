#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 22:23
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : auto_load_cmd_argv.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
from testkeeper.builtin.testkeeper_conf import TestKeeperConf


class AutoLoadCmdArgv:

    def __init__(self):
        testkeeper_cmd_conf = TestKeeperConf().testkeeper_client_conf
