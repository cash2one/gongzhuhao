# encoding:utf-8
# !/usr/bin/env python

import tornado.ioloop
import tornado.web
from tornado.options import options
from apps_admin.urls import handlers
from common.urls import handlers as common_handlers
handlers.extend(common_handlers)
from apps_admin.home import AdminHandler
# handlers.extend(admin_handler)
handlers.append((r'/([\w\W]*)',AdminHandler))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.pool import NullPool

import sys,os
from utils.conf_util import parse_config_file
from setting import admin_settings
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
        self.mcache = MemcacheManager().get_conn() #memcache conn
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    parse_config_file(os.path.join(os.path.dirname(__file__),'web_conf.conf'))
    tornado.options.parse_command_line()
    try:
        port = int(sys.argv[1])
    except:
        port = 8030
    #if port in [8103,8009,8102]:
    app = Application(handlers,options.ENGINE, **admin_settings)
    app.sentry_client = AsyncSentryClient(
         'http://29ec306286ee48c081d5bebb791035ec:d53aa8788702465d863d3943306975d0@logs.gongzhuhao.com/2'
    )
    #else:
    #    app = Application(handlers,engine, **settings_mobile)
    app.listen(port)
    print "Starting development server:",port
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()

