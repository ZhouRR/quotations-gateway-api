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


@router.get("/block/{code}", summary="三大板块")
async def block(code: str, count: Optional[int] = 3, num: Optional[int] = 1):
    """
    板块 \n
    return: 板块行情
    """
    es_req = EastMoneyRequest()
    if code == 'C._BK_HY':
        block_ls = es_req.block_quotations(2, count=count, num=num)
        results = {
            "name": "行业板块",
            "code": "C._BK_HY",
            "blockList": block_ls
        }
    elif code == 'C._BK_GN':
        block_ls = es_req.block_quotations(3, count=count, num=num)
        results = {
            "name": "概念板块",
            "code": "C._BK_GN",
            "blockList": block_ls
        }
    elif code == 'C._BK_DY':
        block_ls = es_req.block_quotations(1, count=count, num=num)
        results = {
            "name": "地域板块",
            "code": "C._BK_DY",
            "blockList": block_ls
        }
    else:
        results = {
            "name": "",
            "code": "",
            "blockList": []
        }
    return response_code.resp_200(results)


@router.get("/block/{code}/stocks", summary="个股列表")
async def stocks(code: str, count: Optional[int] = 10, num: Optional[int] = 1):
    """
    个股列表 \n
    return: 排行榜行情
    """
    es_req = EastMoneyRequest()
    return response_code.resp_200(es_req.block_stocks(code, count, num))
