#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:58
@Auth    : luozhongwen
@Email   : luozhongwen@sensorsdata.cn
@File    : machine_service.py
@IDE     : PyCharm
------------------------------------
"""

from testkeeper.util.system_info import SystemInfo


class MachineService:

    def show_testkeeper_machine_info(self):
        return SystemInfo.get_local_metric()
