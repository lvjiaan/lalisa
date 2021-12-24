import requests
from sqlalchemy import text
import sqlalchemy
from urllib.parse import quote_plus as urlquote
import db.base_engine as dao
import pandas as pd

token_return = requests.get("http://www.nbippc.cn/Retrieval/getDiAccesstoken?appid=1051&appkey=1051")
token = token_return.json()['result']



def post_express2(express):
    url = 'http://114.251.8.193/api/patent/search/expression2?lang=cn&scope=read_tw&client_id=5d8f767eac110007108d0e0a77f83ea8&access_token=%s&express=%s&page=1&page_row=10' % (
        token, express)
    result = requests.post(url)
    return result



def do_express2():
    with dao.engine187.connect() as conn:
        sql = text("SELECT DISTINCT applynum FROM Lvjiaan.dbo.a_1027 WHERE pid IS NULL ")
        result = conn.execute(sql).fetchall()
        for row in result:
            apn = row[0]
            print(apn.replace('/','\/'))
            post_result = post_express2('(公布号=(%s))' % (apn.replace('/','\/')))
            if post_result.json()['total'] != '':
                pid = post_result.json()['context']['records'][0]['pid']
                pno = post_result.json()['context']['records'][0]['pno']
                sql = text("UPDATE Lvjiaan.dbo.a_1027 SET pno=:pno,pid=:pid WHERE applynum=:apn_f")
                conn.execute(sql, {"pno": str(pno), "pid": pid, "apn_f": str(apn)})



if __name__ == '__main__':
    do_express2()
