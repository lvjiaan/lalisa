import pymssql
from dateutil.relativedelta import relativedelta
import datetime

def conn():
    connect = pymssql.connect('192.168.0.210:1433', 'sa', 'wlzx@87811024', 'nbResultsLibrary') #服务器名,账户,密码,数据库名
    if connect:
        print("210连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象

    time_now = datetime.datetime.now()
    for i in range(1,250):
        summarymonth = (time_now + relativedelta(months=-i)).strftime("%Y%m")

        if summarymonth==200912:
            return

        cursor.execute("EXEC Ins_Up_FT_Achieve_Agency_Org_Sum_M " + summarymonth + ";")
        connect.commit()  # 提交

        print(summarymonth + "更新完成")

    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接
    return connect


if __name__ == '__main__':
    conn = conn()