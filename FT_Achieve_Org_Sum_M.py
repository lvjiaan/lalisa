import pymssql
from dateutil.relativedelta import relativedelta
import datetime

def conn():
    connect = pymssql.connect('192.168.0.210:1433', 'sa', 'wlzx@87811024', 'ResultsLibrary') #服务器名,账户,密码,数据库名
    if connect:
        print("210连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象

    time_now = datetime.datetime.now() + relativedelta(months=-3)
    for i in range(100):


        summarymonth = (time_now + relativedelta(months=-i)).strftime("%Y%m")

        print(summarymonth + "开始执行")
        datetime.time.sleep(2000)
        # cursor.execute("EXEC Ins_Up_FT_Achieve_Org_Sum_M "+summarymonth+";")  # 执行sql语句
        cursor.execute("EXEC Ins_Up_FT_Achieve_Org_Sum_M_nb "+summarymonth+";")  # 执行sql语句

        connect.commit()  # 提交
        print(summarymonth + "插入更新完成")

    # cursor.execute("update FT_Achieve_Org_Sum_M set islastmonth =1 where summarymonth = 202101;")  # 执行sql语句
    # cursor.execute("update FT_Achieve_Org_Sum_M set islastmonth =0 where summarymonth = 202011;")  # 执行sql语句
    connect.commit()  # 提交
    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接
    return connect


# 201805

if __name__ == '__main__':
    conn = conn()