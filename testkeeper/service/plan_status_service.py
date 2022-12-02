#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:36
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : plan_status_service.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
import datetime
from testkeeper.interface import sql_interface
from testkeeper.module.execute_status_module import ExecuteStatus
from testkeeper.util.shell_utils import ShellClient
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable


class PlanStatusService(sql_interface):
    def __init__(self):
        self.shell_client = ShellClient()
        self.execute_result = {}

    def update_test_plan_status(self, plan_status_id, name: str, value: str):
        self.common_update_method(TestPlanStatusTable, plan_status_id, name, value)

    def delete_test_plan_status(self, plan_status_id: str):
        if plan_status_id is None:
            logger.warning("plan_id不能为空！")
        else:
            logger.info(plan_status_id)
            self.mul_session.query(TestPlanStatusTable).filter_by(id=plan_status_id).delete()
            self.mul_session.query(TestJobStatusTable).filter_by(planStatusId=plan_status_id).delete()
            self.mul_session.commit()
            logger.info(f"删除测试计划成功:{plan_status_id}")

    def get_test_plan_status_list(self, project_name: str = None, limit: int = 3):
        if project_name is not None and limit is not None:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.mul_session.query(TestPlanStatusTable).filter(
                                         TestPlanTable.projectName == project_name).limit(limit).all()]
        elif project_name is None and limit is not None:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.mul_session.query(TestPlanStatusTable).filter().limit(limit).all()]
        elif project_name is not None and limit is None:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.mul_session.query(TestPlanStatusTable).filter(
                                         TestPlanTable.projectName == project_name).limit(limit).all()]
        else:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.mul_session.query(TestPlanStatusTable).filter().limit(limit).all()]
        return test_plan_status_list

    def generate_test_plan_status_table_obj(self, test_plan: TestPlanTable,
                                            execute_status: ExecuteStatus) -> TestPlanStatusTable:
        now_time = datetime.datetime.now()
        test_plan_status_table_obj = TestPlanStatusTable(
            planName=test_plan.planName,
            planId=test_plan.id,
            executeStatus=execute_status,
            updateTime=now_time,
            createTime=now_time
        )
        return test_plan_status_table_obj


