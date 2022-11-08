#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 21:17
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : exception.py
@IDE     : PyCharm
------------------------------------
"""


class TestKeeperException(Exception):
    """TestKeeper 基础异常"""
    ...


class TestKeeperFileNotFountException(TestKeeperException):
    ...


class TestKeeperCheckerException(TestKeeperException):
    ...


class TestKeeperApiException(TestKeeperException):
    ...
