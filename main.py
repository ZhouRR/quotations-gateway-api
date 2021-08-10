#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 17:36
# @Author  : CoderCharm
# @File    : main.py
# @Software: PyCharm
# @Desc    :

import app.api
import app.core
import app.extensions
import app.utils
import app.setting

from app.api import create_app
from app.setting import configs

fast_app = create_app()


def run_production():
    import asyncio
    import uvloop
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    corn_config = Config()
    corn_config.bind = ['%s:%s' % (configs.HOST, configs.PORT)]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(serve(fast_app, corn_config))
    pass


def run_development():
    import uvicorn
    uvicorn.run(app='main:fast_app', host=configs.HOST, port=configs.PORT, workers=1, reload=False, debug=False)
    pass


if __name__ == "__main__":
    if configs.production:
        run_production()
    else:
        run_development()
