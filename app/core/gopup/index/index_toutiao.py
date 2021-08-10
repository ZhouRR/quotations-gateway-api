#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/23 0023
# @Author  : justin.郑 3907721@qq.com
# @File    : index_toutiao.py
# @Desc    : 头条指数

import json
import pandas as pd
import requests
from gopup.index.cons import index_toutiao_headers


def toutiao_index(keyword="python", start_date="20201016", end_date="20201022", app_name="toutiao"):
    """
    头条指数数据
    :param keyword:     关键词
    :param start_date:  开始日期
    :param end_date:    截止日期
    :param app_name:    平台
    :return:
        datetime    日期
        index       指数
    """
    # list_keyword = '["%s"]' % keyword
    try:
        url = "https://trendinsight.oceanengine.com/api/open/index/get_multi_keyword_hot_trend"
        data = {
            "keyword_list": [keyword],
            "start_date": start_date,
            "end_date": end_date,
            "app_name": app_name
        }
        res = requests.post(url, json=data, headers=index_toutiao_headers)
        hot_list = json.loads(res.text)['data']['hot_list'][0]['hot_list']
        df = pd.DataFrame(hot_list)
        return df
    except:
        return None


def toutiao_relation(keyword="python", start_date="20201012", end_date="20201018", app_name="toutiao"):
    """
    头条相关分析
    :param keyword:     关键词
    :param start_date:  开始日期
    :param end_date:    截止日期
    :return:
        relation_word    相关词
        relation_score   相关性值
        score_rank       相关性值排名
        search_hot       搜索热点值
        search_ratio     搜索比率
    """
    try:
        url = "https://trendinsight.oceanengine.com/api/open/index/get_relation_word"
        data = {"param": {"keyword": keyword,
                          "start_date": start_date,
                          "end_date": end_date,
                          "app_name": app_name}
                }
        res = requests.post(url, json=data, headers=index_toutiao_headers)
        relation_word_list = json.loads(res.text)['data']['relation_word_list']
        df = pd.DataFrame(relation_word_list)
        return df
    except:
        return None


# def toutiao_sentiment(keyword="python", start_date="20201012", end_date="20201018"):
#     """
#     头条情感分析
#     :param keyword:     关键词
#     :param start_date:  开始日期
#     :param end_date:    截止日期
#     :return:
#         keyword    关键词
#         score      情感值
#     """
#     url = "https://index.toutiao.com/api/v1/get_keyword_sentiment"
#     data = {
#         "keyword": keyword,
#         "start_date": start_date,
#         "end_date": end_date
#     }
#     res = requests.get(url, params=data, headers=index_toutiao_headers)
#     score = json.loads(res.text)['data']['score']
#     df = pd.DataFrame([{"score": score, "keyword": keyword}])
#     return df


def toutiao_province(keyword="python", start_date="20201012", end_date="20201018", app_name="toutiao"):
    """
    头条地域分析
    :param keyword:     关键词
    :param start_date:  开始日期
    :param end_date:    截止日期
    :return:
        name    省份
        value   渗透率
    """
    try:
        url = "https://trendinsight.oceanengine.com/api/open/index/get_portrait"
        data = {"param": {"keyword": keyword,
                          "start_date": start_date,
                          "end_date": end_date,
                          "app_name": app_name}
                }
        res = requests.post(url, json=data, headers=index_toutiao_headers)
        res_text = json.loads(res.text)['data']['data'][2]['label_list']
        df = pd.DataFrame(res_text)
        df['name'] = df['name_zh']
        df = df.drop(['label_id', 'name_zh'], axis=1)
        df = df.sort_values(by="value", ascending=False)
        return df
    except:
        return None

def toutiao_city(keyword="python", start_date="20201012", end_date="20201018", app_name="toutiao"):
    """
    头条城市分析
    :param keyword:     关键词
    :param start_date:  开始日期
    :param end_date:    截止日期
    :return:
        name    城市
        value   渗透率
    """
    try:
        url = "https://trendinsight.oceanengine.com/api/open/index/get_portrait"
        data = {"param": {"keyword": keyword,
                          "start_date": start_date,
                          "end_date": end_date,
                          "app_name": app_name}
                }
        res = requests.post(url, json=data, headers=index_toutiao_headers)
        res_text = json.loads(res.text)['data']['data'][3]['label_list']
        df = pd.DataFrame(res_text)
        df['name'] = df['name_zh']
        df = df.drop(['label_id', 'name_zh'], axis=1)
        df = df.sort_values(by="value", ascending=False)
        return df
    except:
        return None


def toutiao_age(keyword="python", start_date="20201012", end_date="20201018", app_name="toutiao"):
    """
    头条年龄分析
    :param keyword:     关键词
    :param start_date:  开始日期
    :param end_date:    截止日期
    :return:
        name    年龄区间
        value   渗透率
    """
    try:
        url = "https://trendinsight.oceanengine.com/api/open/index/get_portrait"
        data = {"param": {"keyword": keyword,
                         "start_date": start_date,
                         "end_date": end_date,
                         "app_name": app_name}
                }
        res = requests.post(url, json=data, headers=index_toutiao_headers)
        res_text = json.loads(res.text)['data']['data'][0]['label_list']
        df = pd.DataFrame(res_text)
        df['name'] = df['name_zh']
        df = df.drop(['label_id', 'name_zh'], axis=1)
        return df
    except:
        return None


def toutiao_gender(keyword="python", start_date="20201012", end_date="20201018", app_name="toutiao"):
    """
    头条性别分析
    :param keyword:     关键词
    :param start_date:  开始日期
    :param end_date:    截止日期
    :return:
        name    性别
        value   渗透率
    """
    try:
        url = "https://trendinsight.oceanengine.com/api/open/index/get_portrait"
        data = {"param": {"keyword": keyword,
                          "start_date": start_date,
                          "end_date": end_date,
                          "app_name": app_name}
                }
        res = requests.post(url, json=data, headers=index_toutiao_headers)
        res_text = json.loads(res.text)['data']['data'][1]['label_list']
        df = pd.DataFrame(res_text)
        df['name'] = df['name_zh']
        df = df.drop(['label_id', 'name_zh'], axis=1)
        df = df.sort_values(by="value", ascending=False)
        return df
    except:
        return None


def toutiao_interest_category(keyword="python", start_date="20201012", end_date="20201018", app_name="toutiao"):
    """
    头条用户阅读兴趣分类
    :param keyword:     关键词
    :param start_date:  开始日期
    :param end_date:    截止日期
    :return:
        name    分类
        value   渗透率
    """
    try:
        url = "https://trendinsight.oceanengine.com/api/open/index/get_portrait"
        data = {"param": {"keyword": keyword,
                          "start_date": start_date,
                          "end_date": end_date,
                          "app_name": app_name}
                }
        res = requests.post(url, json=data, headers=index_toutiao_headers)
        res_text = json.loads(res.text)['data']['data'][4]['label_list']
        df = pd.DataFrame(res_text)
        df['name'] = df['name_zh']
        df = df.drop(['label_id', 'name_zh'], axis=1)
        df = df.sort_values(by="value", ascending=False)
        return df
    except:
        return None


if __name__ == "__main__":
    index_df = toutiao_index(keyword="口罩", start_date='20201214', end_date='20201220', app_name="aweme")
    print(index_df)
 

