#!/usr/bin/env python2.7
# encoding:utf-8
from __future__ import absolute_import

from celery_tasks.base import DatabaseTasks
from celery_tasks.celery import app

@app.task(base=DatabaseTasks)
def cache_view_set(table_name,object_id,default_count=0):
    '''
     :topic detail 浏览数
    :param table_name:
    :param object_id:
    :param default_count:
    :return:
    '''
    count = cache_view_set.rcache.hget(table_name, object_id)
    if not count:
        count=default_count
    cache_view_set.rcache.hset(table_name, object_id, int(count)+1)

@app.task(base=DatabaseTasks)
def count_reply_set(table_name,object_id,default_count=0):
    '''
    :topic 回复总数
    :param table_name:
    :param object_id:
    :param default_count:
    :return:
    '''
    count = count_reply_set.rcache.hget(table_name+'_count_reply', object_id)
    if not count:
        count=default_count
    count_reply_set.rcache.hset(table_name+'_count_reply', object_id, int(count)+1)

@app.task(base=DatabaseTasks)
def count_category_topics_set(table_name,object_id,default_count=0):
    '''
    :topic_ctegory 话题总数
    :param table_name:
    :param object_id:
    :param default_count:
    :return:
    '''
    count = count_category_topics_set.rcache.hget(table_name+'_count_topic', object_id)
    if not count:
        count=default_count
    count_category_topics_set.rcache.hset(table_name+'_count_topic', object_id, int(count)+1)

@app.task(base=DatabaseTasks)
def count_topics_sns_set(table_name,object_id,default_count=0):
    '''
    :topic_ctegory 点赞总数
    :param table_name:
    :param object_id:
    :param default_count:
    :return:
    '''
    count = count_category_topics_set.rcache.hget(table_name+'_count_sns', object_id)
    if not count:
        count=default_count
    count_category_topics_set.rcache.hset(table_name+'_count_sns', object_id, int(count)+1)

