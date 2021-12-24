import requests
from sqlalchemy import text
import sqlalchemy
from urllib.parse import quote_plus as urlquote
import db.base_engine as dao
import pandas as pd
import json

token_return = requests.get("http://www.nbippc.cn/Retrieval/getDiAccesstoken?appid=1051&appkey=1051")
token = token_return.json()['result']


def post_express(express, page):
    url = 'http://114.251.8.193/api/cse/search/expression?&scope=read_cn&client_id=5d8f767eac110007108d0e0a77f83ea8&access_token=%s&express=%s&page=%s&page_row=50' % (
        token, express, page)
    result = requests.post(url)
    with dao.engine187.connect() as conn:
        insert_sql = text(
            "INSERT INTO Lvjiaan.dbo.ju_json (json)VALUES(:json)")
        conn.execute(insert_sql, {"json": str(result.text)})
    return result


def to_db(data_list, table_name):
    engine = sqlalchemy.create_engine(
        "mssql+pymssql://sa:%s@192.168.4.187:1433/Lvjiaan" % urlquote('zhangxueyang@2021'))

    df = pd.DataFrame(data_list)
    df.to_sql(table_name, con=engine, index=False, if_exists='append')


def do_express():
    with dao.engine187.connect() as conn:
        sql = text(
            "SELECT DISTINCT unitname FROM Lvjiaan.dbo.ju_unit_name WHERE unitname IS NOT NULL AND unitname <>'' ")
        result = conn.execute(sql).fetchall()
        for row in result:
            unit_name = row[0]
            print(unit_name)
            express = '( ( 原告或上诉人 = %s OR 被告或被上诉人 = %s OR 原告代理机构 = %s OR 被告代理机构 = %s) )' % (
                unit_name, unit_name, unit_name, unit_name)
            post_result = post_express(express,1).json()
            total = int(post_result['total'])
            if total > 50:
                max_page = (total / 50) if (total % 50 == 0) else (total / 50 + 1)
                for x in range(2, int(max_page) + 1):
                    print(x)
                    rr=post_express(express,x)


def do_parse():
    with dao.engine187.connect() as conn:
        sql = text("SELECT DISTINCT json FROM Lvjiaan.dbo.ju_json WHERE json IS NOT NULL AND json <>'' ")
        rows = conn.execute(sql).fetchall()
        for row in rows:
            json_value = json.loads(row[0])
            if json_value['errorCode'] == '000000':
                print("return true")
                records = json_value['context']['records']
                to_db(records, 'ju_parse')


if __name__ == '__main__':
    do_express()
    # do_parse()
