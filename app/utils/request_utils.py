import json

import grequests
import requests

from app.extensions import logger
from app.setting import configs


def err_handler(request, exception):
    logger.error(request.url)
    logger.error(exception)


def single_request(method, url, **kwargs):
    logger.info(url)
    return requests.request(method,
                            url=url,
                            timeout=configs.REQUEST_TIMEOUT,
                            **kwargs)
    pass


def batch_request(method, urls, payloads=None, **kwargs):
    if payloads is not None:
        req_list = [grequests.request(method,
                                      url=urls,
                                      data=payload,
                                      timeout=configs.REQUEST_TIMEOUT,
                                      **kwargs) for payload in payloads]
    else:
        req_list = [grequests.request(method,
                                      url=url,
                                      timeout=configs.REQUEST_TIMEOUT,
                                      **kwargs) for url in urls]
    logger.info(urls)
    return grequests.imap(req_list, exception_handler=err_handler)
    pass


def get(url, **kwargs):
    return single_request('GET', url, **kwargs)


def batch_get(urls, **kwargs):
    return batch_request('GET', urls, **kwargs)


def post(url, headers=configs.JSON_HEADERS, **kwargs):
    logger.info(json.dumps(kwargs, ensure_ascii=False))
    return single_request('POST', url, headers=headers, **kwargs)


def batch_post(urls, payloads=None, headers=configs.JSON_HEADERS, **kwargs):
    logger.info(json.dumps(kwargs, ensure_ascii=False))
    return batch_request('POST', urls, payloads=payloads, headers=headers, **kwargs)


def put(url, headers=configs.JSON_HEADERS, **kwargs):
    logger.info(json.dumps(kwargs, ensure_ascii=False))
    return single_request('PUT', url, headers=headers, **kwargs)


def batch_put(urls, headers=configs.JSON_HEADERS, **kwargs):
    logger.info(json.dumps(kwargs, ensure_ascii=False))
    return batch_request('PUT', urls, headers=headers, **kwargs)
