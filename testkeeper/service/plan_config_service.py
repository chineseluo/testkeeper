#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:48
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : plan_config_service.py
@IDE     : PyCharm
------------------------------------
"""
import datetime
from testkeeper.interface.sql_interface import SqlInterface

from testkeeper.module.test_plan_conf import TestPlanConfig, TestJobConfig, TestStepConfig, TestMachineConfig
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestStepTable, TestMachineTable


class PlanConfigService(SqlInterface):
    def generate_test_plan_table_obj_by_plan_config(self, test_plan: TestPlanConfig) -> TestPlanTable:
        test_plan_table_obj = TestPlanTable(
            projectName=test_plan.projectName,
            planName=test_plan.PlanName,
            createUser=test_plan.createUser,
            isScheduledExecution=test_plan.isScheduledExecution,
            cron=test_plan.cron,
            isConfigMessagePush=test_plan.isConfigMessagePush,
            messagePushMethod=test_plan.messagePushMethod,
            messagePushWebhook=test_plan.messagePushWebhook,
            updateTime=datetime.datetime.now(),
            createTime=datetime.datetime.now(),
        )
        return test_plan_table_obj

    def generate_test_job_table_obj_by_plan_config(self, test_job: TestJobConfig) -> TestJobTable:
        test_job_table_obj = TestJobTable(
            jobName=test_job.jobName,
            createUser=test_job.createUser,
            executeScriptPath=test_job.executeScriptPath,
            executeScriptCmd=test_job.executeScriptCmd,
            executeTimeout=test_job.executeTimeout,
            runFailedIsNeedContinue=test_job.runFailedIsNeedContinue,
            isSkipped=test_job.isSkipped,
            checkInterval=test_job.checkInterval,
            updateTime=datetime.datetime.now(),
            createTime=datetime.datetime.now()
        )
        return test_job_table_obj

    def generate_test_step_table_obj_by_plan_config(self, test_step: TestStepConfig,
                                                    test_job: TestJobConfig) -> TestStepTable:
        test_step_table_obj = TestStepTable(
            stepName=test_step.stepName,
            executeScriptPath=test_step.executeScriptPath,
            executeScriptCmd=test_step.executeScriptCmd,
            runFailedIsNeedContinue=test_step.runFailedIsNeedContinue,
            isSkipped=test_job.isSkipped,
            checkInterval=test_job.checkInterval,
            updateTime=datetime.datetime.now(),
            createTime=datetime.datetime.now(),
        )
        return test_step_table_obj

    def generate_test_machine_table_obj_by_plan_config(self, test_machine: TestMachineConfig) -> TestMachineTable:
        test_machine_table_obj = TestMachineTable(
            ip=test_machine.ip,
            username=test_machine.username,
            password=test_machine.password,
            hostName=test_machine.hostName,
            cpuSize=test_machine.cpuSize,
            memorySize=test_machine.memorySize,
            diskSize=test_machine.diskSize,
            updateTime=datetime.datetime.now(),
            createTime=datetime.datetime.now(),
        )
        return test_machine_table_obj

    def add_test_plan(self, file_path: str):
        test_plan = TestPlanConfig(file_path)
        test_plan_table_obj = self.generate_test_plan_table_obj_by_plan_config(test_plan)
        for test_job in test_plan.TestJob:
            test_job_table_obj = self.generate_test_job_table_obj_by_plan_config(test_job)
            for test_machine in test_job.executeMachineIpList:
                test_machine_table_obj = self.generate_test_machine_table_obj_by_plan_config(test_machine)
                test_job_table_obj.executeMachineIpList.append(test_machine_table_obj)
            for test_step in test_job.TestStep:
                test_step_table_obj = self.generate_test_step_table_obj_by_plan_config(test_step, test_job)
                test_job_table_obj.testSteps.append(test_step_table_obj)
            test_plan_table_obj.testJobs.append(test_job_table_obj)
        self.mul_session.add(test_plan_table_obj)
        self.mul_session.commit()
