#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler

COLOR_CODE = ["#2364aa", "#3da5d9", "#73bfb8", "#fec601", "#ea7317"]
def set_common_style():
        
    mpl.rcParams.update({
        # [폰트 관련]
        'font.family': 'Arial',             # 글꼴 종류
        'font.size': 15,                    # 기본 폰트 크기

        # [축 관련]
        'axes.grid': False,                  # 기본 그리드 표시 여부
        'grid.linestyle': '--',             # 그리드 스타일
        'grid.alpha': 0.5,                  # 그리드 투명도

        # [눈금 설정]
        'xtick.direction': 'out',            # 눈금 안쪽으로
        'ytick.direction': 'out',

        # [범례]
        'legend.frameon': False,            # 범례 박스 제거
        'legend.loc': 'best',               # 범례 위치 자동
        'legend.edgecolor': 'none',         # 범례 테두리 색

        # [Figure 설정]
        'figure.figsize': (6, 4),           # 기본 figure 크기 (inches)
        'figure.dpi': 300,                  # 디스플레이 해상도
        'savefig.dpi': 300,                 # 저장 해상도
        'savefig.transparent': True,        # 저장 시 투명 배경
        'savefig.bbox': 'tight',            # 저장 시 여백 최소화

        # [PDF/PS 설정]
        'pdf.fonttype': 42,                 # 벡터화 폰트 유지
        'ps.fonttype': 42,
        
        "axes.prop_cycle": cycler('color', COLOR_CODE)
    })

set_common_style()

# 데이터 불러오기
df = pd.read_csv('Country-Corrected_Marine_Waste_Metadata.csv', encoding='latin1')

# 국가별 논문 수 집계
country_counts = df['Country'].value_counts()

# 그래프 그리기
plt.figure(figsize=(10, 8), dpi=300)
plt.barh(country_counts.index, country_counts.values)
plt.xlabel('Number of Papers')
plt.ylabel('Country')
plt.title('Number of Papers by Country')
plt.tight_layout()
plt.show()

#%%
import numpy as np
# 국가별 논문 수 집계 → 상위 10개
country_counts = df['Country'].value_counts()[:20]
countries = country_counts.index.tolist()
counts = country_counts.values.tolist()
y_pos = range(len(countries))

norm = plt.Normalize(0, 20-1)   # counts를 0~1로 정규화
cmap = plt.cm.Blues_r

# 그래프 생성
fig, ax = plt.subplots(figsize=(8, 7))

# 왼쪽 방향 화살표만 그림
for i, val in enumerate(counts):
    color = cmap(i / (20 - 1))
    ax.plot(val, i, marker='>', color=color, markersize=12, markeredgecolor='black', markeredgewidth=0.5)  # 왼쪽 방향 삼각형
    ax.text(val+7, i, str(val), va='center', ha='left')

plt.barh(country_counts.index, country_counts.values, height =0.05, color = 'grey')

# y축에 국가명 붙이기
ax.set_yticks(y_pos)
ax.set_yticklabels(countries)
ax.set_xlim([0,290])

# x축 라벨
ax.set_xlabel('Number of Publications')

# 그래프 정리
plt.tight_layout()
plt.savefig('country.png')
plt.show()

# %%
# 'Research Areas' 컬럼 전처리
df_area = df.dropna(subset=['Research Areas'])
df_area = df_area.assign(
    AreaList=df_area['Research Areas'].str.split(',\s*|;\s*')
).explode('AreaList')
df_area['AreaList'] = df_area['AreaList'].str.strip()


area_counts = df_area['AreaList'].value_counts().head(15)
areas = area_counts.index[::-1]   # 큰 값이 위로 오게 역순
counts = area_counts.values[::-1]

# 색상 매핑 준비
norm = plt.Normalize(0, len(areas)-1)
cmap = plt.cm.Greens  # 색맵 종류 선택

# 그래프 생성
fig, ax = plt.subplots(figsize=(10, 6))

# 막대를 "왼쪽으로" 그리기 위해 음수 부호 붙이기
for i, (area, count) in enumerate(zip(areas, counts)):
    color = cmap(i / (len(areas) - 1))
    ax.barh(area, -count, color=color, edgecolor = 'k', linewidth = 0.5)
    
# x축 방향 반대로 설정
ax.set_xlim(-area_counts.max()*1.1, 0)

# x축 라벨 → 양수로 표시되도록
xlabels = [int(abs(tick)) for tick in ax.get_xticks()]
ax.set_xticklabels(xlabels)

ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

# 레이블
ax.set_xlabel('Number of Papers')
ax.set_title('Top 15 Research Areas (Leftward Bars)')
ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")
plt.tight_layout()
plt.savefig('area.png')
plt.show()