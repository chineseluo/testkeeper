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
import datetime
from testkeeper.util.shell_utils import ShellClient
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable


class SqlInterface:
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))),
                           "db")
    db_name = "testkeeper.db"
    sql_alchemy = SQLalchemyDbOperation(db_path, db_name)
    sqlSession = sql_alchemy.use_connect()
    mul_session = sql_alchemy.use_connect_by_mul_thread()
    execute_result = {}
    shell_client = ShellClient()

    def common_update_method(self, table_obj, update_id: str, name: str, value: str):
        table_obj_instance = self.mul_session.query(table_obj).filter_by(id=update_id).first()
        logger.info(table_obj_instance.__repr__())
        if name in table_obj_instance.__dict__:
            table_obj_instance.__setattr__(name, value)
            table_obj_instance.updateTime = datetime.datetime.now()
            self.mul_session.commit()
        else:
            raise Exception(f"修改的key:{name} 不存在")

    def execute_cmd(self, test_obj: TestJobTable):
        self.execute_result = self.shell_client.run_cmd(
            f"cd {test_obj.executeScriptPath} && {test_obj.executeScriptCmd}",
            timeout=600)


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "testkeeper",
                           "db")
    logger.info(db_path)
