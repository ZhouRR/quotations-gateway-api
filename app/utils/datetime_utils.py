import datetime
from pytz import timezone
import time

cst_tz = timezone('Asia/Shanghai')


def current_time():
    return int(round(time.time() * 1000))


def current_datetime(format_string='%Y%m%d%H%M%S', delta=0):
    now = datetime.datetime.now(cst_tz) + datetime.timedelta(days=delta)
    return now.strftime(format_string)
    pass


def current_date(format_string='%Y%m%d', delta=0):
    now = datetime.datetime.now(cst_tz) + datetime.timedelta(days=delta)
    return now.strftime(format_string)
    pass


def compare_with_current(time1, format_s):
    return compare_time(time1, format_s, current_date(), '%Y%m%d')


def compare_time(time1, format_s, time2, format_e):
    s_time = time.mktime(time.strptime(time1, format_s))
    e_time = time.mktime(time.strptime(time2, format_e))
    return int(s_time) - int(e_time)
