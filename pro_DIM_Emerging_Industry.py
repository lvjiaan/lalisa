import xlrd
import pymssql
import re

wb = xlrd.open_workbook(filename='C:\\Users\\AOC\Desktop\\777.xlsx')

sheet1 = wb.sheet_by_index(0)

smallcode = "null"
smallname = "null"
keyWords = "null"
bigcode = "null"
bigname = "null"


def execSql(sql):
    connect = pymssql.connect('192.168.0.210:1433', 'sa', 'wlzx@87811024', 'ResultsLibrary',
                              autocommit=True)  # 服务器名,账户,密码,数据库名
    if connect:
        print("210连接成功!")
    cursor = connect.cursor()  # 创建一个游标对象
    cursor.execute(sql)
    print("insert success")
    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接
    return connect


def matchNo(str):
    matchNo = re.findall(r'\(不含(.*?)\)', str)
    m2 = "、".join(matchNo)
    return m2


def matchIn(str):
    m2 = re.sub(r'\(不含.*?\)', '', str)
    return m2


for i in range(2, sheet1.nrows):
    rows = sheet1.row_values(i)
    if rows[2] == '':
        bigcode = rows[0]
        bigname = rows[1]
        continue
    if rows[0] != '':
        smallcode = str(rows[0])
    if rows[1] != '':
        smallname = rows[1]

    list = re.findall(r'(.*?(?:\(.*?\))?)、', rows[2] + '、')
    keyWords = rows[3]
    for x in list:
        print(x)
        classifyOut = matchNo(x)
        classifyIn = matchIn(x)
        sql = "insert into dbo.DIM_Emerging_Industry(bigcode,bigname,smallcode,smallname,classifyIn,classifyOut,keyWords)values('%s','%s','%s','%s','%s','%s','%s')" % (
            str(bigcode).split('.')[0], bigname, str(smallcode).split('.')[1], smallname, classifyIn, classifyOut,
            keyWords)
        print(sql)
        execSql(sql)
