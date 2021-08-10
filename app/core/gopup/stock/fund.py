#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/14 21:38
# @Author  : justin.郑 3907721@qq.com
# @File    : fund.py
# @Desc    : 基金数据

import json
import pandas as pd
import requests


def fund_etf_category_sina(symbol="封闭式基金"):
    """
    基金列表
    http://vip.stock.finance.sina.com.cn/fund_center/index.html#jjhqetf
    :param symbol: choice of {"封闭式基金", "ETF基金", "LOF基金"}
    :type symbol: str
    :return: 指定 symbol 的基金列表
    :rtype: pandas.DataFrame
    """
    fund_map = {
        "封闭式基金": "close_fund",
        "ETF基金": "etf_hq_fund",
        "LOF基金": "lof_hq_fund",
    }
    url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/IO.XSRV2.CallbackList['da_yPT46_Ll7K6WD']/Market_Center.getHQNodeDataSimple"
    params = {
        "page": "1",
        "num": "1000",
        "sort": "symbol",
        "asc": "0",
        "node": fund_map[symbol],
        "[object HTMLDivElement]": "qvvne",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("([")+1:-2])
    temp_df = pd.DataFrame(data_json)
    res_df = temp_df[["symbol", "name"]]
    return res_df


def fund_etf_hist_sina(symbol="sz159996"):
    """
    ETF 基金的日行情数据
    http://finance.sina.com.cn/fund/quotes/159996/bc.shtml
    :param symbol: 基金名称, 可以通过 fund_etf_category_sina 函数获取
    :type symbol: str
    :return: ETF 基金的日行情数据
    :rtype: pandas.DataFrame
    """
    url = f"https://finance.sina.com.cn/realstock/company/{symbol}/hisdata/klc_kl.js"
    r = requests.get(url)
    js_code = py_mini_racer.MiniRacer()
    js_code.eval(hk_js_decode)
    dict_list = js_code.call('d', r.text.split("=")[1].split(";")[0].replace('"', ""))  # 执行js解密代码
    temp_df = pd.DataFrame(dict_list)
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    return temp_df


if __name__ == '__main__':
    fund_etf_category_sina_df = fund_etf_category_sina(symbol="ETF基金")
    print(fund_etf_category_sina_df)

    # fund_etf_hist_sina_df = fund_etf_hist_sina(symbol="sz169103")
    # print(fund_etf_hist_sina_df)