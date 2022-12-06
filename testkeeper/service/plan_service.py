#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:47
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : plan_service.py
@IDE     : PyCharm
------------------------------------
"""
import os
import time
import datetime
from loguru import logger
import threading
from testkeeper.interface.sql_interface import SqlInterface
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable
from testkeeper.module.execute_status_module import ExecuteStatus
from testkeeper.util.shell_utils import ShellClient
from testkeeper.util.system_info import SystemInfo
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
from testkeeper.service.job_service import JobService
from testkeeper.service.step_service import StepService
from testkeeper.service.plan_status_service import PlanStatusService
from testkeeper.service.job_status_service import JobStatusService
from testkeeper.service.step_status_service import StepStatusService


class PlanService(SqlInterface):
    def __init__(self):
        self.shell_client = ShellClient()
        self.execute_result = {}
        self.job_service = JobService()
        self.step_service = StepService()
        self.plan_status_service = PlanStatusService()
        self.job_status_service = JobStatusService()
        self.step_status_service = StepStatusService()

    def get_test_plan_list(self, project_name: str = None, limit: int = 3):
        if project_name is not None and limit is not None:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.mul_session.query(TestPlanTable).filter(
                                  TestPlanTable.projectName == project_name).limit(limit).all()]
        elif project_name is None and limit is not None:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.mul_session.query(TestPlanTable).filter().limit(limit).all()]
        elif project_name is not None and limit is None:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.mul_session.query(TestPlanTable).filter(
                                  TestPlanTable.projectName == project_name).limit(limit).all()]
        else:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.mul_session.query(TestPlanTable).filter().limit(limit).all()]
        return test_plan_list

    def delete_test_plan(self, plan_id: str):
        if plan_id is None:
            logger.warning("plan_id不能为空！")
        else:
            logger.info(self.get_test_plan_by_id(plan_id))
            self.get_test_plan_by_id(plan_id).delete()
            self.mul_session.query(TestJobTable).filter_by(planId=plan_id).delete()
            self.mul_session.commit()
            logger.info(f"删除测试计划成功:{plan_id}")

    def update_test_plan(self, plan_id: str, name: str, value: str):
        self.common_update_method(TestPlanTable, plan_id, name, value)

    def get_test_plan_by_id(self, plan_id: str) -> TestPlanTable:
        test_plan_table_obj = self.mul_session.query(TestPlanTable).filter(TestPlanTable.id == plan_id).first()
        return test_plan_table_obj

    def execute_test_plan(self, plan_id: str):
        test_plan_status_table_obj = self.mul_session.query(TestPlanStatusTable).filter_by(planId=plan_id).first()
        # 检查是否有正在运行的任务，任务状态是否是running或者start，如果有，需要等待上一个任务完成，或者，修改上一个任务的状态
        if test_plan_status_table_obj is not None and test_plan_status_table_obj.executeStatus in [
            ExecuteStatus.RUNNING, ExecuteStatus.START]:
            logger.error(f"当前测试计划{plan_id},有正在运行的计划，待上一个计划执行完在执行......")
            return
        else:
            test_plan = self.mul_session.query(TestPlanTable).filter_by(id=plan_id).first()
            logger.info(
                f"当前测试计划没有正在运行的计划，开始执行，测试项目:{test_plan.projectName},测试计划:{test_plan.planName}，测试计划id:{test_plan.id}")

            test_job_list = self.mul_session.query(TestJobTable).filter_by(id=plan_id).all()
            test_plan_status_table_obj = self.plan_status_service.generate_test_plan_status_table_obj(test_plan,
                                                                                                      ExecuteStatus.START)

            for test_job in test_job_list:
                self.job_service.execute_test_job(test_plan_status_table_obj, test_job, test_job.id)

    def stop_test_plan(self, plan_status_id: str):
        test_plan_status_obj = self.plan_status_service.get_plan_status_table_obj(int(plan_status_id))
        logger.info(test_plan_status_obj.__repr__())
        if test_plan_status_obj.executeStatus == ExecuteStatus.RUNNING:
            for test_job_status_obj in test_plan_status_obj.testJobStatusList:
                if test_job_status_obj.executeStatus == ExecuteStatus.RUNNING:
                    self.shell_client.check_call(f"kill -9 {test_job_status_obj.processPid}")
                    self.execute_result["ret"] = 0
                    for test_step_status_obj in test_job_status_obj.testStepStatusList:
                        test_step_status_obj.executeStatus = ExecuteStatus.STOP
                        # test_job_status_obj.testStepStatusList.append(test_step_status_obj)
                    test_job_status_obj.executeStatus = ExecuteStatus.STOP
                    test_plan_status_obj.executeStatus = ExecuteStatus.STOP
                    test_plan_status_obj.testJobStatusList.append(test_job_status_obj)
                    self.mul_session.add(test_plan_status_obj)
                    self.mul_session.commit()
                else:
                    logger.info(f"当前测试任务{test_job_status_obj.id}，不需要停止")
        else:
            logger.error(f"测试计划:{plan_status_id}状态为非RUNNING，不能进行STOP操作!!!")


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))),
                           "db")
    logger.info(db_path)
