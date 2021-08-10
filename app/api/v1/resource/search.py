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


@router.get("/search", summary="检索")
async def top(words: str, count: Optional[int] = 10):
    """
    检索 \n
    return: 检索结果
    """
    es_req = EastMoneyRequest()
    results = es_req.search(words)
    return response_code.resp_200(results[0:count])
