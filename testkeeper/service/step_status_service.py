#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:36
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : step_status_service.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
import datetime
from testkeeper.module.execute_status_module import ExecuteStatus
from testkeeper.interface.sql_interface import SqlInterface
from testkeeper.util.shell_utils import ShellClient
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable


class StepStatusService(SqlInterface):
    def __init__(self):
        super().__init__()
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

    def generate_test_step_status_table_obj(self, test_step: TestStepTable,
                                            execute_status: ExecuteStatus, pid: str) -> TestStepStatusTable:
        now_time = datetime.datetime.now()
        test_step_status_table_obj = TestStepStatusTable(
            stepName=test_step.stepName,
            stepId=test_step.id,
            executeStatus=execute_status,
            updateTime=now_time,
            createTime=now_time,
            processPid=pid
        )
        return test_step_status_table_obj

    def get_step_status_table_obj(self, step_status_id: int) -> TestStepStatusTable:
        step_status_table_obj = self.mul_session.query(TestStepStatusTable).filter_by(id=step_status_id).first()
        return step_status_table_obj
