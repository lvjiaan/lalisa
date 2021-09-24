import os, zipfile
import pymssql, openpyxl, time


def conn(sql, table_name):
    connect = pymssql.connect('192.168.4.187:1433', 'sa', 'zhangxueyang@2021', 'NingboTheme')
    print(connect)
    if connect:
        print("测试187连接成功!")
    cur = connect.cursor()
    cur.execute(sql)

    fields = [field[0] for field in cur.description]  # 获取所有字段名
    all_data = cur.fetchall()  # 所有数据

    book = openpyxl.Workbook()
    sheet = book.active

    for col, field in enumerate(fields):
        sheet.cell(1, col + 1, field)

    row = 2
    for data in all_data:
        for col, field in enumerate(data):
            sheet.cell(row, col + 1, field)
        row += 1
    today = time.strftime("%Y%m%d", time.localtime(time.time()))

    file = open('D:/%s/%s.xlsx' % (today, table_name), 'wb')  # 系统盘路径会拒绝访问
    book.save(file)
    print('%s文件生成成功' % table_name)

    cur.close()  # 关闭游标
    connect.close()
    return connect


# 文件夹打包zip
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


if __name__ == '__main__':
    input("please input any key to start!")
    today = time.strftime("%Y%m%d", time.localtime(time.time()))
    os.mkdir('D:/%s' % today)

    conn1 = conn(
        'SELECT summaryMonth, applyNum, applyDate, grantDate, patentName, patentType, patentTypeName, patenteeType, patenteeName, patenteeAddr, provinceCode, provinceName, cityCode, cityName, districtCode, districtName, functionCode, functionName, streetCode, streetName, mainIpc, agencyId, agencyName, postalcode FROM LT_Patent_Valid',
        '有效表')
    conn2 = conn(
        'SELECT summaryMonth, applyNum, recieveDate, internationalApplyDate, applyPersonName, applyPersonAddr, countryCode, provinceCode, provinceName, cityCode, cityName, cityNameEn, districtCode, districtName, functionCode, functionName, streetCode, streetName, steetNameEn, mainIpc, agencyId, agencyName, isPayFee, industryTagId FROM LT_Patent_PCT_Apply where dataType in (101,201)',
        'PCT表')
    conn3 = conn(
        'SELECT summaryMonth, applyNum, applyDate, grantDate, patentName, patentType, patentTypeName, patenteeName, patenteeType, patenteeAddr, provinceCode, provinceName, cityCode, cityName, districtCode, districtName, functionCode, functionName, streetCode, streetName, mainIpc, postalcode, agencyId, agencyName FROM LT_Patent_Grant where dataType in (101,201)',
        '授权表')
    conn4 = conn(
        'SELECT summaryMonth, applyPersonName, applypersonType, patentTypeCode, patentTypeName, applyDate, patentNum, applyPersonAddr,provinceCode,provinceName,cityCode,cityName,districtCode, districtName, isLandFourAreaCode, isLandFourAreaName, streetCode, streetName, functionCode, functionName,agencyId,agencyName,postalcode,applyMethod FROM DBO.LT_Patent_Apply_Num where dataType in (101,201)',
        '申请表')
    zipFile = 'D:/[%s]专利考核四表汇总.zip' % today
    make_zip('D:/%s' % today, zipFile)
    print('打包文件生成成功，路径  %s' % zipFile)
    input("please input any key to exit!")