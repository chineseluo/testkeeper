#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:46
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : job_service.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
import datetime
import time
import threading
from testkeeper.interface.sql_interface import SqlInterface
from testkeeper.module.execute_status_module import ExecuteStatus
from testkeeper.util.system_info import SystemInfo
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
from testkeeper.service.job_status_service import JobStatusService
from testkeeper.service.plan_status_service import PlanStatusService
from testkeeper.service.step_status_service import StepStatusService
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable


class JobService(SqlInterface):

    def __init__(self):
        self.job_status_service = JobStatusService()
        self.plan_status_service = PlanStatusService()
        self.step_status_service = StepStatusService()

    def delete_test_job(self, job_id: str):
        if job_id is None:
            logger.warning("job_id不能为空！")
        else:
            logger.info(job_id)
            self.mul_session.query(TestJobTable).filter_by(id=job_id).delete()
            self.mul_session.query(TestStepTable).filter_by(jobId=job_id).delete()
            self.mul_session.commit()
            logger.info(f"删除测试任务成功:{job_id}")

    def update_test_job(self, job_id: str, name: str, value: str):
        self.common_update_method(TestJobTable, job_id, name, value)

    def get_test_job_by_id(self, job_id: str):
        test_job_table_obj = self.mul_session.query(TestJobTable).filter(TestJobTable.id == job_id).first()
        return test_job_table_obj

    def get_test_job_list(self, plan_id: str = None):
        if plan_id is not None:
            test_job_list = [test_job.__repr__() for test_job in
                             self.mul_session.query(TestJobTable).filter(TestJobTable.planId == plan_id).all()]
        else:
            test_job_list = [test_job.__repr__() for test_job in
                             self.mul_session.query(TestJobTable).filter().all()]
        return test_job_list

    def stop_test_job(self, job_status_id: str):
        test_job_status_obj = self.job_status_service.get_job_status_table_obj(int(job_status_id))
        test_plan_status_obj = test_job_status_obj.testPlanStatus
        if test_job_status_obj.executeStatus == ExecuteStatus.RUNNING:
            self.shell_client.check_call(f"kill -9 {test_job_status_obj.processPid}")
            test_job_status_obj.executeStatus = ExecuteStatus.STOP
            test_plan_status_obj.executeStatus = ExecuteStatus.STOP
            test_plan_status_obj.testJobStatusList.append(test_job_status_obj)
            self.mul_session.add(test_plan_status_obj)
            self.mul_session.commit()
        else:
            logger.info(f"当前测试任务{test_job_status_obj.id}，不需要停止")

    def start_test_job(self, job_id: str):
        """
        启动测试任务，会给plan_status_table添加一条数据，区别是这个plan_status_table的数据只会关联一个job，因为只执行了一个job
        :param job_id:
        :return:
        """
        test_job_table_obj = self.get_test_job_by_id(job_id)
        test_plan_table_obj = test_job_table_obj.testPlan
        test_plan_status_table_obj = self.plan_status_service.generate_test_plan_status_table_obj(test_plan_table_obj,
                                                                                                  ExecuteStatus.START)
        self.execute_test_job(test_plan_status_table_obj, test_job_table_obj, test_job_table_obj.id)

    def execute_test_job(self, test_plan_status_table_obj, test_job: TestJobTable, job_id: str):

        test_job = self.get_test_job_by_id(job_id) if test_job is None else test_job
        test_job_status_table_obj = self.job_status_service.generate_test_job_status_table_obj(test_job,
                                                                                               ExecuteStatus.START)

        def insert_status_table(execute_status: ExecuteStatus):
            test_job_status_table_obj.executeStatus = execute_status
            test_plan_status_table_obj.executeStatus = execute_status
            test_plan_status_table_obj.testJobStatusList.append(test_job_status_table_obj)
            self.mul_session.add(test_plan_status_table_obj)
            self.mul_session.commit()

        if test_job.isSkipped:
            logger.info(f"跳过当前执行的任务{test_job.jobName}")
            test_job_status_table_obj.executeStatus = ExecuteStatus.SKIPPED
        else:
            logger.info(f"正在执行任务：{test_job.jobName}")
            self.check_execute_job_cmd(test_job, test_plan_status_table_obj, test_job_status_table_obj)

            if test_job.runFailedIsNeedContinue is not True and self.execute_result["ret"] != 0:
                insert_status_table(ExecuteStatus.FAILED)
                raise Exception(f"测试任务{test_job.jobName}执行失败！！！")
            elif test_job.runFailedIsNeedContinue is True and self.execute_result["ret"] != 0:
                insert_status_table(ExecuteStatus.FAILED)
                logger.warning(f"测试任务{test_job.jobName}执行失败，继续执行下一个任务......")
            else:
                current_job_status_table_obj = self.job_status_service.get_job_status_table_obj(
                    test_job_status_table_obj.id)
                if current_job_status_table_obj.executeStatus == ExecuteStatus.STOP:
                    insert_status_table(ExecuteStatus.STOP)
                else:
                    insert_status_table(ExecuteStatus.SUCCESS)
                logger.info(f"测试任务{test_job.jobName}执行成功")


    def check_execute_job_cmd(self, test_job, test_plan_status_table_obj, test_job_status_table_obj):
        execute_cmd_thread = threading.Thread(target=self.execute_cmd, args=(test_job,))
        execute_cmd_thread.setDaemon(True)
        watch_execute_cmd_process_thread = threading.Thread(target=self.watch_execute_job_cmd_process,
                                                            args=(test_job, test_plan_status_table_obj,
                                                                  test_job_status_table_obj))
        watch_execute_cmd_process_thread.setDaemon(True)
        execute_cmd_thread.start()
        watch_execute_cmd_process_thread.start()
        watch_execute_cmd_process_thread.join()

    def watch_execute_job_cmd_process(self, test_job, test_plan_status_table_obj, test_job_status_table_obj):
        time.sleep(test_job.checkInterval)
        pid = SystemInfo.get_process_pid_by_os(self.shell_client, test_job.executeScriptCmd)
        test_job_status_table_obj.processPid = pid

        def insert_status_data(execute_status: ExecuteStatus):
            for test_step in test_job.testSteps:
                test_step_status_table_obj = self.step_status_service.generate_test_step_status_table_obj(test_step,
                                                                                                          test_job_status_table_obj.executeStatus,
                                                                                                          pid)
                test_job_status_table_obj.testStepStatusList.append(test_step_status_table_obj)
            test_plan_status_table_obj.executeStatus = execute_status
            test_job_status_table_obj.executeStatus = execute_status
            test_plan_status_table_obj.testJobStatusList.append(test_job_status_table_obj)
            new_db_session = SQLalchemyDbOperation(self.db_path, self.db_name).use_connect()
            new_db_session.add(test_plan_status_table_obj)
            new_db_session.commit()
            # new_db_session.close()

        while True:
            try:
                process_is_exists, process_is_status = SystemInfo.get_process_status(test_job.executeScriptCmd, pid)
                test_job_status_table_obj.updateTime = datetime.datetime.now()
                test_plan_status_table_obj.updateTime = datetime.datetime.now()
                logger.info(process_is_exists)
                logger.info(process_is_status)
                if process_is_exists is True and process_is_status != "running":
                    logger.warning(f"任务:{test_job.jobName}，运行异常，进程状态{process_is_status},运行状态:{process_is_status}")
                    # 查询状态表，job_status_table状态是否为STOP，如果是，直接结束，如果不是写入异常状态
                    try:
                        current_job_status_table_obj = self.mul_session.query(TestJobStatusTable).filter_by(
                            id=test_job_status_table_obj.id).first()
                    except Exception as e:
                        logger.info(e)
                        raise e

                    if current_job_status_table_obj.executeStatus == ExecuteStatus.STOP:
                        self.execute_result.update({"ret": 0})
                        break
                    else:
                        insert_status_data(ExecuteStatus.EXCEPTION)
                    break
                else:
                    logger.info(
                        f"任务{test_job.jobName}正在运行中，检查周期{test_job.checkInterval}s,运行状态:{process_is_status}")
                    insert_status_data(ExecuteStatus.RUNNING)
            except Exception as e:
                logger.info(e)
                logger.info(f"任务{test_job.jobName}执行结束，结束监听")
                break
            time.sleep(test_job.checkInterval)
