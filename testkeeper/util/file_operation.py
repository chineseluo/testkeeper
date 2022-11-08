#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 21:16
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : file_operation.py
@IDE     : PyCharm
------------------------------------
"""
import yaml
import os
from loguru import logger
from typing import Text, Dict, List
from testkeeper.exception.exception import TestKeeperFileNotFountException
from testkeeper.util.logger_operation import LoggerFormat


class FileOption:
    @staticmethod
    def read_yaml(file):
        """
        Read YML file
        :param file:
        :return:
        """
        if os.path.isfile(file):
            fr = open(file, 'r', encoding='utf-8')
            yaml_info = yaml.safe_load(fr)
            fr.close()
            # LoggerFormat.console_output("读取TestKeeper配置文件信息", yaml_info)
            return yaml_info
        else:
            raise TestKeeperFileNotFountException(f'TestKeeper提示：【{file}】文件不存在!!!')
