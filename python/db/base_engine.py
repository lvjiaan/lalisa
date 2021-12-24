import sqlalchemy
from sqlalchemy import text
from urllib.parse import quote_plus as urlquote

engine187 = sqlalchemy.create_engine("mssql+pymssql://sa:%s@192.168.4.187:1433/Lvjiaan" % urlquote('zhangxueyang@2021'))
engine72 = sqlalchemy.create_engine("mssql+pymssql://sa:%s@172.16.5.72:1433/lvjiaan" % urlquote('wlzx@87811024'))
engine74 = sqlalchemy.create_engine("mssql+pymssql://sa:%s@172.16.5.74:1433/lvjiaan" % urlquote('wlzx@87811024'))
engine174 = sqlalchemy.create_engine("mssql+pymssql://sa:%s@172.16.4.174:1433/InterfaceCollection" % urlquote('wlzx@87811024'))
