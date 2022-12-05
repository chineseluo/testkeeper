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
import time
from loguru import logger
import datetime
import threading
from testkeeper.util.system_info import SystemInfo
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
from testkeeper.interface.sql_interface import SqlInterface
from testkeeper.util.shell_utils import ShellClient
from testkeeper.module.execute_status_module import ExecuteStatus
from testkeeper.service.step_status_service import StepStatusService
from testkeeper.service.job_status_service import JobStatusService
from testkeeper.service.plan_status_service import PlanStatusService
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
        self.step_status_service = StepStatusService()
        self.plan_status_service = PlanStatusService()
        self.job_status_service = JobStatusService()

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

    def stop_test_step(self, step_status_id: str):
        test_step_status_table_obj = self.step_status_service.get_step_status_table_obj(int(step_status_id))
        logger.info(test_step_status_table_obj.__dict__)
        test_job_status_obj = test_step_status_table_obj.testJobStatus
        test_plan_status_obj = test_job_status_obj.testPlanStatus
        if test_step_status_table_obj.executeStatus == ExecuteStatus.RUNNING:
            self.shell_client.check_call(f"kill -9 {test_step_status_table_obj.processPid}")
            test_step_status_table_obj.executeStatus = ExecuteStatus.STOP
            test_job_status_obj.executeStatus = ExecuteStatus.STOP
            test_plan_status_obj.executeStatus = ExecuteStatus.STOP
            test_job_status_obj.testStepStatusList.append(test_step_status_table_obj)
            test_plan_status_obj.testJobStatusList.append(test_job_status_obj)
            self.mul_session.add(test_plan_status_obj)
            self.mul_session.commit()
        else:
            logger.info(f"当前测试步骤{test_step_status_table_obj.id}，不需要停止")

    def start_test_step(self, step_id: str):
        test_step_table_obj = self.get_test_step_by_id(step_id)
        test_job_table_obj = test_step_table_obj.testJob
        test_plan_table_obj = test_step_table_obj.testJob.testPlan
        test_plan_status_table_obj = self.plan_status_service.generate_test_plan_status_table_obj(test_plan_table_obj,
                                                                                                  ExecuteStatus.START)
        test_job_status_table_obj = self.job_status_service.generate_test_job_status_table_obj(test_job_table_obj,
                                                                                               ExecuteStatus.START)
        self.execute_test_step(test_plan_status_table_obj, test_job_status_table_obj, test_step_table_obj, step_id)

    def execute_test_step(self, test_plan_status_table_obj: TestPlanStatusTable,
                          test_job_status_obj: TestJobStatusTable, test_step: TestStepTable, step_id: str):
        test_step_table_obj = self.get_test_step_by_id(step_id)
        test_step_status_table_obj = self.step_status_service.generate_test_step_status_table_obj(test_step,
                                                                                                  test_job_status_obj.executeStatus,
                                                                                                  "")

        def insert_status_table(execute_status: ExecuteStatus):
            test_step_status_table_obj.executeStatus = execute_status
            test_job_status_obj.executeStatus = execute_status
            test_plan_status_table_obj.executeStatus = execute_status
            test_job_status_obj.testStepStatusList.append(test_step_status_table_obj)
            test_plan_status_table_obj.testJobStatusList.append(test_job_status_obj)

        if test_step_table_obj.isSkipped:
            logger.info(f"跳过当前执行的步骤:{test_step_table_obj.stepName}")
            insert_status_table(ExecuteStatus.SKIPPED)
        else:
            logger.info(f"正在执行步骤：{test_step_table_obj.stepName}")
            self.check_execute_step_cmd(test_step, test_step_status_table_obj, test_job_status_obj,
                                        test_plan_status_table_obj)
            if test_step_table_obj.runFailedIsNeedContinue is not True and self.execute_result["ret"] != 0:
                insert_status_table(ExecuteStatus.FAILED)
                raise Exception(f"测试步骤{test_step_table_obj.stepName}执行失败！！！")
            elif test_step_table_obj.runFailedIsNeedContinue is True and self.execute_result["ret"] != 0:
                insert_status_table(ExecuteStatus.FAILED)
                logger.warning(f"测试步骤{test_step_table_obj.stepName}执行失败，继续执行下一个任务......")
            else:
                current_step_status_table_obj = self.step_status_service.get_step_status_table_obj(
                    test_step_table_obj.id)
                if current_step_status_table_obj.executeStatus == ExecuteStatus.STOP:
                    insert_status_table(ExecuteStatus.STOP)
                else:
                    insert_status_table(ExecuteStatus.SUCCESS)
                logger.info(f"测试任务{test_step_table_obj.stepName}执行成功")

    def watch_execute_step_cmd_process(self, test_step: TestStepTable, test_step_status_obj: TestStepStatusTable,
                                       test_job_status_table_obj: TestJobStatusTable,
                                       test_plan_status_table_obj: TestPlanStatusTable):
        time.sleep(test_step.checkInterval)
        pid = SystemInfo.get_process_pid_by_os(self.shell_client, test_step.executeScriptCmd)

        # test_step.processPid = pid

        def insert_status_data(execute_status: ExecuteStatus):
            test_step_status_obj.processPid = pid
            test_step_status_obj.executeStatus = execute_status
            test_step_status_obj.updateTime = datetime.datetime.now()

            test_job_status_table_obj.executeStatus = execute_status
            test_job_status_table_obj.processPid = pid
            test_job_status_table_obj.updateTime = datetime.datetime.now()

            test_plan_status_table_obj.executeStatus = execute_status
            test_plan_status_table_obj.updateTime = datetime.datetime.now()
            logger.info(test_plan_status_table_obj.__dict__)
            test_job_status_table_obj.testStepStatusList.append(test_step_status_obj)
            test_plan_status_table_obj.testJobStatusList.append(test_job_status_table_obj)
            self.mul_session.add(test_plan_status_table_obj)
            self.mul_session.commit()

        while True:
            try:
                process_is_exists, process_is_status = SystemInfo.get_process_status(test_step.executeScriptCmd, pid)
                if process_is_exists is True and process_is_status != "running":
                    logger.warning(f"步骤:{test_step.stepName}，运行异常，进程状态{process_is_status},运行状态:{process_is_status}")
                    # 查询状态表，job_status_table状态是否为STOP，如果是，直接结束，如果不是写入异常状态
                    current_step_status_table_obj = self.step_status_service.get_step_status_table_obj(
                        int(test_step_status_obj.id))
                    if current_step_status_table_obj.executeStatus == ExecuteStatus.STOP:
                        self.execute_result.update({"ret": 0})
                        break
                    else:
                        insert_status_data(ExecuteStatus.EXCEPTION)
                    break
                else:
                    logger.info(f"步骤{test_step.stepName}正在运行中，检查周期{test_step.checkInterval}s,运行状态:{process_is_status}")
                    insert_status_data(ExecuteStatus.RUNNING)
            except Exception as e:
                logger.error(e)
                logger.info(f"步骤{test_step.stepName}执行结束，结束监听")
                break
            time.sleep(test_step.checkInterval)

    def check_execute_step_cmd(self, test_step: TestStepTable, test_step_status_obj: TestStepStatusTable,
                               test_job_status_table_obj: TestJobStatusTable,
                               test_plan_status_table_obj: TestPlanStatusTable):
        execute_cmd_thread = threading.Thread(target=self.execute_cmd, args=(test_step,))
        execute_cmd_thread.setDaemon(True)
        watch_execute_cmd_process_thread = threading.Thread(target=self.watch_execute_step_cmd_process, args=(
            test_step,
            test_step_status_obj,
            test_job_status_table_obj,
            test_plan_status_table_obj
        ))
        watch_execute_cmd_process_thread.setDaemon(True)
        execute_cmd_thread.start()
        watch_execute_cmd_process_thread.start()
        watch_execute_cmd_process_thread.join()
