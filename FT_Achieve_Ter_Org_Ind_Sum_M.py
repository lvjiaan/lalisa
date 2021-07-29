import pymssql
from dateutil.relativedelta import relativedelta
import datetime


def conn():
    connect = pymssql.connect('192.168.0.210:1433', 'sa', 'wlzx@87811024', 'ResultsLibrary')  # 服务器名,账户,密码,数据库名
    if connect:
        print("210连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象

    time_now = datetime.datetime.now() + relativedelta(months=-2)
    for i in range(100):
        # 统计月份设定
        summarymonth = (time_now + relativedelta(months=-i)).strftime("%Y%m")
        # summarymonth = str(202101)

        # cursor.execute("EXEC Main_FT_Achieve_Ter_Org_Ind_Sum_M "+summarymonth+";")  # 执行sql语句
        print(summarymonth + "开始处理")

        # 全国
        # cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_cn " + summarymonth + ";")
        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_cn_results " + summarymonth + ";")

        # 各省
        # cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_province " + summarymonth + ";")
        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_province_results " + summarymonth + ";")

        # 各市
        # cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_city " + summarymonth + ";")
        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_city_results " + summarymonth + ";")

        # 宁波 各区、四区一岛、街道
        # cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_nb " + summarymonth + ";")
        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_nb_results " + summarymonth + ";")

        # 上海 各区
        # cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_sh " + summarymonth + ";")
        cursor.execute("EXEC Up_FT_Achieve_Ter_Org_Ind_Sum_M_00_sh_results " + summarymonth + ";")

        connect.commit()  # 提交
        print(summarymonth + "更新完成")

        # 只更新一个月
        # break

    # cursor.execute("UPDATE [dbo].[FT_Achieve_Ter_Org_Ind_Sum_M] set isLastMonth=0 where summaryMonth=202012;")
    # cursor.execute("UPDATE [dbo].[FT_Achieve_Ter_Org_Ind_Sum_M] set isLastMonth=1 where summaryMonth=202101;")
    connect.commit()  # 提交

    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接
    return connect

if __name__ == '__main__':
    conn = conn()
