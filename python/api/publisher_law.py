import requests
from sqlalchemy import text
import sqlalchemy
from urllib.parse import quote_plus as urlquote
import db.base_engine as dao
import pandas as pd

token_return = requests.get("http://www.nbippc.cn/Retrieval/getDiAccesstoken?appid=1051&appkey=1051")
token = token_return.json()['result']


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
        sql = text("SELECT pid FROM Lvjiaan.dbo.a_1027 WHERE pid IS NOT NULL")
        result = conn.execute(sql).fetchall()
        for row in result:
            pid = row[0]
            print(pid)

            try:
                result = post_law(pid)
                records = result.json()['context']['records'][0]
                df = pd.DataFrame(records)
                df['pid'] = pid
                df.to_sql("ct_law_detail", con=dao.engine187, index=False, if_exists='append')

            except Exception:
                pass





if __name__ == '__main__':
    do_law()
    #update t1 set grantdate=t2.ilsad from Lvjiaan.dbo.a_1027 t1,Lvjiaan.dbo.a_ct_law t2 where t1.pid=t2.pid and t2.ilsso='授权' and t1.grantdate is null;

    # update t1 set grantdate=t2.ilsad from Lvjiaan.dbo.a_1027 t1,Lvjiaan.dbo.a_ct_law t2 where t1.pid=t2.pid and t2.ilssc like '%欧洲专利授权%' and t1.grantdate is null
