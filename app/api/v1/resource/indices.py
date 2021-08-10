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


@router.get("/indices", summary="指数")
async def indices():
    """
    指数 \n
    return: 指数行情
    """
    es_req = EastMoneyRequest()
    results = es_req.indices_quotations(["1.000001", "0.399001", "0.399006"])

    return response_code.resp_200(results)


@router.get("/indices/{code}/stocks", summary="个股列表")
async def stocks(code: str, count: Optional[int] = 10, num: Optional[int] = 1):
    """
    个股列表 \n
    return: 个股列表
    """
    es_req = EastMoneyRequest()
    return response_code.resp_200(es_req.indices_stocks(code, count, num))
