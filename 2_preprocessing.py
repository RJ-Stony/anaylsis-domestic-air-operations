"""
데이터 통합 후에 전처리
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 표기
from matplotlib import font_manager, rc
import platform

if platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
else:
    print('Check your OS system')

df = pd.read_csv('./data/merged_data.csv')

# 결측치 확인
df.isna().sum()
'''
항공사    1
유아     2
'''
# 포항경주-인천 노선은 존재 X, 이용률도 0.0이기 때문에 삭제 조치
df[df['노선'].str.contains('포항경주', na=False)]
df = df[df['노선'] != '포항경주-인천'].reset_index(drop=True)
df.info()

# 유아 수 = 여객 수 - 성인인데, 
# 해당 행에서는 성인 = 여객수이므로 유아에는 fillna(0) 처리
df.iloc[334:336]
df['유아'] = df['유아'].fillna(0).astype(int)
df.info()

# 노선을 분리해서 출발과 도착 컬럼 생성
df[['출발', '도착']] = df['노선'].str.split('-', expand=True)

# 컬럼 순서 재배치
columns = ['월', '출발', '도착', '노선', '항공사', '좌석수', '성인', '유아', '여객수', '이용률']
df = df[columns]
df.head()

# 항공사 컬럼 확인 후 처리
df['항공사'].value_counts()
'''
JNA      221
KAL      173
AAR      103
JJA      101
TWB       69
ESR       59
ABL       44
ASV       15
EOK       14
'''

airline = {
    'JNA': '진에어', 'KAL': '대한항공',
    'AAR': '아시아나', 'JJA': '제주항공',
    'TWB': '티웨이항공', 'ESR': '이스타항공',
    'ABL': '에어부산', 'ASV': '에어서울',
    'EOK': '에어로케이'
}

# 항공사 코드 -> 항공사명으로 변경
df['항공사'] = df['항공사'].replace(airline)
df['항공사'].value_counts()
'''
항공사
진에어      249
대한항공     197
아시아나     118
제주항공     115
티웨이항공     80
이스타항공     66
에어부산      50
에어서울      17
에어로케이     16
'''

# 이상치 확인
df.describe()

# 좌석수가 890000? 음 이상하다
# Boxplot으로 좌석수 이상치
plt.figure(figsize=(6, 5))
sns.boxplot(y=df['좌석수'])
plt.title('좌석수 이상치 확인')
plt.ylabel('좌석수')

plt.show()

# 확인해보니 이용률 = round(성인 / 좌석수 * 100, 2)
# 좌석수가 비정상적으로 큰 값 탐색
outliers = df[df['좌석수'] > 800000]
# 이상치 데이터 확인
outliers[['노선', '항공사', '좌석수', '성인', '이용률']] 

index = df[df['좌석수'] > 800000].index
df.loc[index, '좌석수'] = round(df.loc[index, '성인'] / (df.loc[index, '이용률'] / 100), 0)

# 다시 확인
plt.figure(figsize=(6, 5))
sns.boxplot(y=df['좌석수'])
plt.title('좌석수 이상치 확인')
plt.ylabel('좌석수')

plt.show()

# boxplot에는 이상치로 보이지만, 
# 대형 항공사 때문에 이상치로 보일 수 있는 것 같아 우선 남겨둠

# 유아도 이상치 2건 발생
# 유아 수 = 여객 수 - 성인인데 이 공식이 성립 X
plt.figure(figsize=(6, 5))
sns.boxplot(y=df['유아'])
plt.title('유아 이상치 확인')
plt.ylabel('유아')

plt.show()

outliers = df[df['유아'] > 20000]
# 이상치 데이터 확인
outliers[['노선', '항공사', '여객수', '좌석수', '성인', '유아']] 

# 이 데이터들도 다시 처리(유아 = 여객수 - 성인)
df = df[df['유아'] <= 20000].reset_index(drop=True)

# 다시 확인
plt.figure(figsize=(6, 5))
sns.boxplot(y=df['유아'])
plt.title('유아 이상치 확인')
plt.ylabel('유아')

plt.show()

# 이용률은 이용한 성인 수 대비 좌석수이므로
# 실제 여객수 대비 좌석수인 탑승률 계산
df['탑승률'] = round((df['여객수'] / df['좌석수']) * 100, 1)
df.info()
df['탑승률'].describe()

# 이상치 데이터 확인
outliers = df[df['탑승률'] > 200]
outliers

# 여객수가 왜 좌석수보다 많지? 다시 계산!
df.loc[df['탑승률'] > 200, '여객수'] = df['성인'] + df['유아']
df['탑승률'] = round((df['여객수'] / df['좌석수']) * 100, 1)
df['탑승률'].describe()

# 혹시 모르니 이거에 대해서도 처리(제거)
df = df[df['여객수'] <= df['좌석수']].reset_index(drop=True)

plt.figure(figsize=(6, 5))
sns.boxplot(y=df['탑승률'])
plt.title('탑승률 이상치 확인')
plt.ylabel('탑승률')

plt.show()

# 최종 데이터 저장
df.to_csv('./data/final_data.csv', index=False)
