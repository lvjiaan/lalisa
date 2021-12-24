import requests
from sqlalchemy import text
import sqlalchemy
from urllib.parse import quote_plus as urlquote
import db.base_engine as dao
import pandas as pd
import requests
import datetime
import hashlib

url = 'http://e.cnipr.com/services/rs/score/loadScoreInfo'
api_key = "nbeval"
api_secret = "2ru3s34pk02r77cy"


def post_score(pn):
    params = {
        'pns': pn,
        'api_key': api_key,
        'sign': sign(pn)
    }
    result = requests.get(url, params=params)
    return result


def sign(pn):
    original_str = pn + api_key + api_secret + datetime.datetime.now().strftime("%Y%m%d%H")
    md = hashlib.md5()
    md.update(original_str.encode('ascii'))
    md_digest = md.digest()
    str2 = ''
    for val in md_digest:
        val = val & 0xFF
        if val <= 15:
            str2 += '0'
        str2 += format(val, 'x')
    return str2.lower()


def do_():
    with dao.engine187.connect() as conn:
        sql = text("SELECT DISTINCT pno FROM Lvjiaan.dbo.a_1027 WHERE pno IS not NULL and score is null")
        result = conn.execute(sql).fetchall()
        for row in result:
            apn = row[0]
            print(apn.replace('/', '\/'))
            post_result = post_score(apn.replace('/', '\/'))
            try:
                score = post_result.json()['score']
                sql = text(
                    "UPDATE Lvjiaan.dbo.a_1027 SET score=:score WHERE pno=:apn")
                conn.execute(sql, {"score": str(score),"apn":str(apn)})
            except Exception:
                pass


if __name__ == '__main__':
    do_()
