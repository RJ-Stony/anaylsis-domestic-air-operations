# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:53:40 2025

@author: Roh Jun Seok

전처리된 데이터 sql에 저장
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine

# 실행해야 MySQLdb import 가능
pymysql.install_as_MySQLdb()

import MySQLdb

host = 'localhost'
user = 'root'
pw = 'pw'
db = 'test'
charset = 'utf8'

df = pd.read_csv('./data/final_data.csv')
df.head()
df.info()

# 1. mysql 엔진이 다양하기에 엔진 객체 먼저 만들기
# 2. mysql에 mysqldb 연결
# 3. @로 host 지정
engine = create_engine(f'mysql+mysqldb://{user}:{pw}@{host}/{db}')
conn = engine.connect()

df.to_sql(name='airline_final', con=engine, if_exists='replace', index=False)

conn.close()