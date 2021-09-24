import sqlalchemy
from sqlalchemy import text
from urllib.parse import quote_plus as urlquote
import base_engine as dao

if __name__ == '__main__':
    with dao.engine187.connect() as conn:
        sql = text("SELECT TOP 20 * FROM Lvjiaan.dbo.dim_address WHERE city_name=:city_code")

        result = conn.execute(sql, {"city_code": "宁波市"}).fetchall()
        for row in result:
            print(row)
