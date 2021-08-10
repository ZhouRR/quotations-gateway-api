#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/05/07 17:48
# @Author  :
# @File    : company.py
# @Software: PyCharm
# @Desc    :
"""

"""
from typing import Optional

from fastapi import APIRouter

from app.core.quotations_fix.eastmoney_req import EastMoneyRequest
from app.utils import response_code

router = APIRouter()


@router.get("/calendar", summary="交易日历")
async def calendar(date: Optional[str] = None, time: Optional[str] = None, count: Optional[int] = 5,
                   num: Optional[int] = 1):
    """
    交易日历 \n
    return: 是否交易日
    """
    es_req = EastMoneyRequest()
    return response_code.resp_200(es_req.calendar(date, time, count, num))
