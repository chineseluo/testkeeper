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
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from testkeeper.service.plan_service import PlanService
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from testkeeper.service.job_center import JobCenter


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
        self._loop = asyncio.new_event_loop()

    def add_time_job(self):
        self._plan_service.limit = 1000
        test_plan_list = self._plan_service.get_test_plan_list()
        logger.info(test_plan_list)
        for test_plan in test_plan_list:
            logger.info(test_plan)
            job_center = JobCenter()
            self._scheduler.add_job(id=str(test_plan["planId"]),
                                    name=f'{test_plan["projectName"]}_{test_plan["planName"]}_scheduler_task_{test_plan["planId"]}',
                                    func=job_center.execute_test_plan, trigger="interval",
                                    seconds=60, replace_existing=True, timezone='Asia/Shanghai',
                                    args=[ str(test_plan["planId"]), self._loop])

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
