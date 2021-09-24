
tables=[
# 'LT_Patent_Main',
'LT_Patent_Permission',
'LT_Patent_Pledge',
'LT_Patent_Transfer',
'LT_Patent_Transfer_City',
# 'RT_Patent_Citation',
# 'RT_Patent_Ethnic',
'RT_Patent_Industry_246',
'RT_Patent_Industry_Classify',
# 'RT_Patent_Industry_Strategic',
# 'RT_Patent_Industry_Tag',
# 'RT_Patent_Industry_Technosphere',
'RT_Patent_inventor',
'RT_Patent_Ipc',
'RT_Patent_Original_Apply_Person',
'RT_Patent_Original_Grant_Patentee',
'RT_Patent_Patentee_Valid_Section',
'RT_Patent_Permission_Assignor',
'RT_Patent_Permission_Transferee',
'RT_Patent_Pledge_Mortgagor',
'RT_Patent_Pledge_Pledgee',
# 'RT_Patent_Priority',
'RT_Patent_Public_Num',
'RT_Patent_Transfer_After_Person',
'RT_Patent_Transfer_Before_Person'];


#表 列表
if __name__ == '__main__':
    # info=['a_applynum_wx','WuxiTheme'] #无锡
    # info = ['a_applynum_qd', 'QingdaoTheme']  # 青岛
    # info = ['a_applynum_hz', 'HangzhouTheme'] #杭州
    info = ['a_applynum_nb', 'NingboTheme'] #宁波
    # info = ['a_applynum_zj', 'ZhejiangTheme']

    print("sqoop eval --connect 'jdbc:sqlserver://192.168.4.187:1433;database=%s' --username 'sa' --password 'zhangxueyang@2021' --query \"TRUNCATE table dbo.LT_Patent_Main;\""%(info[1]))
    print("hive -e \"insert overwrite  directory '/testDir/status/test' STORED AS textfile SELECT id,applyNum,patentName,yearid,applyDate,publicDate,grantDate,expireDate,expireReason,patentType,statusCode,isPct,isGrant,publicNum,publicAllNum,mainIpc,ipc,priorityInfo,inventroName,applyPersonid,applyPersonName,applyPersonType,applyPersonAddr,applyProvinceCode,applyProvinceName,applyCityCode,applyCityName,applyDistrictCode,applyDistrictName,applyNbDistrictCode,applyNbDistrictName,grantPersonId,grantPersonName,grantPersonType,grantPersonAddr,grantProvinceCode,grantProvinceName,grantCityCode,grantCityName,grantDistrictCode,grantDistrictName,grantNbDistrictCode,grantNbDistrictName,patenteeId,patentee,patenteeType,patenteeAddr,patenteeProvinceCode,patenteeProvinceName,patenteeCityCode,patenteeCityName,patenteeDistrictCode,patenteeDistrictName,patenteeStreetCode,patenteeStreetName,ningboDistrictCode,ningboDistrictName,agencyId,agencyName,agencyCityCode,agentName,censor,processCreateTime,processUpdateTime,claimsPath,instrPath,internationalApply,internationalPublic,summaryInfo,mainlocarno,patentscore,patentvalue,isPledge FROM achievement.lt_patent_main_tomodel where applynum in (select applynum from achievement.%s);\""%(info[0]))
    print(
        "sqoop export --connect 'jdbc:sqlserver://192.168.4.187:1433;database=%s' --username 'sa' --password 'zhangxueyang@2021' --table 'LT_Patent_Main' --fields-terminated-by '\\0x01' --export-dir '/testDir/status/test' --input-null-string '\\\\N' --input-null-non-string '\\\\N'" % (
        info[1]))
    print("\n")

    for i in tables:
        print(
            "sqoop eval --connect 'jdbc:sqlserver://192.168.4.187:1433;database=%s' --username 'sa' --password 'zhangxueyang@2021' --query \"TRUNCATE table dbo.%s;\"" % (
            info[1],i))
        print("hive -e \"insert overwrite  directory '/testDir/status/test' STORED AS textfile select * from achievement.%s where applynum in (select applynum from achievement.%s);\""%(i,info[0]))
        print("sqoop export --connect 'jdbc:sqlserver://192.168.4.187:1433;database=%s' --username 'sa' --password 'zhangxueyang@2021' --table '%s' --fields-terminated-by '\\0x01' --export-dir '/testDir/status/test' --input-null-string '\\\\N' --input-null-non-string '\\\\N'"%(info[1],i))
        print("\n")
