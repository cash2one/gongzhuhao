from __future__ import absolute_import

#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

from celery import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from setting import ENGINE
from utils.cache_manager import RedisManaher


class DatabaseTasks(Task):
    abstract = True
    _db = None
    _rcache = None

    @property
    def db(self):
        if self._db is None:
            self._db = scoped_session(sessionmaker(bind=create_engine(ENGINE,echo=True),autoflush=True,autocommit=False))
        return self._db

    @property
    def rcache(self):
        if self._rcache is None:
            self._rcache = RedisManaher().cache_con()
        return self._rcache

    def on_success(self, retval, task_id, args, kwargs):
        print '%s, is succeed' % task_id

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print '%s, is failure' % task_id
        # self.retry(exc)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        try:
            self._db.close()
        except:
            pass
