#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 21:22
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : testkeeper_conf.py
@IDE     : PyCharm
------------------------------------
"""
import os
from loguru import logger
from testkeeper.util.file_operation import FileOption
from testkeeper.util.logger_operation import LoggerFormat


class TestKeeperConf:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_testkeeper'):
            cls._testkeeper = super(TestKeeperConf, cls).__new__(cls)
        return cls._testkeeper

    def __init__(self):
        self.base_path = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        self.testkeeper_conf = FileOption.read_yaml(os.path.join(self.base_path, "testkeeper_conf.yml"))
        self.testkeeper_client_conf = FileOption.read_yaml(os.path.join(self.base_path, "testkeeper_cmd_conf.yml"))


if __name__ == '__main__':
    tkcc = TestKeeperConf()
    logger.info(tkcc)
    tkcb = TestKeeperConf()
    logger.info(tkcb)
