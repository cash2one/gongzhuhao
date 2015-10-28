#encoding:utf-8
__author__ = 'binpo'

from datetime import datetime
import os

from libs.apscheduler.schedulers.blocking import BlockingScheduler

from crontab.count_tasks import RewriteCacheDataToTable

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(RewriteCacheDataToTable().count_cache_data,'interval',seconds=3600*6)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
