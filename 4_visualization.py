"""
시각화 진행
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 표기
from matplotlib import font_manager, rc
import matplotlib.ticker as ticker
import platform

if platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
else:
    print('Check your OS system')

df = pd.read_csv('./data/final_data.csv')
df.info()

# --- 항공 노선별 여객 수 및 이용률 분석 ---

# 노선별로 총 여객수를 집계
route = df.groupby('노선')['여객수'].sum().sort_values(ascending=False)

# 노선별 평균 이용률 계산
mean_use_rate = df.groupby('노선')['이용률'].mean().sort_values(ascending=False)
top10_routes = route.head(10)
bottom10_routes = route.tail(10)

# Top 10 노선 여객 수
plt.figure(figsize=(12,6))
ax = top10_routes.plot(kind='bar', color='cornflowerblue')
plt.title('국내 항공 노선별 총 여객 수 (Top 10)')
plt.xlabel('노선')
plt.ylabel('총 여객 수')
plt.xticks(rotation=0)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/1e6:.0f}M'))
plt.grid(axis='y')
plt.show()

# Bottom 10개 노선 여객 수
plt.figure(figsize=(12, 6))
bottom10_routes.plot(kind='bar', color='lightcoral')
plt.title('국내 항공 노선별 총 여객 수 (Bottom 10)')
plt.xlabel('노선')
plt.ylabel('총 여객 수')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.show()

# 상위 5개 노선의 여객 수 비율
top5_routes = route.head(5)
plt.figure(figsize=(8, 8))
plt.pie(top5_routes, labels=top5_routes.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'), startangle=180)
plt.title('국내 항공 여객 수 Top 5 노선 비율')
plt.show()

# 노선별 월별 이용률
top10_routes = route.head(10).index
filter_df = df[df['노선'].isin(top10_routes)].pivot_table(index='노선', columns='월', values='이용률', aggfunc='mean')
plt.figure(figsize=(10, 6))
sns.heatmap(filter_df, cmap='coolwarm', annot=True, 
            fmt='.1f', linewidths=0.5)
plt.title('노선별 월별 평균 이용률 (Top 10)')
plt.xlabel('월')
plt.ylabel('노선')
plt.show()

# 인기 노선 월별 여객 수 변화
popular = ['김포-제주', '김해-제주']
df_filtered = df[df['노선'].isin(popular)]
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_filtered, x='월', y='여객수', hue='노선',
             marker='o')
plt.title('인기 노선 월별 여객 수 변화')
plt.xlabel('월')
plt.ylabel('여객 수')
plt.grid(True)
plt.show()

# 노선별 총 여객 수 vs 평균 이용률
plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(x=route, y=mean_use_rate, 
                          hue=mean_use_rate, palette='coolwarm', 
                          size=route, sizes=(20, 200), 
                          edgecolor='black')
plt.xscale('log')
plt.title("노선별 총 여객 수 vs 평균 이용률")
plt.xlabel("총 여객 수")
plt.ylabel("평균 이용률 (%)")
plt.grid(True, linestyle="--", linewidth=0.5)
plt.show()

# 출발 공항과 도착 공항별 평균 탑승률 계산
group_data = df.groupby(['출발', '도착'])['탑승률'].mean().reset_index()
heat_pivot = group_data.pivot(index='출발', columns='도착', values='탑승률')
heat_pivot = heat_pivot.sort_index(axis=0).sort_index(axis=1)

plt.figure(figsize=(12, 8))
sns.heatmap(heat_pivot, annot=True, fmt='.1f', cmap='YlGnBu')
plt.title('출발 & 도착 공항별 평균 탑승률')
plt.xlabel('도착 공항')
plt.ylabel('출발 공항')
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.show()

# 월별, 항공사별 평균 탑승률 계산
group_airline = df.groupby(['월', '항공사'])['탑승률'].mean().reset_index()

plt.figure(figsize=(12, 8))
sns.lineplot(data=group_airline, x='월', y='탑승률',
             hue='항공사', marker='o', linewidth=2)
plt.title('월별 항공사별 평균 탑승률 변화', fontsize=16)
plt.xlabel('월', fontsize=14)
plt.ylabel('평균 탑승률 (%)', fontsize=14)
plt.xticks(range(1, 9))
plt.legend(title='항공사', fontsize=10, title_fontsize=12, ncol=2)
plt.grid(True, linestyle='-.', alpha=0.6)
plt.tight_layout()
plt.show()
