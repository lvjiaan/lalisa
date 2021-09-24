
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
    for i in tables:
        print("sqoop eval --connect 'jdbc:sqlserver://192.168.0.210:1433;database=ResultsLibrary' --username 'sa' --password 'wlzx@87811024' --query \"TRUNCATE table dbo.%s;\"" % (i))
        print("hive -e \"insert overwrite  directory '/testDir/status/test' STORED AS textfile select * from achievement.%s;\""%(i))
        print("sqoop export --connect 'jdbc:sqlserver://192.168.0.210:1433;database=ResultsLibrary' --username 'sa' --password 'wlzx@87811024' --table '%s' --fields-terminated-by '\\0x01' --export-dir '/testDir/status/test' --input-null-string '\\\\N' --input-null-non-string '\\\\N'"%(i))
        print("\n")
