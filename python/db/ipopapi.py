import requests
import sqlalchemy
import pandas as pd
from urllib.parse import quote_plus as urlquote

token = requests.get("http://www.nbippc.cn/Retrieval/getDiAccesstoken?appid=1051&appkey=1051").json()['result']

if __name__ == '__main__':
    pno = "EP3561719A1"
    param = {
        "lang": "cn",
        "scope": "read_cn",
        "client_id": "5d8f767eac110007108d0e0a77f83ea8",
        "access_token": token,
        "pno": pno
    }

    result_json = requests.post("http://114.251.8.193/api/patent/detail/catalog", data=param)
    category_json = result_json.json()['context']['records'][0]['catalogPatent']

    engine = sqlalchemy.create_engine("mssql+pymssql://sa:%s@192.168.4.187:1433/Lvjiaan" % urlquote('zhangxueyang@2021'))

    df = pd.DataFrame([category_json])
    df.to_sql("CT_IPC2", con=engine, index=False, if_exists='append')

    print(result_json.json()['context']['records'][0]['catalogPatent']['lssc'])
