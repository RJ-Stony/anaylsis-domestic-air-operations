# ✈️ Domestic Air Operations Analysis

국내선 항공편 운항 데이터를 수집·정제하고,  
공항별/노선별 운항 추이를 시각화하는 Python 기반 분석 프로젝트입니다.

---

## 📁 프로젝트 구조

```
anaylsis-domestic-air-operations-main/
├── 1_concat.py           # ✅ 여러 CSV 파일을 하나로 병합
├── 2_preprocessing.py    # ✅ 결측치 제거, 컬럼 정리 등 전처리
├── 3_save_to_sql.py      # ✅ SQLite DB에 정제 데이터 저장
├── 4_visualization.py    # ✅ 공항별 운항량 시각화
├── result/               # 📊 시각화 결과 이미지 저장 폴더
├── .gitignore
└── README.md
```

---

## 🔍 분석 흐름

1. **데이터 통합**
   - `1_concat.py`  
     → 여러 연도 또는 월별 운항 실적 CSV를 하나의 DataFrame으로 병합

2. **데이터 전처리**
   - `2_preprocessing.py`  
     → 결측치 처리, 열 이름 정리, 숫자형 변환 등 클린징

3. **DB 저장**
   - `3_save_to_sql.py`  
     → 정제된 데이터를 SQLite로 저장하여 재사용 가능하게 구성

4. **시각화**
   - `4_visualization.py`  
     → pandas + matplotlib 기반 그래프 생성  
     → 공항별, 시간별, 노선별 운항 수 시각화

---

## 📦 사용 기술

- Python 3.12+
- pandas, matplotlib, sqlite3

---

## 💡 활용 가능성

- 국내선 수요 분석 및 예측
- 공항/노선별 트렌드 파악
- 지역별 항공 연결성 비교

---

## 📌 참고 사항

- 데이터는 공공데이터포털 등에서 수집된 것으로 가정
- `.csv` 파일은 `1_concat.py` 실행 전 동일한 경로에 준비되어 있어야 함
