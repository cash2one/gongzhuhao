# -*- coding: utf-8 -*-
"""
    Date util tools

    :copyright: (c) 2012 by fangshi.lb.
"""

#!/usr/bin/python
'''''
Filename: "utildate.py"
author:   "binpo"
date  :   "2014-03-24"
version:  "1.00"
'''
from time import strftime, localtime
import time

from datetime import timedelta, date, datetime

import calendar

year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())
hour = strftime("%H", localtime())
min = strftime("%M", localtime())
sec = strftime("%S", localtime())


def today():
    '''''
    get today,date format="YYYY-MM-DD"
    '''
    return date.today()


def todaystr():
    '''''
    get date string
    date format="YYYYMMDD"
    '''
    return year + mon + day

def monthstr():
    '''''
    get date string
    date format="YYYYMMDD"
    '''
    return year + mon

def yyyydddddatetime(format="%Y-%m-%d %H:%M:%S",input_date=None):
    '''''
        get datetime,format="YYYY-MM-DD HH:MM:SS"
    '''
    return input_date and strftime(format, input_date) or strftime(format,localtime())


def datetime_format(format="%Y-%m-%d %H:%M:%S",input_date=None):
    return input_date and datetime.strftime(input_date,format) or datetime.strftime(datetime.now(),format)

def datetime_format_2(format="%Y-%m-%d %H:%M:%S",input_date=None):
    if not input_date:
        return None
    else:
        return datetime.strftime(input_date,format)

def datetimestr():
    '''''
    get datetime string
    date format="YYYYMMDDHHMMSS"
    '''
    return year + mon + day + hour + min + sec


def getdayofday(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if(n < 0):
        n = abs(n)
        return date.today() - timedelta(days=n)
    else:
        return date.today() + timedelta(days=n)


def get_date_operation(n=0):
    if(n < 0):
        n = abs(n)
        return datetime.now() - timedelta(days=n)
    else:
        return datetime.now() + timedelta(days=n)

def getdaysofmonth(year, mon):
    '''''
    get days of month
    '''
    return calendar.monthrange(year, mon)[1]


def getfirstdayofmonth(year, mon):
    '''''
    get the first day of month
    date format = "YYYY-MM-DD"
    '''
    days = "01"
    if(int(mon) < 10):
        mon = "0" + str(int(mon))
    arr = (year, mon, days)
    return "-".join("%s" % i for i in arr)


def getlastdayofmonth(year, mon):
    '''''
    get the last day of month
    date format = "YYYY-MM-DD"
    '''
    days = calendar.monthrange(year, mon)[1]
    mon = addzero(mon)
    arr = (year, mon, days)
    return "-".join("%s" % i for i in arr)


def get_firstday_month(n=0):
    '''''
    get the first day of month from today
    n is how many months
    '''
    (y, m, d) = getyearandmonth(n)
    d = "01"
    arr = (y, m, d)
    return "-".join("%s" % i for i in arr)


def get_lastday_month(n=0):
    '''''
    get the last day of month from today
    n is how many months
    '''
    return "-".join("%s" % i for i in getyearandmonth(n))


def get_today_month(n=0):
    '''''
    get last or next month's today
    n is how many months
    date format = "YYYY-MM-DD"
    '''
    (y, m, d) = getyearandmonth(n)
    arr = (y, m, d)
    if(int(day) < int(d)):
        arr = (y, m, day)
    return "-".join("%s" % i for i in arr)


def getyearandmonth(n=0):
    '''''
    get the year,month,days from today
    befor or after n months
    '''
    thisyear = int(year)
    thismon = int(mon)
    totalmon = thismon + n
    if(n >= 0):
        if(totalmon <= 12):
            days = str(getdaysofmonth(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if(j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(getdaysofmonth(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days)
    else:
        if((totalmon > 0) and (totalmon < 12)):
            days = str(getdaysofmonth(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if(j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(getdaysofmonth(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days)


def addzero(n):
    '''''
    add 0 before 0-9
    return 01-09
    '''
    nabs = abs(int(n))
    if(nabs < 10):
        return "0" + str(nabs)
    else:
        return nabs

        #print today()

#print addzero(10)
#print get_today_month(-1)
#print get_lastday_month(3)
#print get_firstday_month(3)

import time

def time_passed(value):
    now = datetime.now()
    past = now - value
    if past.days:
        return u'%s天前' % past.days
    mins = past.seconds / 60
    if mins < 60:
        return u'%s分钟前' % mins
    hours = mins / 60
    return u'%s小时前' % hours
#print datetime_format()

def the_rest_of_today():
    end_time = datetime(int(year),int(mon),int(day),23,59,59)
    now = datetime.now()
    return int((end_time-now).total_seconds())

def time_of_seven_days_ago():
    return datetime.now() - timedelta(days=7)

def  time_of_a_month_ago():
    return datetime.now() - timedelta(days=30)


#print type(the_rest_of_today()),the_rest_of_today()