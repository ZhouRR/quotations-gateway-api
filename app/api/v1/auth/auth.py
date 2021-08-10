#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/03/31 17:48
# @Author  :
# @File    : auth.py
# @Software: PyCharm
# @Desc    :
"""

"""
from fastapi import APIRouter

from app.utils import response_code

router = APIRouter()


@router.get("/auth/token", summary="获取Token")
async def auth_token():
    """
    获取Token \n
    return: token
    """
    return response_code.resp_404()
