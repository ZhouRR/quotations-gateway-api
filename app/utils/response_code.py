#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/19 16:12
# @Author  : CoderCharm
# @File    : response_code.py
# @Software: PyCharm
# @Desc    :
"""
定义返回的状态

# 看到文档说这个orjson 能压缩性能(squeezing performance)
https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse

It's possible that ORJSONResponse might be a faster alternative.

# 安装
pip install --upgrade orjson

测试了下，序列化某些特殊的字段不友好，比如小数
TypeError: Type is not JSON serializable: decimal.Decimal
"""
from mimetypes import guess_type
from urllib.parse import quote

from fastapi import status
from fastapi.responses import JSONResponse, Response, ORJSONResponse

from typing import Union


def resp_200(data: Union[list, dict, str] = None, *, message: str = "Success") -> dict:
    return {
        'code': 200,
        'message': message,
        'data': data,
    }


def resp_400(data: str = None) -> Response:
    return ORJSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            'code': 400,
            'message': "Invalid Parameters",
            'data': data,
        }
    )


def resp_403(data: str = None) -> Response:
    return ORJSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            'code': 403,
            'message': "Forbidden",
            'data': data,
        }
    )


def resp_404(data: str = None) -> Response:
    return ORJSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'code': 404,
            'message': "Page Not Found",
            'data': data,
        }
    )


def resp_500(data: str = None) -> Response:
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'code': "500",
            'message': "Server internal error",
            'data': data,
        }
    )


def resp_file(data: Union[list, dict, str] = None, filename: str = "default.txt") -> Response:
    headers = {}
    content_disposition_filename = quote(filename)
    if content_disposition_filename != filename:
        content_disposition = "attachment; filename*=utf-8''{}".format(
            content_disposition_filename
        )
    else:
        content_disposition = 'attachment; filename="{}"'.format(filename)
    headers.setdefault("content-disposition", content_disposition)
    return Response(content=data, media_type=guess_type(filename)[0] or "text/plain", headers=headers)


# 自定义
def resp_5000(data: Union[list, dict, str]) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 5000,
            'message': "Token failure",
            'data': data,
        }
    )
