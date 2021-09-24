import pymssql
from dateutil.relativedelta import relativedelta
import datetime

#######专利考核 汇总 存储过程
def conn():
    connect = pymssql.connect('192.168.0.210:1433', 'sa', 'wlzx@87811024', 'ResultsLibrary') #服务器名,账户,密码,数据库名
    if connect:
        print("210连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象

    time_now = datetime.datetime.now() + relativedelta(months=-1)
    for i in range(100):
        summarymonth = (time_now + relativedelta(months=-i)).strftime("%Y%m")
        print(summarymonth)
        # if summarymonth==201912:
        #     return
        # 区县
        cursor.execute("EXEC Up_FT_Patents_Ter_Eva_Sum_M "+summarymonth+";")
        # 街道
        cursor.execute("EXEC Up_FT_Patents_Ter_Eva_Sum_M_street " + summarymonth + ";")
        connect.commit()  # 提交
        print(summarymonth + "更新完成")
    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接
    return connect

if __name__ == '__main__':
    conn = conn()