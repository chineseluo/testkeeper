#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 21:01
@Auth    : luozhongwen
@Email   : luozhongwen@sensorsdata.cn
@File    : system_info.py
@IDE     : PyCharm
------------------------------------
"""
import os
import psutil
from loguru import logger
from testkeeper.util.shell_utils import ShellClient


class SystemInfo:

    @staticmethod
    def get_cpu_count():
        return psutil.cpu_count()

    @staticmethod
    def get_memory_info():
        return psutil.virtual_memory()

    @staticmethod
    def get_total_memory():
        total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))
        used = str(round(psutil.virtual_memory().used / (1024.0 * 1024.0 * 1024.0), 2))
        free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))
        return total, used, free

    @staticmethod
    def get_disk_info():
        disk_info = psutil.disk_usage("/")
        total = str(round(disk_info.total / (1024.0 * 1024.0 * 1024.0), 2))
        used = str(round(disk_info.used / (1024.0 * 1024.0 * 1024.0), 2))
        free = str(round(disk_info.free / (1024.0 * 1024.0 * 1024.0), 2))
        return total, used, free

    @staticmethod
    def get_current_sys_user_info():
        return psutil.users()

    @staticmethod
    def get_all_process_pid():
        return psutil.pids()

    @staticmethod
    def get_all_process():
        for item in psutil.process_iter(attrs=["pid", "cmd"]):
            logger.info(item)
        return psutil.process_iter()

    @staticmethod
    def get_process_status():
        pid = SystemInfo.get_process_by_os()
        process_is_exists = psutil.pid_exists(int(pid.strip()))
        process_is_status = psutil.Process(int(pid.strip())).status()
        return process_is_exists, process_is_status

    @staticmethod
    def get_process_by_os():
        shell_client = ShellClient()
        pid = shell_client.check_output('ps -ef|grep "echo test" | grep -v grep | awk' + " '{print $2}'")
        return pid


if __name__ == '__main__':
    logger.info(SystemInfo.get_cpu_count())
    logger.info(SystemInfo.get_disk_info())

    logger.info(SystemInfo.get_total_memory())
    logger.info(SystemInfo.get_process_status())
