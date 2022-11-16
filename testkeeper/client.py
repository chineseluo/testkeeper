#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 21:13
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : client.py
@IDE     : PyCharm
------------------------------------
"""
import sys
import argparse
from loguru import logger
from testkeeper import __version__, __description__
from testkeeper.builtin.testkeeper_conf import TestKeeperConf
from testkeeper.service.plan_service import PlanService
from testkeeper.util.logger_operation import LoggerFormat

plan_service = PlanService()


def plan_show(*args, **kwargs):
    """
    显示所有测试计划配置
    :param args:
    :param kwargs:
    :return:
    """
    title = "PLAN CONFIG LIST SHOW ** 计划配置列表展示"
    if args[0].project_name is not None and args[0].limit is not None:
        LoggerFormat.console_pretty_table(title,
                                          plan_service.get_test_plan_list(args[0].project_name, int(args[0].limit)))
    elif args[0].project_name is None and args[0].limit is not None:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_plan_list(limit=args[0].limit))
    elif args[0].project_name is not None and args[0].limit is None:
        LoggerFormat.console_pretty_table(title,
                                          plan_service.get_test_plan_list(project_name=args[0].project_name))
    else:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_plan_list())


def plan_load(*args, **kwargs):
    """
    从yml中加载测试计划
    :param args:
    :param kwargs:
    :return:
    """
    logger.info("test")


def plan_update(*args, **kwargs):
    """
    更新测试计划配置中的字段
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.update_test_plan(args[0].plan_id, args[0].name, args[0].value)


def plan_delete(*args, **kwargs):
    """
    删除测试计划配置，对应计划下job和step配置数据也删除
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.delete_test_plan(args[0].plan_id)


def plan_start(*args, **kwargs):
    """
    执行测试计划，生成测试计划/任务/步骤状态信息
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.execute_test_plan(args[0].plan_id)


def job_start(*args, **kwargs):
    plan_service.start_test_job(args[0].job_id)


def plan_stop(*args, **kwargs):
    """
    停止正在运行的测试计划，根据plan_status_id进行停止
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.stop_test_plan(args[0].plan_status_id)


def job_stop(*args, **kwargs):
    """
    停止正在运行的测试任务，根据job_status_id进行停止
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.stop_test_job(args[0].job_status_id)


def step_start(*args, **kwargs):
    """
    运行测试步骤，根据step_status_id运行，运行测试步骤会生成一条job_status，以及一条plan_status数据
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.start_test_step(args[0].step_id)


def step_stop(*args, **kwargs):
    """
    停止正在运行的测试步骤，根据step_status_id进行停止
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.stop_test_step(args[0].step_status_id)


def job_add(*args, **kwargs):
    """
    添加测试job配置
    :param args:
    :param kwargs:
    :return:
    """
    logger.info("test")


def job_delete(*args, **kwargs):
    """
    删除测试job配置，及对应step配置
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.delete_test_job(args[0].job_id)


def job_update(*args, **kwargs):
    """
    更新测试任务中的字段
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.update_test_job(args[0].job_id, args[0].name, args[0].value)


def job_show(*args, **kwargs):
    """
    查询所有测试任务配置
    :param args:
    :param kwargs:
    :return:
    """
    title = "JOB CONFIG LIST SHOW ** 任务配置列表展示"
    if args[0].plan_id is not None:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_job_list(args[0].plan_id))
    else:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_job_list())


def step_show(*args, **kwargs):
    """
    查询所有测试步骤配置
    :param args:
    :param kwargs:
    :return:
    """
    title = "STEP CONFIG LIST SHOW ** 步骤配置列表展示"
    if args[0].job_id is not None:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_step_list(args[0].job_id))
    else:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_step_list())


def step_update(*args, **kwargs):
    """
    更新测试步骤中的字段
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.update_test_step(args[0].step_id, args[0].name, args[0].value)


def step_delete(*args, **kwargs):
    """
    删除测试步骤
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.delete_test_step(args[0].step_id)


def plan_status_show(*args, **kwargs):
    """
    展示所有执行的测试计划，状态信息
    :param args:
    :param kwargs:
    :return:
    """
    title = "PLAN STATUS LIST SHOW ** 计划执行状态列表展示"
    if args[0].project_name is not None and args[0].limit is not None:
        LoggerFormat.console_pretty_table(title,
                                          plan_service.get_test_plan_status_list(args[0].project_name,
                                                                                 int(args[0].limit)))
    elif args[0].project_name is None and args[0].limit is not None:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_plan_status_list(limit=args[0].limit))
    elif args[0].project_name is not None and args[0].limit is None:
        LoggerFormat.console_pretty_table(title,
                                          plan_service.get_test_plan_status_list(project_name=args[0].project_name))
    else:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_plan_status_list())


def plan_status_delete(*args, **kwargs):
    """
    删除测试运行状态
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.delete_test_plan_status(args[0].plan_status_id)


def job_status_delete(*args, **kwargs):
    """
    删除测试任务运行状态
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.delete_test_job_status(args[0].job_status_id)


def step_status_delete(*args, **kwargs):
    """
    删除测试步骤运行状态
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.delete_test_step_status(args[0].step_status_id)


def plan_status_update(*args, **kwargs):
    """
    更新测试计划执行状态
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.update_test_plan_status(args[0].plan_status_id, args[0].name, args[0].value)


def job_status_show(*args, **kwargs):
    """
    显示所有任务状态信息
    :param args:
    :param kwargs:
    :return:
    """
    title = "JOB EXECUTE STATUS LIST SHOW ** 任务执行状态列表展示"
    if args[0].plan_id is not None:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_job_status_list(args[0].plan_id))
    else:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_job_status_list())


def job_status_update(*args, **kwargs):
    """
    更新任务执行状态信息
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.update_test_job_status(args[0].job_status_id, args[0].name, args[0].value)


def step_status_show(*args, **kwargs):
    """
    显示所有步骤状态信息
    :param args:
    :param kwargs:
    :return:
    """
    title = "STEP EXECUTE STATUS LIST SHOW ** 步骤执行状态列表展示"
    if args[0].job_status_id is not None:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_step_status_list(args[0].job_status_id))
    else:
        LoggerFormat.console_pretty_table(title, plan_service.get_test_step_status_list())


def step_status_update(*args, **kwargs):
    """
    更新步骤执行状态信息
    :param args:
    :param kwargs:
    :return:
    """
    plan_service.update_test_step_status(args[0].step_status_id, args[0].name, args[0].value)


def get_local_machine_metric(*args, **kwargs):
    ...


def init_scaffold_parser(subparsers):
    testkeeper_cmd_conf = TestKeeperConf().testkeeper_client_conf
    sub_scaffold_parser_list = []
    for parent_cmd_info in testkeeper_cmd_conf["parameters"]:
        parent_cmd = parent_cmd_info['parent_cmd']
        sub_scaffold_parser = subparsers.add_parser(
            f"{parent_cmd['param_name']}", help=f"{parent_cmd['help']}",
        )
        sub_scaffold_parser.set_defaults(func=eval(parent_cmd['func']))
        if "children_cmd" in parent_cmd:
            for children_cmd_info in parent_cmd['children_cmd']:
                sub_scaffold_parser.add_argument(*children_cmd_info["param_name"],
                                                 type=eval(children_cmd_info["type"]), nargs="?",
                                                 help=children_cmd_info["help"],
                                                 default=eval(children_cmd_info["default"]),
                                                 dest=children_cmd_info["dest"])
            sub_scaffold_parser_list.append(sub_scaffold_parser)
    return sub_scaffold_parser_list


def print_child_help(sub_scaffold_parser_list, argv_list, argv_index):
    for sub_scaffold_parser in sub_scaffold_parser_list:
        if sub_scaffold_parser.prog.__contains__(argv_list[argv_index]):
            sub_scaffold_parser.print_help()


def entry():
    tk_argv = sys.argv
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-v", "-V", "--version", "--Version", help="show version", default=__version__)
    subparsers = parser.add_subparsers(help="TK cmd sub-command help")
    sub_scaffold_parser_list = init_scaffold_parser(subparsers)
    if len(tk_argv) == 1:
        parser.print_help()
        sys.exit()
    elif len(tk_argv) == 2:
        if tk_argv[1] in ["-V", "-v", "--Version", "--version"]:
            print(f"""
             +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +++ +-+
             | T | | E | | S | | T | | K | | E | | E | | P | | E | | R |
             +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +++ +-+
            """)
            logger.info(f"The testkeeper version is {__version__}")
        elif tk_argv[1] in ["-h", "-H", "--help", "--Help"]:
            parser.print_help()
        else:
            args = parser.parse_args()
            try:
                args.func(args)
            except Exception as e:
                print_child_help(sub_scaffold_parser_list, tk_argv, 1)
                raise Exception(f"参数传递错误，异常信息{e}")
    elif len(tk_argv) == 3:
        if tk_argv[2] in ["-h", "-H", "--help", "--Help"]:
            print_child_help(sub_scaffold_parser_list, tk_argv, 1)
        else:
            print_child_help(sub_scaffold_parser_list, tk_argv, 1)
    else:
        logger.info(tk_argv)
        args = parser.parse_args()
        try:
            args.func(args)
        except Exception as e:
            print_child_help(sub_scaffold_parser_list, tk_argv, 1)
            raise Exception(f"参数传递错误，异常信息{e}")
    sys.exit(0)


if __name__ == '__main__':
    ...
