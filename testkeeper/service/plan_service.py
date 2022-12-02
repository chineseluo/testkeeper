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
from testkeeper.builtin.test_plan_conf import TestPlanConfig, TestJobConfig, TestStepConfig, TestMachineConfig
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

    def start_test_job(self, job_id: str):
        """
        启动测试任务，会给plan_status_table添加一条数据，区别是这个plan_status_table的数据只会关联一个job，因为只执行了一个job
        :param job_id:
        :return:
        """
        test_job_table_obj = self.job_service.get_test_job_by_id(job_id)
        test_plan_table_obj = test_job_table_obj.testPlan
        test_plan_status_table_obj = self.plan_status_service.generate_test_plan_status_table_obj(test_plan_table_obj,
                                                                                                  ExecuteStatus.START)
        self.execute_test_job(test_plan_status_table_obj, test_job_table_obj, test_job_table_obj.id)

    def start_test_step(self, step_id: str):
        test_step_table_obj = self.job_service.get_test_step_by_id(step_id)
        test_job_table_obj = test_step_table_obj.testJob
        test_plan_table_obj = test_step_table_obj.testJob.testPlan
        test_plan_status_table_obj = self.plan_status_service.generate_test_plan_status_table_obj(test_plan_table_obj,
                                                                                                  ExecuteStatus.START)
        test_job_status_table_obj = self.job_status_service.generate_test_job_status_table_obj(test_job_table_obj,
                                                                                               ExecuteStatus.START)
        self.execute_test_step(test_plan_status_table_obj, test_job_status_table_obj, test_step_table_obj, step_id)

    def stop_test_step(self, step_status_id: str):
        test_step_status_table_obj = self.get_step_status_table_obj(int(step_status_id))
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

    def execute_test_plan(self, plan_id: str):
        test_plan_status_table_obj = self.mul_session.query(TestPlanStatusTable).filter_by(planId=plan_id).first()

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
            logger.info(test_plan_status_table_obj.__repr__())
            for test_job in test_job_list:
                self.execute_test_job(test_plan_status_table_obj, test_job, test_job.id)
            self.mul_session.add(test_plan_status_table_obj)
            self.mul_session.commit()

    def execute_cmd(self, test_obj):
        logger.info("#####")
        self.execute_result = self.shell_client.run_cmd(
            f"cd {test_obj.executeScriptPath} && {test_obj.executeScriptCmd}",
            timeout=600)

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
                    current_step_status_table_obj = self.get_step_status_table_obj(int(test_step_status_obj.id))
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

    def get_plan_status_table_obj(self, plan_status_id: int) -> TestPlanStatusTable:
        plan_status_table_obj = self.mul_session.query(TestPlanStatusTable).filter_by(id=plan_status_id).first()
        return plan_status_table_obj

    def get_step_status_table_obj(self, step_status_id: int) -> TestStepStatusTable:
        step_status_table_obj = self.mul_session.query(TestStepStatusTable).filter_by(id=step_status_id).first()
        return step_status_table_obj

    def execute_test_step(self, test_plan_status_table_obj: TestPlanStatusTable,
                          test_job_status_obj: TestJobStatusTable, test_step: TestStepTable, step_id: str):
        test_step_table_obj = self.job_service.get_test_step_by_id(step_id)
        test_step_status_table_obj = self.step_status_service.generate_test_step_status_table_obj(test_step, test_job_status_obj.executeStatus,"")

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
                current_step_status_table_obj = self.get_step_status_table_obj(test_step_table_obj.id)
                if current_step_status_table_obj.executeStatus == ExecuteStatus.STOP:
                    insert_status_table(ExecuteStatus.STOP)
                else:
                    insert_status_table(ExecuteStatus.SUCCESS)
                logger.info(f"测试任务{test_step_table_obj.stepName}执行成功")

    def execute_test_job(self, test_plan_status_table_obj, test_job: TestJobTable, job_id: str):
        test_job = self.job_service.get_test_job_by_id(job_id) if test_job is None else test_job
        test_job_status_table_obj = self.job_status_service.generate_test_job_status_table_obj(test_job, ExecuteStatus.START)

        def insert_status_table(execute_status: ExecuteStatus):
            test_job_status_table_obj.executeStatus = execute_status
            test_plan_status_table_obj.executeStatus = execute_status

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
        test_plan_status_table_obj.testJobStatusList.append(test_job_status_table_obj)

    def stop_test_plan(self, plan_status_id: str):
        test_plan_status_obj = self.get_plan_status_table_obj(int(plan_status_id))
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

    def check_job_status(self, check_interval: int = 10):
        # TODO 执行任务后，开启一个异步线程，进行监听任务状态，如果任务处于运行中，修改executeStatus为running，如果任务结束，主动结束该子线程
        # 如果是本机执行，只需要检查是否存在进程即可，如果是非本机执行，需要使用ssh，然后检查进程是否存在
        # TODO 如果管控僵尸进程
        logger.info(f"开启监控线程，检查job时间间隔为{check_interval}")
        ...

    def distribute_script(self):
        # TODO 分发测试脚本到不同机器
        # 打包 -> 分发 -> 解压
        ...


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))),
                           "db")
    logger.info(db_path)
