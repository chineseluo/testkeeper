#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 6:22 下午
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : sqlalchemy_db_operation.py
@IDE     : PyCharm
------------------------------------
"""
import os
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class SQLalchemyDbOperation:
    def __init__(self, db_path, db_name):
        self.sqlalchemy_engine = None
        self.sqlalchemy_db_session = None
        self.db_path = db_path
        self.db_name = db_name

    def __connect(self):
        if self.sqlalchemy_engine:
            self.sqlalchemy_engine = None
        # 初始化数据库连接
        db_full_path = os.path.join(self.db_path, self.db_name)
        logger.info(f'数据库路径为：{db_full_path}')
        self.sqlalchemy_engine = create_engine(
            f'sqlite:///{db_full_path}', echo=True,
            connect_args={'check_same_thread': False})
        # 创建DbSession
        DBSession = sessionmaker(bind=self.sqlalchemy_engine)
        self.sqlalchemy_db_session = DBSession()

    def use_connect(self):
        if self.sqlalchemy_db_session is None:
            self.__connect()
        return self.sqlalchemy_db_session

    def create_table(self):
        self.__connect()
        Base = declarative_base()
        Base.metadata.create_all(self.sqlalchemy_engine)

    def __del__(self):
        if self.sqlalchemy_db_session:
            self.sqlalchemy_db_session.close()
        # if self.sqlalchemy_engine:
        #     self.sqlalchemy_engine.drop()


if __name__ == '__main__':
    print(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))

    # c = s.use_connect().query(SgxAutoTestResult).filter(SgxAutoTestResult.id == 4331).one()
    # print(c.stage)
    # print(c.__dict__)
