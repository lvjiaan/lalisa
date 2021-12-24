import json
import sqlalchemy
from sqlalchemy import text
import db.base_engine as dao
import pandas as pd
from urllib.parse import quote_plus as urlquote

if __name__ == '__main__':
    data_list = []

    with dao.engine72.connect() as conn:
        sql_select_json = text(
            "SELECT json FROM PublicInterface.Patents.T_Publisher WHERE json like '%pa%'")
        result = conn.execute(sql_select_json).fetchall()
        for row in result:
            json_value = json.loads(row[0])
            data = json_value['indexInfo']
            data['an'] = json_value['an']
            data['pn'] = json_value['pn']
            data_list.append(data)

    engine = sqlalchemy.create_engine(
        "mssql+pymssql://sa:%s@172.16.5.72:1433/PublicInterface" % urlquote('wlzx@87811024'))

    df = pd.DataFrame(data_list)
    df.to_sql("parse_publisher", con=engine, index=False, if_exists='append')
