#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:59
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : execute_status_module.py
@IDE     : PyCharm
------------------------------------
"""
from enum import Enum
from typing import Text


class ExecuteStatus(Text, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    EXCEPTION = "EXCEPTION"
    RUNNING = "RUNNING"
    SKIPPED = "SKIPPED"
    STOP = "STOP"
    START = "START"
    END = "END"
