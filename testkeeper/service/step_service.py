#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:36
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : step_service.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
import datetime
from testkeeper.interface.sql_interface import SqlInterface
from testkeeper.util.shell_utils import ShellClient
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable


class StepService(SqlInterface):
    def __init__(self):
        self.shell_client = ShellClient()
        self.execute_result = {}

    def delete_test_step(self, step_id: str):
        if step_id is None:
            logger.warning("step_id不能为空！")
        else:
            logger.info(step_id)
            self.mul_session.query(TestStepTable).filter_by(id=step_id).delete()
            self.mul_session.commit()
            logger.info(f"删除测试步骤成功:{step_id}")

    def update_test_step(self, step_id: str, name: str, value: str):
        self.common_update_method(TestStepTable, step_id, name, value)

    def get_test_step_by_id(self, step_id: str):
        test_job_table_obj = self.mul_session.query(TestStepTable).filter(TestStepTable.id == step_id).first()
        return test_job_table_obj

    def get_test_step_list(self, job_id: str = None):
        if job_id is not None:
            test_step_list = [test_job.__repr__() for test_job in
                              self.mul_session.query(TestStepTable).filter(TestStepTable.jobId == job_id).all()]
        else:
            test_step_list = [test_job.__repr__() for test_job in
                              self.mul_session.query(TestStepTable).filter().all()]
        logger.info(test_step_list)
        return test_step_list

