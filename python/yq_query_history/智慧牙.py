import requests
from sqlalchemy import text
import sqlalchemy
# import pandas as pd
from urllib.parse import quote_plus as urlquote
import db.base_engine as dao
import pandas as pd
import json

if __name__ == '__main__':
    with dao.engine187.connect() as conn:
        sql = text(
            "SELECT publicNum FROM Lvjiaan.dbo.a_test1 WHERE publicNum NOT IN (SELECT publicNUm FROM Lvjiaan.dbo.a_score)")
        result = conn.execute(sql).fetchall()
        for row in result:
            publicNum = row[0]
            get_result_json = requests.get("http://www.nbippc.cn/Valuation/Zhihuiya", params={"pn": publicNum}).text
            format_str = get_result_json.replace('\\n', '').replace('\\', '').replace(' ', '')[2:-2]

            try:
                json_list = [json.loads(format_str), ]
                print(json_list)

                df = pd.DataFrame(list(json_list))

                df['publicNum'] = publicNum
                df.to_sql("a_score", con=dao.engine187, index=False, if_exists='append')
                # break
            except Exception:
                pass
