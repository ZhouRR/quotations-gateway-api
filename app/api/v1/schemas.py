#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/8 11:33
# @Author  : CoderCharm
# @File    : schemas.py
# @Software: PyCharm
# @Desc    :
"""

验证参数

"""
import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """
    好友
    """
    username: str
    action: int = 1


class UserLogin(BaseModel):
    """
    用户登录
    """
    username: str
    password: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class Sentence(BaseModel):
    """

    """
    title: str
    content: str
