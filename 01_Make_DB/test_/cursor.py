#!/usr/local/bin/python3

import psycopg2
import pandas as pd
from sqlalchemy import create_engine

#データベースから　データを取得する
engine = create_engine('postgresql://pison:Ramen!yokosuka2023@localhost:5432/pison')
connection = engine.connect()
#df = pd.read_sql('SELECT * FROM dummy', connection)
df = pd.read_sql('DROP TABLE as_dummy_test', connection)
connection.close()
print(df)
