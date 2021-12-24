import json
import sqlalchemy
from sqlalchemy import text
import db.base_engine as dao
import pandas as pd
from urllib.parse import quote_plus as urlquote
if __name__ == '__main__':
    data_list = []

    with dao.engine174.connect() as conn:
        sql_select_json = text(
            "SELECT json_value FROM InterfaceCollection.Json.json_msa_change WHERE json_value like '%values%'")
        result = conn.execute(sql_select_json).fetchall()
        for row in result:
            json_value = json.loads(row[0])
            data = json_value[0]['values']
            data_list.append(data)


    engine = sqlalchemy.create_engine(
        "mssql+pymssql://sa:%s@172.16.4.174:1433/InterfaceCollection" % urlquote('wlzx@87811024'))

    df = pd.DataFrame(data_list)
    df.to_sql("parse_msa_change", con=engine, index=False, if_exists='append')

