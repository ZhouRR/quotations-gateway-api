#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 15:50
# @Author  : CoderCharm
# @File    : logger.py
# @Software: PyCharm
# @Desc    :
"""

日志文件配置

# 本来是想 像flask那样把日志对象挂载到app对象上，作者建议直接使用全局对象
https://github.com/tiangolo/fastapi/issues/81#issuecomment-473677039

"""

import os
import time
from loguru import logger

# 获取环境变量
from app.setting import configs

basedir = configs.LOG_PATH

# 定位到log日志文件
log_path = os.path.join(basedir, 'logs')

if os.path.exists(log_path):
    # import shutil
    # shutil.rmtree(log_path)
    pass

if not os.path.exists(log_path):
    # os.mkdir(log_path)
    pass

log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}.log')

# 日志简单配置
# logger.add(log_path_error, rotation="12:00", retention="5 days", enqueue=True)


__all__ = ["logger"]


def error(param):
    try:
        return logger.error(param)
    except UnicodeEncodeError as e:
        logger.error("cant encode character")


def info(param):
    try:
        return logger.info(param)
    except UnicodeEncodeError as e:
        logger.error("cant encode character")
