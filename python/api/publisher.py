import requests
from sqlalchemy import text
import sqlalchemy
import pandas as pd
from urllib.parse import quote_plus as urlquote
import db.base_engine as dao

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


if __name__ == '__main__':
    with dao.engine187.connect() as conn:
        sql = text("SELECT TOP 1 pno FROM Lvjiaan.dbo.a_t924 WHERE pid IS NULL")
        result = conn.execute(sql).fetchall()
        for row in result:
            pno = row[0]
            category_json = post_detail(pno).json()['context']['records'][0]['catalogPatent']
            pid = category_json['pid']
            sql = text("UPDATE Lvjiaan.dbo.a_t924 SET json=:json,pid=:pid WHERE pno=:pno")
            conn.execute(sql, {"json": str(category_json), "pid": pid, "pno": str(pno)})
