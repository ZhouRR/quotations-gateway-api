#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 17:44
# @Author  : CoderCharm
# @File    : __init__.py.py
# @Software: PyCharm
# @Desc    :
"""

路由汇总

"""

from fastapi import APIRouter
from app.api.v1.profile import profile
from app.api.v1.auth import auth

from app.api.v1.resource import calendar, search, indices, block, stock


api_v1 = APIRouter()

api_v1.include_router(auth.router, tags=["Auth"])
api_v1.include_router(profile.router, tags=["Profile"])

api_v1.include_router(calendar.router, tags=["Calendar"])
api_v1.include_router(search.router, tags=["Search"])
api_v1.include_router(indices.router, tags=["Index"])
api_v1.include_router(block.router, tags=["Block"])
api_v1.include_router(stock.router, tags=["Stock"])
