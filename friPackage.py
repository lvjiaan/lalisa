import os, zipfile
import pymssql, openpyxl, time
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText


# 执行sql，导出生成excel
def conn(sql, table_name):
    connect = pymssql.connect('192.168.0.210:1433', 'sa', 'wlzx@87811024', 'ResultsLibrary')
    if connect:
        print("210连接成功!")
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

    file = open('//tsclient/D/%s/%s.xlsx' % (today, table_name), 'wb')  # 系统盘路径会拒绝访问
    book.save(file)
    print('%s文件生成成功' % table_name)

    cur.close()  # 关闭游标
    connect.close()
    return connect


# # 发送邮件
# def send_email(today):
#     smtpserver = 'smtp.163.com'
#
#     # 发送者
#     sender = '13003782538@163.com'
#     password = 'EPQAFLWTKVGPWCNA'
#
#     content = '【测试】专利考核四表每周五打包给需求组，日期：%s' % today
#     subject = '专利考核周五打包%s' % today
#
#     # 接收者
#     receivers = ['873134524@qq.com', '928118664@qq.com']
#
#     msg = MIMEMultipart()
#     msg.attach(MIMEText(content, 'plain', 'utf-8'))
#     msg['Subject'] = Header(subject, 'utf-8')
#     msg['From'] = '13003782538<13003782538@163.com>'
#     msg['To'] = '873134524<873134524@qq.com>,928118664<928118664@qq.com>'
#
#     # 加入附件
#     zipApart = MIMEApplication(open('E:/[%s]专利考核四表汇总.zip' % today, 'rb').read())
#     zipApart.add_header('Content-Disposition', 'attachment', filename='%s专利考核四表汇总.zip' % today)
#     msg.attach(zipApart)
#     try:
#         server = smtplib.SMTP(smtpserver)
#         server.login(sender, password)
#         server.sendmail(sender, receivers, msg.as_string())
#         print('邮件发送成功')
#         server.quit()
#     except smtplib.SMTPException as e:
#         print('error:', e)  # 打印错误


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
    today = time.strftime("%Y%m%d", time.localtime(time.time()))
    os.mkdir('//tsclient/D/%s' % today)

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
    zipFile = '//tsclient/D/[%s]专利考核四表汇总.zip' % today
    make_zip('//tsclient/D/%s' % today, zipFile)
    print('打包文件生成成功，路径  %s' % zipFile)
    # 发送邮件
    # send_email(today)

    # shutil.rmtree('F:/%s' % today)
    # os.remove(zipFile)
    # print('本地文件已删除')
