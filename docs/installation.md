# 安装

OpenSourceTest使用python开发，它支持在Python3.8+版本和大多数操作系统。

## 安装

TestKeeper在PyPI官方仓库中，可以通过pip安装（推荐使用豆瓣源安装）

~~~bash
pip install testkeeper -i https://pypi.douban.com/simple
~~~

如果您以前安装的TestKeeper过老，并且想要升级到最新版本，则可以使用-U选项。

~~~bash
pip install -U testkeeper
~~~

## 检查安装

安装TestKeeper后，系统将添加三个命令。在TestKeeper中TK命令等价于tk、testkeeper、TestKeeper。

- 1、TK -V：查看TestKeeper版本号（使用时：[-V|-v|--Version|--version"]等价）
- 2、TK -h：查看TestKeeper帮助说明（使用时：[-h|-H|--help|--Help]等价）
- 3、TK onlinedocs：查看TestKeeper在线文档地址
- 4、TK start_ui_project -h：查看创建ui项目时的帮助说明（使用时：[-h|-H|--help|--Help]等价）
- 5、TK start_ui_project [project_name]：创建ui自动化项目，[project_name]自定义
- 6、TK start_http_project -h：查看创建接口项目时的帮助说明（使用时：[-h|-H|--help|--Help]等价）
- 7、TK start_http_project [project_name]：创建接口自动化项目，[project_name]自定义
- 8、TK start_app_project [project_name]：创建app自动化项目，[project_name]自定义
- 6、TK start_app_project -h：查看创建app自动化项目时的帮助说明（使用时：[-h|-H|--help|--Help]等价）

检查TestKeeper版本：

~~~bash
TK -V
~~~
~~~bash
chineseluodeMacBook-Pro:~ chineseluo$ TK -v

             +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +++ +-+
             | T | | E | | S | | T | | K | | E | | E | | P | | E | | R |
             +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +++ +-+

2022-11-22 16:09:31.532 | INFO     | testkeeper.client:entry:362 - The testkeeper version is 0.1.0
~~~

查看可用选项，请运行：

~~~bash
TK -h
~~~

~~~bash
chineseluodeMacBook-Pro:~ chineseluo$ TK -h
usage: TK [-h] [-v VERSION]
          {plan_load,plan_show,plan_update,plan_stop,plan_delete,plan_start,job_add,job_delete,job_start,job_stop,job_update,job_show,step_show,step_update,plan_status_show,plan_status_update,plan_status_delete,job_status_show,job_status_delete,job_status_update,step_status_show,step_status_update,step_status_delete,step_start,step_stop,get_local_machine_metric}
          ...

测试任务管理

positional arguments:
  {plan_load,plan_show,plan_update,plan_stop,plan_delete,plan_start,job_add,job_delete,job_start,job_stop,job_update,job_show,step_show,step_update,plan_status_show,plan_status_update,plan_status_delete,job_status_show,job_status_delete,job_status_update,step_status_show,step_status_update,step_status_delete,step_start,step_stop,get_local_machine_metric}
                        TK cmd sub-command help
    plan_load           加载测试计划
    plan_show           查询测试计划列表，展示配置信息
    plan_update         更新测试计划配置
    plan_stop           更新测试计划配置
    plan_delete         删除测试计划配置
    plan_start          执行测试计划
    job_add             测试计划
    job_delete          删除测试计划
    job_start           删除测试计划
    job_stop            删除测试计划
    job_update          更新测试任务
    job_show            显示测试任务
    step_show           显示测试任务
    step_update         修改测试步骤配置
    plan_status_show    显示测试任务
    plan_status_update  修改测试计划状态
    plan_status_delete  修改测试计划状态
    job_status_show     显示测试任务
    job_status_delete   显示测试任务
    job_status_update   显示测试任务
    step_status_show    显示测试步骤状态
    step_status_update  显示测试任务
    step_status_delete  显示测试任务
    step_start          执行测试计划
    step_stop           执行测试计划
    get_local_machine_metric 获取本机资源信息

optional arguments:
  -h, --help            show this help message and exit
  -v VERSION, -V VERSION, --version VERSION, --Version VERSION
                        show version
~~~
