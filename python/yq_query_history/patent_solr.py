import requests
from sqlalchemy import text
import sqlalchemy
# import pandas as pd
from urllib.parse import quote_plus as urlquote
import db.base_engine as dao
import pandas as pd


def post_patent_list_solr(patentee):
    url = 'http://api.sti.gov.cn/stiservice/sendMessage'
    token = requests.get(
        "http://api.sti.gov.cn/oauth/token?username=jeecg&grant_type=saml_auth&client_id=client_3&client_secret=s4DWmpkNm8HS").json()[
        'access_token']
    params = {
        'app_id': 'cfdc9a74030a41659cd43b887baf4800',
        'app_code': 'PatentList',
        'client_id': '1001',
        'client_secret': '1024',
        'server_name': 'PatentList',
        'params': '{"patentee":"%s"}' % (patentee),
        'method': 'POST'
    }
    headers = {
        'Authorization': 'bearer ' + token
    }
    post_result = requests.post(url, data=params, headers=headers)
    return post_result


if __name__ == '__main__':
    sheet = pd.read_excel('E:\\通商银行-测试企业名单.xlsx', sheet_name='Sheet1')
    query_ent_set = set(sheet['企业名称'].values)

    for row in sheet.itertuples():
        ent_name = row[1]
        credit_code = row[2]
        set_name = {ent_name, }
        with dao.engine187.connect() as conn:
            sql = text("SELECT unitId FROM Lvjiaan.dbo.ct_unit_change_record WHERE unitname=:unitname")
            result = conn.execute(sql, {"unitname": str(ent_name)}).fetchall()
            if len(result) >= 1:
                unitId = result[0][0]
                sql = text("SELECT unitName FROM Lvjiaan.dbo.ct_unit_change_record WHERE unitId=:unitId")
                result_name = conn.execute(sql, {"unitId": str(unitId)}).fetchall()
                if len(result_name) >= 1:
                    for name in result_name:
                        unitName = name[0]
                        set_name.add(unitName)
        print(set_name)
        for name in set_name:
            result = post_patent_list_solr(name)
            if result.json()['body']['data']['totalItemCount'] != 0:
                df = pd.DataFrame(result.json()['body']['data']['data'])
                df['creditCode'] = credit_code
                df['unitName'] = ent_name
                df.to_sql("a_test1", con=dao.engine187, index=False, if_exists='append')
