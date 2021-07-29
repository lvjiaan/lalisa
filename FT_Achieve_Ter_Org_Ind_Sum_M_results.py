import pymssql
from dateutil.relativedelta import relativedelta
import datetime


def conn():
    connect = pymssql.connect('192.168.0.210:1433', 'sa', 'wlzx@87811024', 'ResultsLibrary')  # 服务器名,账户,密码,数据库名
    if connect:
        print("210连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象

    time_now = datetime.datetime.now()
    for i in range(250):
        # summarymonth = (time_now + relativedelta(months=-i)).strftime("%Y%m")
        summarymonth = str(202012)

        # 插入
        # cursor.execute("EXEC Main_FT_Achieve_Ter_Org_Ind_Sum_M " + summarymonth + ";")
        print(summarymonth + "插入完成")

        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_city_results " + summarymonth + ";")
        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_province_results " + summarymonth + ";")
        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_cn_results " + summarymonth + ";")
        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_sh_results " + summarymonth + ";")
        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_nb_results " + summarymonth + ";")

        connect.commit()

        print(summarymonth + "更新完成")
        break

    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接
    return connect


if __name__ == '__main__':
    conn = conn()
