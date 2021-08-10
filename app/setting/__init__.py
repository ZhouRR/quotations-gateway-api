#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 17:37
# @Author  : CoderCharm
# @File    : __init__.py.py
# @Software: PyCharm
# @Desc    :
"""
配置文件
根据环境变量 区分生产开发
"""

import pydantic.dataclasses
import pydantic.version
import pydantic.color
import colorsys
import pydantic.types
import pydantic.validators
import pydantic.datetime_parse
import pydantic.main
import pydantic.parse
import pydantic.networks
import pydantic.decorator
import pydantic.env_settings
import pydantic.tools

import passlib
import passlib.handlers.bcrypt

import os
import app.setting.development_config

# 获取环境变量
env = os.getenv("PRODUCTION", "")
if env:
    # 如果有虚拟环境 则是 生产环境
    from .app_config import configs
    configs.production = True
else:
    # 没有则是开发环境
    from .development_config import configs
    configs.production = False
