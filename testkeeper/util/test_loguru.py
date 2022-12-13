import logging
import sys
from pathlib import Path
from flask import Flask
from loguru import logger, _defaults

app = Flask(__name__)
class InterceptHandler(logging.Handler):
    def emit(self, record):
        loggerlogger_opt = logger.opt(depth=6, exception=record.exc_info)
        loggerlogger_opt.log(record.levelname, record.getMessage())
def configure_logging(flask_app: Flask):
    #配置日志
    path = Path(flask_app.config['LOG_PATH'])
    if not path.exists():
        path.mkdir(parents=True)
    log_name = Path(path, 'sips.log')
    logging.basicConfig(handlers=[InterceptHandler(level='INFO')], level='INFO')
    # 配置日志到标准输出流
    logger.configure(handlers=[{"sink": sys.stderr, "level": 'INFO'}])
    # 配置日志到输出到文件
    logger.add(log_name, rotation="500 MB", encoding='utf-8', colorize=False, level='INFO')

#实现日志的刷新重新写入操作
def add(self, sink, *,
    level=_defaults.LOGURU_LEVEL, format=_defaults.LOGURU_FORMAT,
    filter=_defaults.LOGURU_FILTER, colorize=_defaults.LOGURU_COLORIZE,
    serialize=_defaults.LOGURU_SERIALIZE, backtrace=_defaults.LOGURU_BACKTRACE,
    diagnose=_defaults.LOGURU_DIAGNOSE, enqueue=_defaults.LOGURU_ENQUEUE,
    catch=_defaults.LOGURU_CATCH, **kwargs
):
    trace = logger.add('runtime.log')
    logger.debug('this is a debug message')
    logger.remove(trace)
    logger.debug('this is another debug message')
