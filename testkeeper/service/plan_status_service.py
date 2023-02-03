#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:36
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : plan_status_service.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
import datetime
from testkeeper.interface.sql_interface import SqlInterface
from testkeeper.module.execute_status_module import ExecuteStatus
from testkeeper.util.shell_utils import ShellClient
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestMachineTable
from testkeeper.exception.exception import *
from typing import Text


class PlanStatusService(SqlInterface):
    def __init__(self):
        super().__init__()
        self.shell_client = ShellClient()
        self.execute_result = {}
        self.__plan_status_id = None
        self.__project_name = None
        self.__limit = 3
        self.__plan_id = None

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, limit):
        if limit is None:
            self.__limit = self.__limit
        else:
            if not isinstance(limit, int):
                raise TestKeeperArgvCheckException(f"参数limit:{limit}，类型错误，应当为int类型！")
            self.__limit = limit

    @property
    def project_name(self):
        return self.__project_name

    @project_name.setter
    def project_name(self, project_name):
        if project_name is None:
            self.__project_name = self.__project_name
        else:
            if not isinstance(project_name, Text):
                raise TestKeeperArgvCheckException(f"参数project_name:{project_name}，类型错误，应当为str类型！")
            self.__project_name = project_name

    @property
    def plan_status_id(self):
        return self.__plan_status_id

    @plan_status_id.setter
    def plan_status_id(self, plan_status_id):
        if plan_status_id is None:
            raise TestKeeperArgvCheckException(f"参数plan_status_id:{plan_status_id},不能为None！")
        else:
            if not isinstance(plan_status_id, int):
                raise TestKeeperArgvCheckException(f"参数plan_status_id:{plan_status_id},类型错误，应当为int类型！")
            self.__plan_status_id = plan_status_id

    @property
    def plan_id(self):
        return self.__plan_id

    @plan_id.setter
    def plan_id(self, plan_id):
        if plan_id is None:
            raise TestKeeperArgvCheckException(f"参数planId:{plan_id},不能为None！")
        else:
            try:
                logger.info(plan_id)
                self.__plan_id = int(plan_id)
            except Exception as e:
                logger.error(e)
                raise TestKeeperArgvCheckException(f"参数planId:{plan_id},类型错误，应当为int类型！")

    def update_test_plan_status(self, name: str, value: str):
        self.common_update_method(TestPlanStatusTable, self.__plan_status_id, name, value)

    def delete_test_plan_status(self):
        self.mul_session.query(TestPlanStatusTable).filter_by(id=self.__plan_status_id).delete()
        self.mul_session.query(TestJobStatusTable).filter_by(planStatusId=self.__plan_status_id).delete()
        self.mul_session.commit()
        logger.info(f"删除测试计划状态成功:{self.__plan_status_id}")

    def get_test_plan_status_list(self):
        if self.__project_name is not None:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.mul_session.query(TestPlanStatusTable).filter(
                                         TestPlanTable.projectName == self.__project_name).limit(self.__limit).all()]
        else:
            test_plan_status_list = [test_plan.__repr__() for test_plan in
                                     self.mul_session.query(TestPlanStatusTable).filter().limit(self.__limit).all()]
        return test_plan_status_list

    def generate_test_plan_status_table_obj(self, test_plan: TestPlanTable,
                                            execute_status: ExecuteStatus) -> TestPlanStatusTable:
        now_time = datetime.datetime.now()
        test_plan_status_table_obj = TestPlanStatusTable(
            planName=test_plan.planName,
            planId=test_plan.id,
            executeStatus=execute_status,
            updateTime=now_time,
            createTime=now_time
        )
        self.mul_session.add(test_plan_status_table_obj)
        return test_plan_status_table_obj

    def get_plan_status_table(self) -> TestPlanStatusTable:
        plan_status_table_obj = self.mul_session.query(TestPlanStatusTable).filter_by(id=self.__plan_status_id).first()
        return plan_status_table_obj

    def get_plan_status_table_obj(self) -> TestPlanStatusTable:
        plan_status_table_obj = self.mul_session.query(TestPlanStatusTable).filter_by(id=self.__plan_status_id)
        return plan_status_table_obj

    def get_plan_status_table_obj_by_plan_id(self) -> TestPlanStatusTable:
        plan_status_table_obj = self.mul_session.query(TestPlanStatusTable).filter_by(planId=self.__plan_id).first()
        return plan_status_table_obj
