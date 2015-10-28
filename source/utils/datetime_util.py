# -*- coding: utf-8 -*-

'''''
Filename: "utildate.py"
author:   "binpo"
date  :   "2014-03-24"
version:  "1.00"
'''

import datetime

def datetime_format(format='%Y-%m-%d %H:%M:%S',input_date=None):
    if input_date:
        return datetime.datetime.strftime(input_date,format)
    else:
        return datetime.datetime.strftime(datetime.datetime.now(),format)

def getdayofday(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if(n < 0):
        n = abs(n)
        return datetime.datetime.today() - datetime.datetime.timedelta(days=n)
    else:
        return datetime.datetime.today() + datetime.datetime.timedelta(days=n)

def get_month_last_day(month=None,year=None):
    date1 = datetime.datetime.today()
    if not year:
        y=date1.year
    else:
        y=year
    if month:
        m = int(month)
    else:m = date1.month
    #month_start_dt = datetime.date(y,m,1)
    if m == 12:
        month_end_dt = datetime.date(y+1,1,1) - datetime.timedelta(days=1)
    else:
        month_end_dt = datetime.date(y,m+1,1) - datetime.timedelta(days=1)
    return month_end_dt



def get_month_first_day(month=None,year=None):
    date1 = datetime.datetime.today()
    if not year:
        y=date1.year
    else:
        y=year
    if month:
        m = int(month)
    else:m = date1.month
    # if m == 12:
    #     month_end_dt = datetime.date(y-1,1,1) - datetime.timedelta(days=1)
    # else:
    #
    month_end_dt = datetime.date(y,m,1)
    return month_end_dt


def get_month_day(input_date,input_day=None):
    date1 = input_date
    y=date1.year
    m = date1.month
    day = date1.day
    month_day = datetime.date(y,m,input_day+day)
    return month_day
