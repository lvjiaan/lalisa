import pymssql

connect = pymssql.connect('192.168.4.187:1433', 'sa', 'zhangxueyang@2021', 'Lvjiaan',autocommit=True)  # 服务器名,账户,密码,数据库名
if connect:
    print("210连接成功!")