import json
from json import JSONDecodeError

from app.extensions import logger
from app.setting import configs
from app.utils import request_utils, datetime_utils, decimal_utils


def resp_valid(json_resp, data_name):
    return json_resp is not None and data_name in json_resp and json_resp[data_name] is not None


class EastMoneyRequest:
    base_url = configs.EAST_MONEY_URL
    history_base_url = configs.EAST_MONEY_HISTORY_URL
    search_base_url = configs.EAST_MONEY_SEARCH_URL
    data_interface_url = configs.EAST_MONEY_DATA_INTERFACE

    def calendar(self, date=None, time=None, count=5, num=1):
        trade_date = date
        if trade_date is None:
            trade_date = datetime_utils.current_date('%Y-%m-%d')
        try:
            resp = request_utils.get(
                "%s/%s" % (self.data_interface_url, "EM_DataCenter/JS.aspx?type=GSRL&sty=GSRL&stat=21&fd=%s&p=1"
                                                    "&pageNo=%i&ps=%i&_=%i" %
                           (trade_date, num, count, datetime_utils.current_time())))
        except Exception as e:
            logger.error(e)
            resp = None
        results = {'trade': False}
        if resp is None:
            return results
        try:
            resp_str = resp.text.replace("(", "")
            resp_str = resp_str.replace(")", "")
            resp_json = json.loads(resp_str)
        except JSONDecodeError as e:
            logger.error(e)
            return results
        results = {
            'trade': True,
            'data': resp_json
        }
        trade_time = time
        format_str = '%Y-%m-%d %H:%M:%S'
        if trade_time is None:
            trade_time = datetime_utils.current_datetime('%H:%M:%S')
        am = datetime_utils.compare_time('%s %s' % (trade_date, trade_time), format_str,
                                         '%s %s' % (trade_date, '09:30:00'),
                                         format_str) > 0 and datetime_utils.compare_time(
            '%s %s' % (trade_date, trade_time), format_str, '%s %s' % (trade_date, '11:30:00'), format_str) < 0
        pm = datetime_utils.compare_time('%s %s' % (trade_date, trade_time), format_str,
                                         '%s %s' % (trade_date, '13:00:00'),
                                         format_str) > 0 and datetime_utils.compare_time(
            '%s %s' % (trade_date, trade_time), format_str, '%s %s' % (trade_date, '15:00:00'), format_str) < 0
        results['trade'] = am or pm
        return results

    def search(self, words):
        try:
            resp = request_utils.get(
                "%s/%s" % (self.search_base_url, "api/suggest/get?input=%s&type=14&token"
                                                 "=D43BF722C8E33BDC906FB84D85E326E8&markettype=&mktnum=&jys=&classify"
                                                 "=&securitytype=&status=&count=5&_=%i" %
                           (words, datetime_utils.current_time())))
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        results = []
        if json_resp is None or "QuotationCodeTable" not in json_resp or "Data" not in json_resp["QuotationCodeTable"]:
            return results
        if json_resp["QuotationCodeTable"]["Data"] is None:
            return results
        for json_obj in json_resp["QuotationCodeTable"]["Data"]:
            stock = {
                "name": json_obj["Name"],
                "code": json_obj["Code"],
                "pinYin": json_obj["PinYin"],
                "classify": json_obj["Classify"],
                "marketType": json_obj["MarketType"],
                "secTypeName": json_obj["SecurityTypeName"],
                "secType": json_obj["SecurityType"],
                "sinaCode": json_obj["QuoteID"]
            }
            results.append(stock)
        return results

    def stock_top(self, rise=1, turnover=False, options=False, quantity=False, count=10, num=1):
        try:
            fid = "f3"
            if turnover:
                fid = "f8"
            elif options:
                fid = "f62"
            elif quantity:
                fid = "f10"
            resp = request_utils.get(
                "%s/%s" % (self.base_url, "api/qt/clist/get?pn=%i&pz=%i&po=%i&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281"
                                          "&fltt=2&invt=2&fid=%s&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,"
                                          "f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,"
                                          "f22,f11,f62,f128,f136,f115,f152&_=%i" %
                           (num, count, rise, fid, datetime_utils.current_time())))
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        results = []
        if json_resp is None or "data" not in json_resp or "diff" not in json_resp["data"]:
            return results
        for json_obj in json_resp["data"]["diff"]:
            stock = {
                "name": json_obj["f14"],
                "code": json_obj["f12"],
                "increase": decimal_utils.decimal2str(json_obj["f4"], prefix_plus=True),
                "increasePercent": decimal_utils.decimal2str(json_obj["f3"], prefix_plus=True),
                "price": decimal_utils.decimal2str(json_obj["f2"]),
                "result": decimal_utils.decimal2str(json_obj["f3"], prefix_plus=True),
            }
            results.append(stock)
        return results

    def stock_quotations(self, code):
        try:
            resp = request_utils.get(
                "%s/%s" % (
                    self.base_url, "api/qt/stock/get?secid=%s&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f118,"
                                   "f107,f57,f58,f59,f152,f43,f169,f170,f46,f60,f44,f45,f51,f52,f168,f50,f47,f48,f49,"
                                   "f46,f169,f161,f162,f117,f84,f85,f47,f48,f163,f167,f171,f113,f114,f115,f116,f86,"
                                   "f117,f85,f119,f120,f121,f122,f292,f191&invt=2&_=%i" %
                    (code, datetime_utils.current_time())))
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        if not resp_valid(json_resp, "data") or "f57" not in json_resp["data"]:
            return {}
        if json_resp["data"]["f47"] == "-":
            vol = '-'
            vol_unit = '-'
        else:
            vol = json_resp["data"]["f47"] / 10000 if json_resp["data"]["f47"] < 10000000 \
                else json_resp["data"]["f47"] / 100000000
            vol_unit = '万' if json_resp["data"]["f47"] < 10000000 else '亿'
        left_unit = 1
        try:
            for unit in range(0, json_resp["data"]["f59"]):
                left_unit = left_unit * 10
        except TypeError as e:
            logger.error(e)
        stock = {
            "name": json_resp["data"]["f58"],
            "code": json_resp["data"]["f57"],
            "currentPrice": decimal_utils.decimal2str(json_resp["data"]["f43"], left=left_unit),
            "highPrice": decimal_utils.decimal2str(json_resp["data"]["f44"], left=left_unit),
            "lowPrice": decimal_utils.decimal2str(json_resp["data"]["f45"], left=left_unit),
            "openPrice": decimal_utils.decimal2str(json_resp["data"]["f46"], left=left_unit),
            "prePrice": decimal_utils.decimal2str(json_resp["data"]["f60"], left=left_unit),
            "limitUp": decimal_utils.decimal2str(json_resp["data"]["f51"], left=left_unit),
            "limitDown": decimal_utils.decimal2str(json_resp["data"]["f52"], left=left_unit),
            "turnOver": decimal_utils.decimal2str(json_resp["data"]["f168"], left=100),
            "volume": decimal_utils.decimal2str(vol),
            "volUnit": vol_unit,
            "amount": json_resp["data"]["f48"],
            "innerVol": decimal_utils.decimal2unit(json_resp["data"]["f161"]),
            "outVol": decimal_utils.decimal2unit(json_resp["data"]["f49"]),
            "volRatio": decimal_utils.decimal2str(json_resp["data"]["f50"], left=100),
            "comRatio": decimal_utils.decimal2str(json_resp["data"]["f191"], left=100),
            "flowValue": decimal_utils.decimal2unit(json_resp["data"]["f117"]),
            "trShares": decimal_utils.decimal2unit(json_resp["data"]["f85"]),
            "sumShares": decimal_utils.decimal2unit(json_resp["data"]["f84"]),
            "totalValue": decimal_utils.decimal2unit(json_resp["data"]["f116"]),
            "pe": decimal_utils.decimal2str(json_resp["data"]["f162"], left=100),
            "pb": decimal_utils.decimal2str(json_resp["data"]["f167"], left=100),
            "amp": decimal_utils.decimal2str(json_resp["data"]["f171"], left=100),
        }
        return stock
        pass

    def stock_buy_sell(self, code):
        try:
            resp = request_utils.get(
                "%s/%s" % (
                    self.base_url, "api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&volt=2&fields"
                                   "=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,"
                                   "f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,"
                                   "f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,"
                                   "f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,"
                                   "f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,"
                                   "f274,f275,f127,f199,f128,f198,f259,f260,f261,f171,f277,f278,f279,f288,f292,"
                                   "f182&secid=%s&_=%i" % (code, datetime_utils.current_time())))
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        if not resp_valid(json_resp, "data") or "f57" not in json_resp["data"]:
            return {}
        stock = {
            "buyPrice1": decimal_utils.decimal2str(json_resp["data"]["f19"]),
            "buyPrice2": decimal_utils.decimal2str(json_resp["data"]["f17"]),
            "buyPrice3": decimal_utils.decimal2str(json_resp["data"]["f15"]),
            "buyPrice4": decimal_utils.decimal2str(json_resp["data"]["f13"]),
            "buyPrice5": decimal_utils.decimal2str(json_resp["data"]["f11"]),
            "buyAoumt1": decimal_utils.decimal2str(json_resp["data"]["f20"], count=0),
            "buyAoumt2": decimal_utils.decimal2str(json_resp["data"]["f18"], count=0),
            "buyAoumt3": decimal_utils.decimal2str(json_resp["data"]["f16"], count=0),
            "buyAoumt4": decimal_utils.decimal2str(json_resp["data"]["f14"], count=0),
            "buyAoumt5": decimal_utils.decimal2str(json_resp["data"]["f12"], count=0),
            "sellPrice1": decimal_utils.decimal2str(json_resp["data"]["f31"]),
            "sellPrice2": decimal_utils.decimal2str(json_resp["data"]["f33"]),
            "sellPrice3": decimal_utils.decimal2str(json_resp["data"]["f35"]),
            "sellPrice4": decimal_utils.decimal2str(json_resp["data"]["f37"]),
            "sellPrice5": decimal_utils.decimal2str(json_resp["data"]["f39"]),
            "sellAoumt1": decimal_utils.decimal2str(json_resp["data"]["f32"], count=0),
            "sellAoumt2": decimal_utils.decimal2str(json_resp["data"]["f34"], count=0),
            "sellAoumt3": decimal_utils.decimal2str(json_resp["data"]["f36"], count=0),
            "sellAoumt4": decimal_utils.decimal2str(json_resp["data"]["f38"], count=0),
            "sellAoumt5": decimal_utils.decimal2str(json_resp["data"]["f40"], count=0),
        }
        return stock
        pass

    def stock_detail(self, code):
        stock = self.stock_quotations(code)
        stock = dict(self.stock_buy_sell(code), **stock)
        try:
            resp = request_utils.get(
                "%s/%s" % (
                    self.base_url, "api/qt/stock/trends2/get?secid=%s&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,"
                                   "f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,"
                                   "f58&ut=e1e6871893c6386c5ff6967026016627&iscr=0&isqhquote=" % code))
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        if not resp_valid(json_resp, "data") or "trends" not in json_resp["data"]:
            return {}
        trends = json_resp["data"]["trends"]
        if len(trends) > 0:
            trend = trends[-1].split(",")
            change = float(trend[2]) - json_resp["data"]["preClose"]
        else:
            change = 0
        stock.setdefault("increase", decimal_utils.decimal2str(change, prefix_plus=True))
        stock.setdefault("increasePercent", decimal_utils.decimal2str(change / json_resp["data"]["preClose"], right=100,
                                                                      prefix_plus=True))
        return stock

    def stock_minutely(self, code):
        try:
            resp = request_utils.get(
                "%s/%s" % (
                    self.base_url, "api/qt/stock/trends2/get?secid=%s&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,"
                                   "f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,"
                                   "f58&ut=e1e6871893c6386c5ff6967026016627&iscr=0&isqhquote=" % code))
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        if json_resp is None or "data" not in json_resp or json_resp["data"] is None or "trends" not in json_resp[
            "data"]:
            return {}
        stock = {
            "name": json_resp["data"]["name"],
            "code": json_resp["data"]["code"],
            "preClose": json_resp["data"]["preClose"]
        }
        trends = json_resp["data"]["trends"]
        stock.setdefault("trends", trends)
        return stock

    def stock_history(self, code, tp, beg, end, count):
        if end == "":
            end = datetime_utils.current_date()
        try:
            resp = request_utils.get(
                "%s/%s" % (
                    self.history_base_url, "api/qt/stock/kline/get?secid=%s&fields1=f1,f2,f3,f4,f5&fields2=f51,"
                                           "f52,f53,f54,f55,f56,"
                                           "f57&klt=%i&fqt=0&beg=%s&end=%s&ut"
                                           "=fa5fd1943c7b386f172d6893dbfba10b" % (code, tp, beg, end)))
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        if json_resp is None or "data" not in json_resp or json_resp["data"] is None or "klines" not in json_resp[
            "data"]:
            return {}
        stock = {
            "name": json_resp["data"]["name"],
            "code": json_resp["data"]["code"],
            "decimal": json_resp["data"]["decimal"],
            "total": json_resp["data"]["dktotal"]
        }
        histories = json_resp["data"]["klines"][-count:]
        stock.setdefault("histories", histories)
        return stock

    def indices_quotations(self, indices_code=None):
        if indices_code is None:
            indices_code = []
        results = []
        for code in indices_code:
            try:
                resp = request_utils.get(
                    "%s/%s" % (
                        self.base_url, "api/qt/stock/trends2/get?secid=%s&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,"
                                       "f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,"
                                       "f58&ut=e1e6871893c6386c5ff6967026016627&iscr=0&isqhquote=" % code))
                json_resp = resp.json()
            except Exception as e:
                logger.error(e)
                json_resp = None
            if json_resp is None or "data" not in json_resp or "trends" not in json_resp["data"]:
                continue
            trends = json_resp["data"]["trends"]
            trend = trends[-1].split(",")
            change = float(trend[2]) - json_resp["data"]["preClose"]
            indices = {
                "name": json_resp["data"]["name"],
                "increase": decimal_utils.decimal2str(change, prefix_plus=True),
                "price": float(trend[2]),
                "increasePercent": decimal_utils.decimal2str(change / json_resp["data"]["preClose"] * 100,
                                                             prefix_plus=True)
            }
            results.append(indices)
        return results

    def indices_stocks(self, code, count=10, num=1):
        try:
            if code == "000001":
                url = "%s/%s" % (self.base_url, "api/qt/clist/get?fid=f62&po=1&pz=%i&pn=%i&np=1&fltt=2&invt=2&ut"
                                                "=b2884a393a59ad64002292a3e90d46a5&fs=m:1+t:2+f:!2,"
                                                "m:1+t:23+f:!2&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,"
                                                "f84,f87,f204,f205,f124" %
                                 (count, num))
            elif code == "399001":
                url = "%s/%s" % (self.base_url, "api/qt/clist/get?fid=f62&po=1&pz=%i&pn=%i&np=1&fltt=2&invt=2&ut"
                                                "=b2884a393a59ad64002292a3e90d46a5&fs=m:0+t:80+f:!2&fields=f12,f14,"
                                                "f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124" %
                                 (count, num))
            elif code == "399006":
                url = "%s/%s" % (self.base_url, "api/qt/clist/get?fid=f62&po=1&pz=%i&pn=%i&np=1&fltt=2&invt=2&ut"
                                                "=b2884a393a59ad64002292a3e90d46a5&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,"
                                                "m:0+t:80+f:!2&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,"
                                                "f84,f87,f204,f205,f124" %
                                 (count, num))
            else:
                return []
            resp = request_utils.get(url)
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        results = []
        if not resp_valid(json_resp, "data") or "diff" not in json_resp["data"]:
            return results
        for json_obj in json_resp["data"]["diff"]:
            stock = {
                "name": json_obj["f14"],
                "code": json_obj["f12"],
                "increasePercent": decimal_utils.decimal2str(json_obj["f3"], prefix_plus=True),
                "price": decimal_utils.decimal2str(json_obj["f2"]),
            }
            results.append(stock)
        return results

    def block_quotations(self, block_code=None, count=10, num=1):
        try:
            resp = request_utils.get(
                "%s/%s" % (self.base_url, "api/qt/clist/get?pn=%i&pz=%i&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281"
                                          "&fltt=2&invt=2&fid=f3&fs=m:90+t:%i+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,"
                                          "f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,"
                                          "f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,"
                                          "f222&_=%i" % (num, count, block_code, datetime_utils.current_time())))
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        results = []
        if json_resp is None or "data" not in json_resp or "diff" not in json_resp["data"]:
            return results
        for json_obj in json_resp["data"]["diff"]:
            block = {
                "blockName": json_obj["f14"],
                "blockCode": json_obj["f12"],
                "blockEsCode": "%i.%s" % (json_obj["f13"], json_obj["f12"]),
                "blockIncreasePercent": decimal_utils.decimal2str(json_obj["f3"], prefix_plus=True),
                "topStockName": json_obj["f128"],
                "topStockIncreasePercent": decimal_utils.decimal2str(json_obj["f136"], prefix_plus=True),
            }
            results.append(block)
        return results

    def block_stocks(self, code, count=10, num=1):
        try:
            resp = request_utils.get(
                "%s/%s" % (self.base_url, "api/qt/clist/get?fid=f62&po=1&pz=%i&pn=%i&np=1&fltt=2&invt=2&ut"
                                          "=b2884a393a59ad64002292a3e90d46a5&fs=b:%s&fields=f12,f14,f2,f3,f62,"
                                          "f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124" %
                           (count, num, code)))
            json_resp = resp.json()
        except Exception as e:
            logger.error(e)
            json_resp = None
        results = []
        if not resp_valid(json_resp, "data") or "diff" not in json_resp["data"]:
            return results
        for json_obj in json_resp["data"]["diff"]:
            stock = {
                "name": json_obj["f14"],
                "code": json_obj["f12"],
                "increasePercent": decimal_utils.decimal2str(json_obj["f3"], prefix_plus=True),
                "price": decimal_utils.decimal2str(json_obj["f2"]),
            }
            results.append(stock)
        return results

    pass
