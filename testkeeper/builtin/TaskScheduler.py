#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 15:40
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : watcher.py
@IDE     : PyCharm
------------------------------------
"""
import asyncio
import time

from loguru import logger
from testkeeper.module.sqlite_module import TestPlanTable, TestJobTable, TestStepTable
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.gevent import GeventScheduler
from testkeeper.service.plan_service import PlanService
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


class TaskScheduler:

    def __init__(self):
        self.executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
        self.job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        self._scheduler = BlockingScheduler()
        self._plan_service = PlanService()

    def test_say(self):
        time.sleep(10)
        logger.info("test****")

    def add_time_job(self):
        test_plan_list = self._plan_service.get_test_plan_list(limit=1000)
        # self._scheduler.add_job(id="1", name="1", func=self.test_say, trigger="interval",
        #                         seconds=10, replace_existing=True, timezone='Asia/Shanghai')
        # self._scheduler.add_job(id="2", name="2", func=self.test_say, trigger="interval",
        #                         seconds=10, replace_existing=True, timezone='Asia/Shanghai')
        for test_plan in test_plan_list:
            logger.info(test_plan)
            plan_service = PlanService()
            self._scheduler.add_job(id=str(test_plan["planId"]),
                                    name=f'{test_plan["projectName"]}_{test_plan["planName"]}_scheduler_task_{test_plan["planId"]}',
                                    func=plan_service.execute_test_plan, trigger="interval",
                                    seconds=30, replace_existing=True, timezone='Asia/Shanghai',
                                    args=[test_plan["planId"]])

    def update_time_job(self):
        ...

    def delete_time_job(self):
        ...

    def get_time_job(self):
        ...

    def get_time_jobs(self):
        return self._scheduler.get_jobs()

    def pause_time_job(self):
        ...

    def resume_time_job(self):
        ...

    def start_execute_time_job(self):
        self.add_time_job()
        self._scheduler.start()


if __name__ == '__main__':
    ts = TaskScheduler()
    ts.start_execute_time_job()
    logger.info(ts.get_time_jobs())
