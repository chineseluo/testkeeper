#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:45
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : job_center.py
@IDE     : PyCharm
------------------------------------
"""
from testkeeper.service.job_status_service import JobStatusService
from testkeeper.service.plan_status_service import PlanStatusService
from testkeeper.service.step_status_service import StepStatusService
from testkeeper.util.system_info import SystemInfo
import asyncio
import datetime
import functools
from loguru import logger
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable
from testkeeper.service.job_service import JobService
from testkeeper.service.plan_service import PlanService
from testkeeper.module.execute_status_module import ExecuteStatus
from testkeeper.util.shell_utils import ShellClient


class JobCenter:
    def __init__(self):
        self.job_status_service = JobStatusService()
        self.plan_status_service = PlanStatusService()
        self.step_status_service = StepStatusService()
        self.job_service = JobService()
        self.plan_service = PlanService()
        # self.loop = asyncio.get_event_loop()
        # self.loop = asyncio.set_event_loop(asyncio.new_event_loop())
        self.shell_client = ShellClient()
        self.execute_result = {}

    def execute_test_job(self, loop, test_plan_status_table_obj, test_job: TestJobTable, job_id: str):
        logger.info(self.plan_status_service.mul_session.hash_key)

        test_job = self.job_service.get_test_job_by_id(job_id) if test_job is None else test_job
        test_job_status_table_obj = self.job_status_service.generate_test_job_status_table_obj(test_job,
                                                                                               ExecuteStatus.START)

        def insert_status_table(execute_status: ExecuteStatus):
            test_job_status_table_obj.executeStatus = execute_status
            test_plan_status_table_obj.executeStatus = execute_status
            test_plan_status_table_obj.testJobStatusList.append(test_job_status_table_obj)
            logger.info(self.plan_status_service.mul_session.hash_key)
            self.plan_status_service.mul_session.add(test_plan_status_table_obj)
            # except Exception as e:
            #     logger.info(e)
            #     self.mul_session.query(TestPlanStatusTable).filter_by(planId=test_plan_status_table_obj.planId).update(
            #         {"executeStatus": execute_status})
            # finally:
            self.plan_status_service.mul_session.commit()

        if test_job.isSkipped:
            logger.info(f"跳过当前执行的任务{test_job.jobName}")
            test_job_status_table_obj.executeStatus = ExecuteStatus.SKIPPED
        else:
            logger.info(f"正在执行任务：{test_job.jobName}")
            self.check_execute_job_cmd_by_async(loop, test_job, test_plan_status_table_obj, test_job_status_table_obj)
            logger.info(f'ret:{self.execute_result["ret"]}')
            if test_job.runFailedIsNeedContinue is not True and self.execute_result["ret"] != 0:
                insert_status_table(ExecuteStatus.FAILED)
                raise Exception(f"测试任务{test_job.jobName}执行失败！！！")
            elif test_job.runFailedIsNeedContinue is True and self.execute_result["ret"] != 0:
                insert_status_table(ExecuteStatus.FAILED)
                logger.warning(f"测试任务{test_job.jobName}执行失败，继续执行下一个任务......")
            else:
                # current_job_status_table_obj = self.job_status_service.get_job_status_table_obj(
                #     test_job_status_table_obj.id)
                if test_job_status_table_obj.executeStatus == ExecuteStatus.STOP:
                    insert_status_table(ExecuteStatus.STOP)
                else:
                    insert_status_table(ExecuteStatus.SUCCESS)
                logger.info(f"测试任务{test_job.jobName}执行成功")

    async def watch_execute_cmd_by_async(self, test_job, test_plan_status_table_obj, test_job_status_table_obj):
        await asyncio.sleep(test_job.checkInterval)
        pid = SystemInfo.get_process_pid_by_os(self.shell_client,
                                               f"cd {test_job.executeScriptPath} &&  echo 测试计划_id_{test_job.testPlan.id}_测试任务id_{test_job.id} &&  {test_job.executeScriptCmd}")
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
            try:
                self.plan_status_service.mul_session.add(test_plan_status_table_obj)
            except Exception as e:
                logger.info(e)
                self.plan_status_service.mul_session.query(TestPlanStatusTable).filter_by(
                    planId=test_plan_status_table_obj.planId).update(
                    {"executeStatus": execute_status})
            finally:
                self.plan_status_service.mul_session.commit()

        while True:
            logger.info("开始监听......")
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
                        current_job_status_table_obj = self.job_service.mul_session.query(TestJobStatusTable).filter_by(
                            id=test_job_status_table_obj.id).first()
                    except Exception as e:
                        logger.info(e)
                        raise e

                    if current_job_status_table_obj.executeStatus == ExecuteStatus.STOP:
                        self.execute_result.update({"ret": 0})
                        logger.info(self.execute_result)

                        return
                    elif current_job_status_table_obj.executeStatus == ExecuteStatus.RUNNING:
                        self.execute_result.update({"ret": 0})
                        logger.info(self.execute_result)
                        return
                    else:
                        self.execute_result.update({"ret": 1})
                        logger.info(self.execute_result)

                        insert_status_data(ExecuteStatus.EXCEPTION)
                        return
                else:
                    logger.info(
                        f"任务{test_job.jobName}正在运行中，检查周期{test_job.checkInterval}s,运行状态:{process_is_status}")
                    insert_status_data(ExecuteStatus.RUNNING)
            except Exception as e:
                logger.info(e)
                self.execute_result.update({"ret": 0})
                logger.info(f"任务{test_job.jobName}执行结束，结束监听")
                return
            await asyncio.sleep(test_job.checkInterval)

    def check_execute_job_cmd_by_async(self, loop, test_job, test_plan_status_table_obj, test_job_status_table_obj):
        asyncio.set_event_loop(loop)
        tasks = [asyncio.ensure_future(self.execute_cmd_by_async(loop, test_job)),
                 asyncio.ensure_future(
                     self.watch_execute_cmd_by_async(test_job, test_plan_status_table_obj, test_job_status_table_obj))]
        loop.run_until_complete(asyncio.wait(tasks))

    async def execute_cmd_by_async(self,loop, test_job):
        logger.info("开始执行命令")
        await loop.run_in_executor(None, functools.partial(self.shell_client.run_cmd,
                                                                cmd=f"cd {test_job.executeScriptPath} &&  echo 测试计划_id_{test_job.testPlan.id}_测试任务id_{test_job.id} &&  {test_job.executeScriptCmd}",
                                                                timeout=600))

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

    def execute_test_plan(self, loop, plan_id: str):
        loop = asyncio.new_event_loop() if loop is None else loop
        test_plan_status_table_obj = self.plan_status_service.get_plan_status_table_obj_by_plan_id(plan_id)
        # 检查是否有正在运行的任务，任务状态是否是running或者start，如果有，需要等待上一个任务完成，或者，修改上一个任务的状态
        if test_plan_status_table_obj is not None and test_plan_status_table_obj.executeStatus in [
            ExecuteStatus.RUNNING, ExecuteStatus.START]:
            logger.error(f"当前测试计划{plan_id},有正在运行的计划，待上一个计划执行完在执行......")
            return
        else:
            test_plan = self.plan_service.get_test_plan_by_id(plan_id)
            logger.info(test_plan.__repr__())
            logger.info(
                f"当前测试计划没有正在运行的计划，开始执行，测试项目:{test_plan.projectName},测试计划:{test_plan.planName}，测试计划id:{test_plan.id}")

            test_plan_status_table_obj = self.plan_status_service.generate_test_plan_status_table_obj(test_plan,
                                                                                                      ExecuteStatus.START)
            for test_job in self.plan_service.get_test_job_list_by_plan_id(plan_id):
                self.execute_test_job(loop, test_plan_status_table_obj, test_job, test_job.id)

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
                    self.plan_status_service.mul_session.add(test_plan_status_obj)
                    self.plan_status_service.mul_session.commit()
                else:
                    logger.info(f"当前测试任务{test_job_status_obj.id}，不需要停止")
        else:
            logger.error(f"测试计划:{plan_status_id}状态为非RUNNING，不能进行STOP操作!!!")
