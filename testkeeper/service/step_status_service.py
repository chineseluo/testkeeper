#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:36
@Auth    : luozhongwen
@Email   : luozhongwen@sensorsdata.cn
@File    : step_status_service.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
import datetime
from testkeeper.interface import sql_interface
from testkeeper.util.shell_utils import ShellClient
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable


class StepStatusService(sql_interface):
    def __init__(self):
        self.shell_client = ShellClient()
        self.execute_result = {}

    def update_test_step_status(self, step_status_id: str, name: str, value: str):
        self.common_update_method(TestStepStatusTable, step_status_id, name, value)

    def delete_test_step_status(self, step_status_id: str):
        if step_status_id is None:
            logger.warning("step_status_id不能为空！")
        else:
            logger.info(step_status_id)
            self.mul_session.query(TestStepStatusTable).filter_by(id=step_status_id).delete()
            self.mul_session.commit()
            logger.info(f"删除测试步骤成功:{step_status_id}")

    def get_test_step_status_list(self, job_status_id: str = None):
        if job_status_id is not None:
            test_step_status_list = [test_job.__repr__() for test_job in
                                     self.mul_session.query(TestStepStatusTable).filter(
                                         TestStepStatusTable.jobStatusId == job_status_id).all()]
        else:
            test_step_status_list = [test_job.__repr__() for test_job in
                                     self.mul_session.query(TestStepStatusTable).filter().all()]
        logger.info(test_step_status_list)
        return test_step_status_list
