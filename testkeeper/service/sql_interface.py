#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:47
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : sql_interface.py
@IDE     : PyCharm
------------------------------------
"""
import os
from loguru import logger
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
from sqlalchemy.orm import sessionmaker


class SqlInterface:
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))),
                           "db")
    db_name = "testkeeper.db"
    sql_alchemy = SQLalchemyDbOperation(db_path, db_name)
    sqlSession = sql_alchemy.use_connect()
    mul_session = sql_alchemy.use_connect_by_mul_thread()


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "testkeeper",
                           "db")
    logger.info(db_path)
