#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 17:36
# @Author  : CoderCharm
# @File    : __init__.py.py
# @Software: PyCharm
# @Desc    :
"""
模仿flask 工厂模式目录结构

"""
import traceback

import app.api.v1.profile


from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_v1
from app.extensions import logger
from app.setting import configs
from app.utils.custom_exc import PostParamsError, TokenAuthError  # 自定义异常

# swagger 文档分类 https://fastapi.tiangolo.com/tutorial/metadata/
tags_metadata = [
    {
        "name": "sample",
        "description": "",
    },
]


def create_app():
    fast_app = FastAPI(
        title="FastAPI",
        description="",
        version="1.0.0",
        docs_url=configs.DOCS_URL,
        openapi_url=configs.OPENAPI_URL,
        redoc_url=configs.REDOC_URL,
        openapi_tags=tags_metadata
    )

    url_prefix = configs.URL_PREFIX

    fast_app.include_router(
        api_v1,
        prefix=url_prefix + "/api/v1",
        # tags=["items"],
        # dependencies=[Depends(get_token_header)],
        # responses={404: {"description": "Not found"}},
    )

    register_exception(fast_app)  # 注册捕获异常信息
    register_cors(fast_app)  # 跨域设置
    register_middleware(fast_app)
    register_orm(fast_app)
    return fast_app


def register_exception(fast_app: FastAPI):
    """
    全局异常捕获
    :param fast_app:
    :return:
    """

    # 捕获自定义异常
    @fast_app.exception_handler(PostParamsError)
    async def query_params_exception_handler(request: Request, exc: PostParamsError):
        """
        捕获 自定义抛出的异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"参数查询异常\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"code": 400, "data": {"tip": exc.err_desc}, "message": "fail"},
        )

    @fast_app.exception_handler(TokenAuthError)
    async def token_exception_handler(request: Request, exc: TokenAuthError):
        logger.error(f"参数查询异常\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"code": 400, "data": None, "message": exc.err_desc},
        )

    # 捕获参数 验证错误
    @fast_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        捕获请求参数 验证错误
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"参数错误\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"code": 400, "data": {"tip": exc.errors()}, "body": exc.body, "message": "fail"}),
        )

    # 捕获全部异常
    @fast_app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        try:
            logger.error(f"全局异常\nURL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc(exc)}")
        except TypeError as e:
            logger.error(f"全局异常\nURL:{request.url}\nHeaders:{request.headers}\n{exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "data": {"tip": "服务器错误"}, "message": "failed"},
        )


def register_cors(fast_app: FastAPI):
    """
    支持跨域

    貌似发现了一个bug
    https://github.com/tiangolo/fastapi/issues/133

    :param fast_app:
    :return:
    """

    fast_app.add_middleware(
        CORSMiddleware,
        # allow_origins=['http://localhost:8081'],  # 有效, 但是本地vue端口一直在变化, 接口给其他人用也不一定是这个端口
        # allow_origins=['*'],   # 无效 bug allow_origins=['http://localhost:8081']
        allow_origin_regex='https?://.*',  # 改成用正则就行了
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_middleware(fast_app: FastAPI):
    """
    请求响应拦截 hook

    https://fastapi.tiangolo.com/tutorial/middleware/
    :param fast_app:
    :return:
    """

    @fast_app.middleware("http")
    async def logger_request(request: Request, call_next):
        # https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
        logger.info(f"request:{request.method} url:{request.url}\nheaders:{request.headers.get('user-agent')}"
                    f"\nIP:{request.client.host}")

        response = await call_next(request)
        return response


def register_orm(fast_app: FastAPI) -> None:
    # configs = {
    #     "connections": {"default": configs.DB_ADDRESS},
    #     "apps": {
    #         "models": {
    #             "models": ["app.api.v1.models"],
    #             "default_connection": "default"
    #         }
    #     },
    # }
    # register_tortoise(fast_app, config=configs)
    pass
