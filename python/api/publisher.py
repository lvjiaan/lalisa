import requests
from sqlalchemy import text
import sqlalchemy
from urllib.parse import quote_plus as urlquote
import db.base_engine as dao
import pandas as pd

token_return = requests.get("http://www.nbippc.cn/Retrieval/getDiAccesstoken?appid=1051&appkey=1051")
token = token_return.json()['result']


def post_detail(pid):
    url = 'http://114.251.8.193/api/patent/detail/catalog'
    params = {
        "pid": pid,
        "lang": "cn",
        "scope": "read_cn",
        "client_id": "5d8f767eac110007108d0e0a77f83ea8",
        "access_token": token
    }
    result_json = requests.post(url, data=params)
    return result_json


def post_express2(express):
    url = 'http://114.251.8.193/api/patent/search/expression2?lang=cn&scope=read_cn&client_id=5d8f767eac110007108d0e0a77f83ea8&access_token=%s&express=%s&page=1&page_row=10' % (
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


def post_express(express):
    url = 'http://114.251.8.193/api/patent/search/expression?lang=cn&scope=read_tw&client_id=5d8f767eac110007108d0e0a77f83ea8&access_token=%s&express=%s&page=1&page_row=10' % (
        token, express)
    result = requests.post(url)
    return result


def do_express2():
    with dao.engine187.connect() as conn:
        sql = text("SELECT DISTINCT apn_f FROM Lvjiaan.dbo.a_ex3 WHERE pid IS NULL ")
        result = conn.execute(sql).fetchall()
        for row in result:
            apn = row[0]
            print(apn)
            post_result = post_express2('(申请号=(%s))' % (apn))
            if post_result.json()['total'] != '':
                pid = post_result.json()['context']['records'][0]['pid']
                pno = post_result.json()['context']['records'][0]['pno']
                sql = text("UPDATE Lvjiaan.dbo.a_ex3 SET pno=:pno,pid=:pid WHERE apn_f=:apn_f")
                conn.execute(sql, {"pno": str(pno), "pid": pid, "apn_f": str(apn)})


def post_law(pid):
    url = "http://114.251.8.193/api/patent/detail/law"
    params = {
        "pid": pid,
        "lang": "cn",
        "scope": "read_cn",
        "client_id": "5d8f767eac110007108d0e0a77f83ea8",
        "access_token": token
    }
    post_result = requests.post(url, data=params)
    return post_result


def do_law():
    with dao.engine187.connect() as conn:
        sql = text("SELECT pid FROM Lvjiaan.dbo.a_ex2 WHERE pid IS NOT NULL AND grant_date IS NULL")
        result = conn.execute(sql).fetchall()
        for row in result:
            pid = row[0]
            print(pid)

            try:
                result = post_law(pid)
                records = result.json()['context']['records'][0]
                df = pd.DataFrame(records)
                df['pid'] = pid
                df.to_sql("a_ct_law", con=dao.engine187, index=False, if_exists='append')

            except Exception:
                pass


def post_patent_list_solr(apn):
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
        'params': '{"applyNum":"%s"}' % (apn),
        'method': 'POST'
    }
    headers = {
        'Authorization': 'bearer ' + token
    }
    post_result = requests.post(url, data=params, headers=headers)
    return post_result


def do_solr():
    with dao.engine187.connect() as conn:
        sql = text(
            "SELECT DISTINCT apn_f FROM Lvjiaan.dbo.a_ex2 WHERE patent_name IS NULL AND apn_f IS NOT NULL AND PATENT_name is null")
        result = conn.execute(sql).fetchall()
        for row in result:
            apn = row[0]
            print(apn)
            post_result = post_patent_list_solr(apn)
            if post_result.json()['body']['data']['totalItemCount'] != 0:
                patentee = ''
                patentname = post_result.json()['body']['data']['data'][0]['patentname']
                statuscode = post_result.json()['body']['data']['data'][0]['statuscode']
                grantdate = post_result.json()['body']['data']['data'][0]['grantdate']
                try:
                    patentee = post_result.json()['body']['data']['data'][0]['patentee']
                except Exception:
                    pass
                # pno = post_result.json()['body']['data']['data'][0]['publicnum']

                sql = text(
                    "UPDATE Lvjiaan.dbo.a_ex2 SET patent_name=:patent_name,patentee=:patentee,grant_date=:grant_date,status_code=:status_code WHERE apn_f=:apn_f")
                conn.execute(sql, {"patent_name": str(patentname), "patentee": patentee, "grant_date": grantdate,
                                   "status_code": statuscode, "apn_f": str(apn)})


def do_solr_ex4():
    with dao.engine187.connect() as conn:
        sql = text(
            "SELECT DISTINCT apn_f FROM Lvjiaan.dbo.a_ex4 WHERE patent_name IS NULL AND apn_f IS NOT NULL AND PATENT_name is null")
        result = conn.execute(sql).fetchall()
        for row in result:
            apn = row[0]
            print(apn)
            post_result = post_patent_list_solr(apn)
            if post_result.json()['body']['data']['totalItemCount'] != 0:
                patentname = post_result.json()['body']['data']['data'][0]['patentname']
                applyname = post_result.json()['body']['data']['data'][0]['applypersonname']
                applydate = post_result.json()['body']['data']['data'][0]['applydate']
                # pno = post_result.json()['body']['data']['data'][0]['publicnum']

                sql = text(
                    "UPDATE Lvjiaan.dbo.a_ex4 SET patent_name=:patent_name,apply_name=:apply_name,apply_date=:apply_date WHERE apn_f=:apn_f")
                conn.execute(sql, {"patent_name": str(patentname), "apply_name": applyname, "apply_date": applydate,
                                   "apn_f": str(apn)})


def do_detail():
    with dao.engine187.connect() as conn:
        sql = text("SELECT pid FROM Lvjiaan.dbo.a_ex3 WHERE pid IS NOT NULL AND patent_name IS NULL")
        result = conn.execute(sql).fetchall()
        for row in result:
            pid = row[0]
            print(pid)
            category_json = post_detail(pid).json()['context']['records'][0]['catalogPatent']
            print(category_json)

            patentname = category_json['tio']
            apply_name = category_json['apo']

            apply_date = category_json['ad']
            sql = text(
                "UPDATE Lvjiaan.dbo.a_ex3 SET patent_name=:patent_name,apply_name=:apply_name,apply_date=:apply_date WHERE pid=:pid")
            conn.execute(sql, {"patent_name": str(patentname), "apply_name": apply_name,
                               "apply_date": apply_date, "pid": str(pid)})


def do_detail2():
    with dao.engine187.connect() as conn:
        sql = text("SELECT pid FROM Lvjiaan.dbo.a_ex1 WHERE pid IS NOT NULL AND patent_name IS NULL")
        result = conn.execute(sql).fetchall()
        for row in result:
            pid = row[0]
            print(pid)
            category_json = post_detail(pid).json()
            sql = text(
                "UPDATE Lvjiaan.dbo.a_ex1 SET json=:json WHERE pid=:pid")
            conn.execute(sql, {"json": str(category_json), "pid": str(pid)})


def do_express():
    with dao.engine187.connect() as conn:
        sql = text("SELECT DISTINCT applynum FROM Lvjiaan.dbo.a_1027 WHERE applynum IS NOT NULL AND tio is NULL")
        result = conn.execute(sql).fetchall()
        for row in result:
            apn = row[0]
            print(apn)
            post_result = post_express('(公布号=(%s))' % (apn.replace('/', '\/')))
            try:
                if post_result.json()['total'] == '':
                    continue
                list_records = post_result.json()['context']['records']
                tio = ''
                aso = ''
                lssc = ''
                apo = ''
                ad = ''
                print(list_records)
                for record in list_records:
                    try:
                        if tio == '':
                            tio = record['tio']
                    except Exception:
                        pass
                    try:
                        if aso == '':
                            aso = record['aso']
                    except Exception:
                        pass
                    try:
                        if lssc == '':
                            lssc = record['lsscn']
                    except Exception:
                        pass
                    try:
                        if apo == '':
                            apo = record['apo']
                    except Exception:
                        pass
                    try:
                        if ad == '':
                            ad = record['ad'].split(' ')[0].replace('/', '')
                    except Exception:
                        pass

                sql = text(
                    "UPDATE Lvjiaan.dbo.a_1027 SET tio=:tio,aso=:aso,lssc=:lssc,apo=:apo,ad=:ad WHERE applynum=:applynum")
                conn.execute(sql,
                             {"tio": str(tio), "aso": aso, "apo": apo, "lssc": lssc, "ad": ad, "applynum": str(apn)})
            except Exception:
                pass

            # break


if __name__ == '__main__':
    do_express()

    # do_solr_ex4()
    # do_express2()
    # do_detail()
    # do_law()
