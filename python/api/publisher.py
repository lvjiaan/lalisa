import requests
from sqlalchemy import text
import sqlalchemy
# import pandas as pd
from urllib.parse import quote_plus as urlquote
import db.base_engine as dao
import pandas as pd

token_return = requests.get("http://www.nbippc.cn/Retrieval/getDiAccesstoken?appid=1051&appkey=1051")
token = token_return.json()['result']


def post_detail(pno):
    url = 'http://114.251.8.193/api/patent/detail/catalog'
    params = {
        "pno": pno,
        "lang": "cn",
        "scope": "read_cn",
        "client_id": "5d8f767eac110007108d0e0a77f83ea8",
        "access_token": token
    }
    result_json = requests.post(url, data=params)
    return result_json


def post_express2(express):
    url = 'http://114.251.8.193/api/patent/search/expression2?lang=cn&scope=read_us&client_id=5d8f767eac110007108d0e0a77f83ea8&access_token=%s&express=%s&page=1&page_row=10' % (
        token, express)
    # params = {
    #     "lang": "cn",
    #     "scope": "read_cn",
    #     "client_id": "5d8f767eac110007108d0e0a77f83ea8",
    #     "access_token": token,
    #     "express": express.encode('GBK'),
    #     "page": "1",
    #     "page_row": "10"
    # }
    result = requests.post(url)
    return result


def do_express2():
    with dao.engine187.connect() as conn:
        sql = text("SELECT DISTINCT apn_f FROM Lvjiaan.dbo.a_ex1 WHERE pid IS NULL AND apn_f IS NOT NULL")
        result = conn.execute(sql).fetchall()
        for row in result:
            apn = row[0]
            print(apn)
            post_result = post_express2('(申请号=(%s))' % (apn))
            if post_result.json()['total'] != '':
                pid = post_result.json()['context']['records'][0]['pid']
                pno = post_result.json()['context']['records'][0]['pno']
                sql = text("UPDATE Lvjiaan.dbo.a_ex1 SET pno=:pno,pid=:pid WHERE apn_f=:apn_f")
                conn.execute(sql, {"pno": str(pno), "pid": pid, "apn_f": str(apn)})


def do_law():
    url = "http://114.251.8.193/api/patent/detail/law"
    params = {
        "pid": "PIDEPA42017101100000000002169131I0RVHOC015F0B",
        "lang": "cn",
        "scope": "read_cn",
        "client_id": "5d8f767eac110007108d0e0a77f83ea8",
        "access_token": token
    }
    result_json = requests.post(url, data=params)
    print(result_json.json())
    records = result_json.json()['context']['records'][0]
    df = pd.DataFrame(records)
    df['pid'] = 'lvjiaan'
    df.to_sql("a_ct_law", con=dao.engine187, index=False, if_exists='append')


def post_patent_list_solr():
    params = {
        'app_id': 'cfdc9a74030a41659cd43b887baf4800',
        'app_code': 'PatentList',
        'client_id': '1001',
        'client_secret': '1024',
        'server_name': 'PatentList',
        'params': '{"patentee":"宁波爱科特生活电器有限公司","patentType":"2",grantDateStart:"20190101"}',
        'method': 'POST'
    }
    headers={
        'Authorization':'bearer '
    }


if __name__ == '__main__':
    # do_express2()
    do_law()
    # with dao.engine187.connect() as conn:
    #     sql = text("SELECT TOP 1 pno FROM Lvjiaan.dbo.a_t924 WHERE pid IS NULL")
    #     result = conn.execute(sql).fetchall()
    #     for row in result:
    #         pno = row[0]
    #         category_json = post_detail(pno).json()['context']['records'][0]['catalogPatent']
    #         pid = category_json['pid']
    #         sql = text("UPDATE Lvjiaan.dbo.a_t924 SET json=:json,pid=:pid WHERE pno=:pno")
    #         conn.execute(sql, {"json": str(category_json), "pid": pid, "pno": str(pno)})
