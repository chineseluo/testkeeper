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
from testkeeper.interface import sql_interface
from testkeeper.util.shell_utils import ShellClient
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable


class JobService(sql_interface):

    def __init__(self):
        self.shell_client = ShellClient()
        self.execute_result = {}

    def common_update_method(self, table_obj, update_id: str, name: str, value: str):
        table_obj_instance = self.mul_session.query(table_obj).filter_by(id=update_id).first()
        logger.info(table_obj_instance.__repr__())
        if name in table_obj_instance.__dict__:
            table_obj_instance.__setattr__(name, value)
            table_obj_instance.updateTime = datetime.datetime.now()
            self.mul_session.commit()
        else:
            raise Exception(f"修改的key:{name} 不存在")

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
        logger.info(test_job_list)
        return test_job_list
