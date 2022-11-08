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
import json
from loguru import logger
from testkeeper.service.sql_interface import SqlInterface
from testkeeper.module.sqlite_module import TestJobTable, TestPlanTable
from testkeeper.util.shell_utils import ShellClient


class PlanService(SqlInterface):
    def __init__(self):
        self.shell_client = ShellClient()

    def get_test_plan_list(self, project_name: str = None, limit: int = 3):
        if project_name is not None and limit is not None:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.sqlSession.query(TestPlanTable).filter(
                                  TestPlanTable.projectName == project_name).limit(limit).all()]
        else:
            test_plan_list = [test_plan.__repr__() for test_plan in
                              self.sqlSession.query(TestPlanTable).filter().limit(limit).all()]
        return test_plan_list

    def delete_test_plan(self, plan_id: str):
        if plan_id is None:
            logger.warning("plan_id不能为空！")
        else:
            logger.info(plan_id)
            logger.info(self.sqlSession.query(TestPlanTable).filter(TestPlanTable.planId == plan_id).first())
            self.sqlSession.query(TestPlanTable).filter_by(planId=plan_id).delete()
            self.sqlSession.query(TestJobTable).filter_by(planId=plan_id).delete()
            self.sqlSession.commit()
            logger.info(f"删除测试计划成功:{plan_id}")

    def update_test_plan(self, plan_id: str, name: str, value: str):
        if name is not None and value is not None:
            test_plan = self.sqlSession.query(TestPlanTable).filter_by(planId=plan_id).first()
            if name in test_plan.__dict__:
                test_plan.__setattr__(name, value)
                self.sqlSession.commit()
            else:
                raise Exception("修改的key不存在")

    def add_test_plan(self, file_path: str):
        ...

    def execute_test_plan(self, plan_id: str):
        test_plan = self.sqlSession.query(TestPlanTable).filter_by(planId=plan_id).first()
        test_job_list = self.sqlSession.query(TestJobTable).filter_by(planId=plan_id).all()
        for test_job in test_job_list:
            self.execute_test_job(test_job, test_job.jobId)

    def execute_test_job(self, test_job: TestJobTable, job_id: str):
        test_job = self.get_test_job(job_id) if test_job is None else test_job
        if test_job.isSkipped:
            logger.info(f"跳过当前执行的任务{test_job.jobName}")
        else:
            logger.info(f"正在执行任务：{test_job.jobName}")
            execute_result = self.shell_client.run_cmd(
                f"cd {test_job.executeScriptPath} && run {test_job.executeScriptCmd}",
                timeout=600)
            if execute_result["ret"] != 0:
                test_job.executeStatus = "failed"
            else:
                test_job.executeStatus = "success"
            if test_job.runFailedIsNeedContinue is not True and execute_result["ret"] != 0:
                raise Exception(f"测试任务{test_job.jobName}执行失败！！！")
            else:
                logger.warning(f"测试任务{test_job.jobName}执行失败，继续执行下一个任务......")
            self.sqlSession.commit()

    def stop_test_plan(self, plan_id: str):
        ...

    def stop_test_job(self, job_id: str):
        ...

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

    def get_test_job_list(self, plan_id: str = None):
        if plan_id is not None:
            test_job_list = [test_job.__repr__() for test_job in
                             self.sqlSession.query(TestJobTable).filter(TestJobTable.planId == plan_id).all()]
        else:
            test_job_list = [test_job.__repr__() for test_job in
                             self.sqlSession.query(TestJobTable).filter().all()]
        logger.info(test_job_list)
        return test_job_list

    def get_test_job(self, job_id: str):
        test_job = self.sqlSession.query(TestJobTable).filter(TestJobTable.jobId == job_id).first()
        return test_job
