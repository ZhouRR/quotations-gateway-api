#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 10:15
# @Author  : CoderCharm
# @File    : production_config.py
# @Software: PyCharm
# @Desc    :
"""

生产环境
服务器上设置 ENV 环境变量

"""
import os
from typing import Optional

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    #
    HOST: str = os.getenv("HOST", "127.0.0.1")
    #
    PORT: int = os.getenv("PORT", 8090)
    URL_PREFIX: str = os.getenv("URL_PREFIX", "/quotations")
    # 文档地址 生产环境可以关闭 None
    DOCS_URL: Optional[str] = URL_PREFIX + "/api/v1/docs"
    # 文档关联请求数据接口 生产环境可以关闭 None
    OPENAPI_URL: Optional[str] = URL_PREFIX + "/api/v1/openapi.json"
    # 禁用 redoc 文档
    REDOC_URL: Optional[str] = None

    # log address
    LOG_PATH = os.path.abspath('./logs')

    EAST_MONEY_URL = os.getenv("EAST_MONEY_URL", "http://7.push2.eastmoney.com")
    EAST_MONEY_HISTORY_URL = os.getenv("EAST_MONEY_HISTORY_URL", "http://push2his.eastmoney.com")
    EAST_MONEY_SEARCH_URL = os.getenv("EAST_MONEY_SEARCH_URL", "https://searchapi.eastmoney.com")
    EAST_MONEY_DATA_INTERFACE = os.getenv("EAST_MONEY_DATA_INTERFACE", "http://datainterface.eastmoney.com")

    REQUEST_TIMEOUT: int = os.getenv("REQUEST_TIMEOUT", 10)
    JSON_HEADERS = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    production = False


configs = BaseConfig()
