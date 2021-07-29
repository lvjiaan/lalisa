import pymssql
import sqlalchemy

# connect = pymssql.connect('192.168.4.187:1433', 'sa', 'zhangxueyang@2021', 'Lvjiaan',autocommit=True)  # 服务器名,账户,密码,数据库名
# if connect:
#     print("210连接成功!")
results=
engin = sqlalchemy.create_engine("mssql+pymssql://sa:wlzx87811024@172.16.5.45:1433/Lvjiaan")
results.to_sql("CT_IPC2", con=engin, index=False, if_exists='append')