#encoding:utf-8
__author__ = 'wangjinkuan'

from sqlalchemy import Column,Integer,String,DateTime,Boolean,SmallInteger,Date,TIMESTAMP
from sqlalchemy.sql.functions import now

from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, MetaData,ForeignKey

lstdata = [{'column_name':'Fprovince','column_type':'integer'},
          {'column_name':'Fcity','column_type':'integer'},
          {'column_name':'Farea','column_type':'integer'},
          {'column_name':'Fdetail_address','column_type':'varchar(256)'},
          {'column_name':'Faddress','column_type':'varchar(256)'},
          {'column_name':'Fsign_text','column_type':'varchar(256)','default':''},
          {'column_name':'Flast_visit','column_type':'datetime'},
          {'column_name':'Flast_visit_ip','column_type':'varchar(256)','default':''},
          {'column_name':'Fvisit_times','column_type':'integer','default':'0'},
          {'column_name':'Fcoin','column_type':'integer','default':'0'},
          {'column_name':'Femail_check_url','column_type':'varchar(256)','default':''}]

# alter table infos add ex tinyint not null default '0';

mysql_engine = create_engine('mysql://root:sunwang@127.0.0.1:3306/db_gongzhuhao?charset=utf8',encoding='utf-8', echo=True)

Session = sessionmaker(bind=mysql_engine)
session = Session()


def alter_table():
    for data in lstdata:
        if 'default' in data and 'varchar' in data.get('column_type'):
            sql = 'alter table t_users add'+' '+data.get('column_name')+' '+data.get('column_type')+' '+'default " "'
        elif 'default' in data:
            sql = 'alter table t_users add'+' '+data.get('column_name')+' '+data.get('column_type')+' '+'default'+' '+data.get('default')
        else:
            sql = 'alter table t_users add'+' '+data.get('column_name')+' '+data.get('column_type')
    # sql = 'alter table t_users add Flast_visit_date datetime'
        session.execute(sql)
        session.commit()

alter_table()













