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
    if args[0].project_name is not None and args[0].limit is not None:
        LoggerFormat.console_pretty_table("plan show",
                                          plan_service.get_test_plan_list(args[0].project_name, int(args[0].limit)))
    elif args[0].project_name is None and args[0].limit is not None:
        LoggerFormat.console_pretty_table("plan list show", plan_service.get_test_plan_list(limit=args[0].limit))
    elif args[0].project_name is not None and args[0].limit is None:
        LoggerFormat.console_pretty_table("plan list show",
                                          plan_service.get_test_plan_list(project_name=args[0].project_name))
    else:
        LoggerFormat.console_pretty_table("plan list show", plan_service.get_test_plan_list())


def plan_load(*args, **kwargs):
    logger.info("test")


def plan_update(*args, **kwargs):
    plan_service.update_test_plan(args[0].plan_id, args[0].name, args[0].value)


def plan_delete(*args, **kwargs):
    plan_service.delete_test_plan(args[0].plan_id)


def plan_start(*args, **kwargs):
    plan_service.execute_test_plan(args[0].plan_id)


def job_add(*args, **kwargs):
    logger.info("test")


def job_delete(*args, **kwargs):
    logger.info("test")


def job_update(*args, **kwargs):
    logger.info("test")


def job_show(*args, **kwargs):
    if args[0].plan_id is not None:
        LoggerFormat.console_pretty_table("job list show", plan_service.get_test_job_list(args[0].plan_id))
    else:
        LoggerFormat.console_pretty_table("job list show", plan_service.get_test_job_list())


def plan_status_show(*args, **kwargs):
    ...


def plan_status_update(*args, **kwargs):
    ...


def job_status_show(*args, **kwargs):
    ...


def job_status_update(*args, **kwargs):
    ...


def step_status_show(*args, **kwargs):
    ...


def step_status_update(*args, **kwargs):
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
        for children_cmd_info in parent_cmd['children_cmd']:
            sub_scaffold_parser.add_argument(*children_cmd_info["param_name"],
                                             type=eval(children_cmd_info["type"]), nargs="?",
                                             help=children_cmd_info["help"], default=eval(children_cmd_info["default"]),
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
