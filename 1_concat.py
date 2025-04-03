# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 12:02:23 2025

@author: Roh Jun Seok

항공기 운항 실태 조사
2024년 1월~8월 국내노선 여객 이용률을 바탕으로

먼저 1월~8월 데이터를 통합
"""

import pandas as pd

# 1월부터 8월까지의 데이터를 통합
dfs = []

for i in range(1, 9):
    df = pd.read_csv(f'./data/2024년 {i}월 국내노선 여객 이용률.csv')
    # 이용율 컬럼을 하나로 보기 위해
    if '이용율' in df.columns:
        df = df.rename(columns={'이용율': '이용률'})
    df['월'] = i
    dfs.append(df)

total_df = pd.concat(dfs, ignore_index=True)
total_df.head()

total_df.to_csv('./data/merged_data.csv', index=False)