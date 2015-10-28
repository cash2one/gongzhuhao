# encoding:utf-8
# !/usr/bin/env python

import tornado.ioloop
import tornado.web
from tornado.options import options
from apps_crm import handlers

from common.urls import handlers as common_handler
handlers.extend(common_handler)

from apps_crm.home import HomeHandler
handlers.append((r'/([\w\W]*)',HomeHandler))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.pool import NullPool

import sys,os
from utils.conf_util import parse_config_file
from setting import settings
from utils.cache_manager import RedisManaher,MemcacheManager
from raven.contrib.tornado import AsyncSentryClient

class MySQLPingListener(object):

    def checkout(self, dbapi_con, con_record, con_proxy):
        from sqlalchemy.exc import DisconnectionError
        from _mysql_exceptions import OperationalError
        try:
            dbapi_con.ping()
        except OperationalError:
            raise DisconnectionError("Database server went away")

class Application(tornado.web.Application):

    def __init__(self, handlers, engine,**settings):

        engine = create_engine(engine,echo=False,
                                                pool_size=25,
                                                max_overflow=140,
                                                pool_recycle=40,
                                                pool_timeout=5,
                                                listeners=[MySQLPingListener()])
        session_factory = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
        self.db = session_factory()

        self.rcache = RedisManaher().cache_con()  #redis cache conn
        self.mcache = MemcacheManager().get_conn() #memcacx`he conn
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    parse_config_file(os.path.join(os.path.dirname(__file__),'web_conf.conf'))
    tornado.options.parse_command_line()
    try:
        port = int(sys.argv[1])
    except:
        port = 8000
    app = Application(handlers,options.ENGINE, **settings)

    app.sentry_client = AsyncSentryClient(
         'http://29ec306286ee48c081d5bebb791035ec:d53aa8788702465d863d3943306975d0@logs.gongzhuhao.com/2'
    )
    app.listen(port)
    print "Starting development server:",port
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()

