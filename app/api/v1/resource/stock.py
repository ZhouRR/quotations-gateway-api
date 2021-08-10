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


@router.get("/stock/top/{tp}", summary="排行榜")
async def top(tp: str, count: Optional[int] = 10, num: Optional[int] = 1):
    """
    排行榜 \n
    return: 排行榜行情
    """
    es_req = EastMoneyRequest()
    if tp == "rise":
        results = es_req.stock_top(count=count, num=num)
    elif tp == "fell":
        results = es_req.stock_top(rise=0, count=count, num=num)
    elif tp == "turnover":
        results = es_req.stock_top(rise=1, turnover=True, count=count, num=num)
    elif tp == "quantity":
        results = es_req.stock_top(rise=1, quantity=True, count=count, num=num)
    elif tp == "options":
        results = es_req.stock_top(rise=1, options=True, count=count, num=num)
    else:
        results = []
    return response_code.resp_200(results)


@router.get("/stock/{code}", summary="个股信息")
async def detail(code: str):
    """
    排行榜 \n
    return: 排行榜行情
    """
    es_req = EastMoneyRequest()
    return response_code.resp_200(es_req.stock_detail(code))


@router.get("/stock/{code}/minutely", summary="分时行情")
async def minutely(code: str):
    """
    排行榜 \n
    return: 排行榜行情
    """
    es_req = EastMoneyRequest()
    return response_code.resp_200(es_req.stock_minutely(code))


@router.get("/stock/{code}/history", summary="历史行情")
async def history(code: str, tp: Optional[str] = "daily",
                  beg: Optional[str] = "19700101", end: Optional[str] = "", count: Optional[int] = 50):
    """
    历史行情 \n
    return: 历史行情
    """
    es_req = EastMoneyRequest()
    tp_value = 101
    if tp == "daily":
        tp_value = 101
    elif tp == "weekly":
        tp_value = 102
    elif tp == "monthly":
        tp_value = 103
    elif tp == "yearly":
        tp_value = 104
    elif tp == "5minutely":
        tp_value = 5
    elif tp == "15minutely":
        tp_value = 15
    elif tp == "30minutely":
        tp_value = 30
    elif tp == "60minutely":
        tp_value = 60
    else:
        response_code.resp_404("not found")
    return response_code.resp_200(es_req.stock_history(code, tp_value, beg, end, count))
