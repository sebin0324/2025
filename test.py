# app.py
# -*- coding: utf-8 -*-
"""
Streamlit 여행·문화 만족도 대시보드 (국가/도시/관광 카테고리)
- 설문 데이터 업로드 → 평균 점수/분포/국가 비교
- 개선 포인트 자동 제안
- 자유서술형 후기 자동 분류(불만 카테고리) & 요약
- 분석결과 다운로드 기능

데이터 예시 컬럼 (CSV/Excel):
- timestamp, country, city, category, hospitality, transport, cleanliness, value_for_money, attractions, overall, comment
  * 점수 컬럼은 1~5 리커트 척도 가정
"""

import io
import base64
import textwrap
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# =============== 기본 설정 ===============
st.set_page_config(
    page_title="여행·문화 만족도 대시보드",
    page_icon="🌏",
    layout="wide",
)

st.title("🌏 여행·문화 만족도 대시보드")
st.caption("업로드한 설문 데이터를 바탕으로 평균 점수, 개선 포인트, 불만 자동 분류/요약을 제공합니다.")

# =============== 유틸 함수 ===============

def _to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")

@st.cache_data(show_spinner=False)
def load_sample() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 220
    countries = ["대한민국", "일본", "태국", "프랑스", "스페인", "미국"]
    cities = {
        "대한민국": ["서울", "부산", "제주"],
        "일본": ["도쿄", "오사카", "교토"],
        "태국": ["방콕", "치앙마이"],
        "프랑스": ["파리", "니스"],
        "스페인": ["바르셀로나", "마드리드"],
        "미국": ["뉴욕", "라스베이거스"],
    }
    categories = ["역사/문화", "자연/휴양", "쇼핑", "미식", "축제/공연"]
    comments_pool = [
        "대중교통 연결이 불편했어요",
        "물가가 생각보다 너무 비쌌습니다",
        "길거리 청결 상태가 아쉬워요",
        "현지인들이 아주 친절했어요",
        "관광지가 너무 붐벼서 제대로 못 봤어요",
        "박물관이 훌륭했고 설명도 잘 되어 있습니다",
        "영어가 잘 안 통했어요",
        "치안이 불안해서 밤에 돌아다니기 무서웠어요",
        "음식이 정말 맛있고 가성비도 좋았습니다",
        "공항에서 시내까지 이동이 번거로웠어요",
        "축제가 인상적이었지만 화장실이 부족했어요",
        "날씨가 너무 더워서 이동이 힘들었어요",
        "비가 많이 와서 관광이 제한됐어요",
        "와이파이가 잘 안 터져요",
    ]
    rows = []
    for i in range(n):
        ctry = rng.choice(countries)
        row = {
            "timestamp": pd.Timestamp("2025-07-01") + pd.to_timedelta(int(rng.integers(0, 31)), unit="D"),
            "country": ctry,
            "city": rng.choice(cities[ctry]),
            "category": rng.choice(categories),
            "hospitality": int(rng.integers(2, 6)),
            "transport": int(rng.integers(1, 6)),
            "cleanliness": int(rng.integers(1, 6)),
            "value_for_money": int(rng.integers(1, 6)),
            "attractions": int(rng.integers(1, 6)),
            "overall": int(rng.integers(1, 6)),
            "comment": rng.choice(comments_pool) if rng.random() < 0.9 else "",
        }
        rows.append(row)
    return pd.DataFrame(rows)


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    expected = [
        "timestamp","country","city","category",
        "hospitality","transport","cleanliness","value_for_money","attractions","overall",
        "comment"
    ]
    missing = [c for c in expected if c not in df.columns]
    if missing:
        st.error(f"누락된 컬럼이 있습니다: {missing}\n다음 예시 스키마를 참고하세요: {expected}")
        st.stop()
    # 타입 정리
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    score_cols = ["hospitality","transport","cleanliness","value_for_money","attractions","overall"]
    for c in score_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["country","city","category","comment"]:
        if c in df:
            df[c] = df[c].fillna("").astype(str)
    return df

# 간단 한국어/일상 키워드 사전 기반 카테고리 분류 (여행 도메인)
CATEGORY_KEYWORDS = {
    "교통/이동": ["교통", "대중교통", "환승", "연결", "이동", "공항"],
    "물가/가성비": ["비싸", "물가", "가성비", "가격"],
    "청결/환경": ["청결", "더럽", "쓰레기", "위생"],
    "친절/서비스": ["친절", "불친절", "응대", "서비스"],
    "혼잡/대기": ["붐벼", "혼잡", "줄", "대기"],
    "언어/의사소통": ["영어", "의사소통", "언어", "통역"],
    "치안/안전": ["치안", "안전", "무섭", "소매치기"],
    "관광지 품질": ["박물관", "전시", "관광지", "명소", "공연", "축제"],
    "날씨/기후": ["날씨", "더워", "추워", "비", "폭우"],
    "통신/인터넷": ["와이파이", "인터넷", "데이터", "신호"],
    "음식/미식": ["맛", "음식", "레스토랑", "미식"],
}

NEGATIVE_HINTS = [
    "불편", "아쉽", "문제", "최악", "별로", "다신", "실망", "불만", "짜증", "화남",
    "불친절", "느려", "늦", "더럽", "시끄럽", "비싸", "부족", "붐벼", "위험",
]

POSITIVE_HINTS = ["좋았", "만족", "친절", "깨끗", "최고", "추천", "편리", "안전"]


def classify_comment(text: str) -> list:
    text = (text or "").lower()
    cats = []
    for cat, kws in CATEGORY_KEYWORDS.items():
        for k in kws:
            if k in text:
                cats.append(cat)
                break
    return cats or (["기타"] if text.strip() else [])


def sentiment_rule(text: str) -> str:
    text = (text or "").lower()
    pos = any(k in text for k in POSITIVE_HINTS)
    neg = any(k in text for k in NEGATIVE_HINTS)
    if neg and not pos:
        return "부정"
    if pos and not neg:
        return "긍정"
    if pos and neg:
        return "혼합"
    return "중립"


def summarize_top_issues(df_comments: pd.DataFrame, top_k: int = 3) -> str:
    # 카테고리별 건수 상위 + 대표 의견 예시
    if df_comments.empty:
        return "요약할 댓글이 없습니다."
    counts = (
        df_comments.explode("categories")["categories"].value_counts().drop(labels=[""], errors="ignore")
    )
    bullets = []
    for cat, cnt in counts.head(top_k).items():
        if pd.isna(cat):
            continue
        sample = (
            df_comments[df_comments["categories"].apply(lambda x: cat in (x or []))]
            .sort_values("sentiment", ascending=True)
            ["comment"]
            .head(2)
            .tolist()
        )
        examples = " / ".join([textwrap.shorten(s, width=60, placeholder="...") for s in sample])
        bullets.append(f"• **{cat}**: {cnt}건 — 예: {examples}")
    if not bullets:
        return "뚜렷한 불만 카테고리가 식별되지 않았습니다."
    return "\n".join(bullets)


def improvement_suggestions(mean_scores: pd.Series, threshold: float = 3.5) -> list:
    tips = {
        "hospitality": "관광안내소/가이드 교육 강화, 안내 표지 다국어화",
        "transport": "공항-도심 연계 강화, 환승 안내 개선",
        "cleanliness": "핵심 관광지 청소 주기 상향 및 쓰레기통 확충",
        "value_for_money": "시티패스/통합권 제공, 무료 프로그램 확대",
        "attractions": "설명 품질 개선, 큐레이션/타임슬롯 도입으로 체류 경험 향상",
        "overall": "여행자 여정(Journey) 전반의 병목 점검",
    }
    out = []
    for k, v in mean_scores.items():
        if k in tips and v < threshold:
            out.append(f"- {k} 평균 {v:.2f}점 → 제안: {tips[k]}")
    return out or ["임계값 미만 항목이 없습니다. 전반적으로 양호합니다."]

# =============== 사이드바: 데이터 입력 ===============
st.sidebar.header("데이터 입력")
mode = st.sidebar.radio("데이터 소스", ["샘플 데이터 사용", "파일 업로드(CSV/Excel)"])

df: pd.DataFrame
if mode == "샘플 데이터 사용":
    df = load_sample()
else:
    up = st.sidebar.file_uploader("설문 파일 업로드", type=["csv", "xlsx", "xls"])
    if up is None:
        st.info("샘플을 보거나, 파일을 업로드하세요.")
        df = load_sample()
    else:
        if up.name.endswith(".csv"):
            df = pd.read_csv(up)
        else:
            df = pd.read_excel(up)

# 정제 & 체크
df = ensure_columns(df)

# 필터
st.sidebar.subheader("필터")
country_sel = st.sidebar.multiselect("국가 선택", sorted(df["country"].unique()), default=list(sorted(df["country"].unique())))
city_sel = st.sidebar.multiselect("도시 선택", sorted(df["city"].unique()), default=list(sorted(df["city"].unique())))
cat_sel = st.sidebar.multiselect("카테고리 선택", sorted(df["category"].unique()), default=list(sorted(df["category"].unique())))

mask = df["country"].isin(country_sel) & df["city"].isin(city_sel) & df["category"].isin(cat_sel)
df_f = df.loc[mask].copy()

st.markdown(f"**표본 수:** {len(df_f)}건  |  기간: {df_f['timestamp'].min().date()} ~ {df_f['timestamp'].max().date()}")

# =============== 요약 카드 ===============
score_cols = ["hospitality","transport","cleanliness","value_for_money","attractions","overall"]
means = df_f[score_cols].mean(numeric_only=True)
cols = st.columns(len(score_cols))
labels = {
    "hospitality": "친절도",
    "transport": "교통 편의",
    "cleanliness": "청결",
    "value_for_money": "가성비",
    "attractions": "관광지 매력",
    "overall": "종합만족",
}
for i, c in enumerate(score_cols):
    with cols[i]:
        st.metric(label=labels[c], value=f"{means[c]:.2f} / 5")

# =============== 차트 ===============
with st.expander("점수 분포 및 국가/도시 비교 차트", expanded=True):
    # 항목별 평균 막대
    fig1, ax1 = plt.subplots()
    ax1.bar([labels[c] for c in score_cols], [means[c] for c in score_cols])
    ax1.set_ylim(0,5)
    ax1.set_ylabel("평균 점수")
    ax1.set_title("항목별 평균 점수")
    st.pyplot(fig1)

    # 국가별 overall 평균
    by_country = df_f.groupby("country")["overall"].mean().sort_values(ascending=False)
    fig2, ax2 = plt.subplots()
    ax2.bar(by_country.index, by_country.values)
    ax2.set_ylim(0,5)
    ax2.set_title("국가별 종합만족 평균")
    st.pyplot(fig2)

    # 도시별 overall 상위 10
    by_city = df_f.groupby("city")["overall"].mean().sort_values(ascending=False).head(10)
    fig3, ax3 = plt.subplots()
    ax3.bar(by_city.index, by_city.values)
    ax3.set_ylim(0,5)
    ax3.set_title("도시 TOP10 종합만족 평균")
    st.pyplot(fig3)

    # overall 히스토그램
    fig4, ax4 = plt.subplots()
    ax4.hist(df_f["overall"].dropna(), bins=5, range=(1,6))
    ax4.set_title("종합만족 분포")
    st.pyplot(fig4)

# =============== 개선 포인트 ===============
st.subheader("🛠️ 개선 포인트 제안")
th = st.slider("개선 임계값 (미만 항목 제안)", 1.0, 5.0, 3.5, 0.1)
for tip in improvement_suggestions(means, threshold=th):
    st.write(tip)

# =============== 텍스트 분석 ===============
st.subheader("🧠 후기 자동 분류 & 요약")

# 코멘트 전처리
c_df = df_f[["comment"]].copy()
c_df["comment"] = c_df["comment"].fillna("")
c_df = c_df[c_df["comment"].str.strip() != ""].copy()

if c_df.empty:
    st.info("후기 텍스트가 없습니다. 샘플 데이터를 사용하거나 코멘트를 포함해 업로드하세요.")
else:
    c_df["categories"] = c_df["comment"].apply(classify_comment)
    c_df["sentiment"] = c_df["comment"].apply(sentiment_rule)

    colA, colB = st.columns([1,1])
    with colA:
        st.markdown("**감성 분포**")
        sent_counts = c_df["sentiment"].value_counts()
        fig5, ax5 = plt.subplots()
        ax5.bar(sent_counts.index, sent_counts.values)
        ax5.set_title("감성(긍정/부정/혼합/중립) 분포")
        st.pyplot(fig5)

    with colB:
        st.markdown("**카테고리 TOP5**")
        cat_counts = c_df.explode("categories")["categories"].value_counts().head(5)
        fig6, ax6 = plt.subplots()
        ax6.bar(cat_counts.index, cat_counts.values)
        ax6.set_title("불만/이슈 카테고리 상위")
        st.pyplot(fig6)

    st.markdown("**요약 (상위 이슈 & 예시)**")
    st.markdown(summarize_top_issues(c_df, top_k=5))

    with st.expander("분석 테이블 보기"):
        st.dataframe(c_df.reset_index(drop=True))

# =============== 다운로드 ===============
with st.expander("결과 다운로드"):
    st.download_button("현재 필터링된 데이터 CSV 다운로드", data=_to_csv_bytes(df_f), file_name="filtered_survey.csv", mime="text/csv")

# =============== 푸터 ===============
st.caption("키워드 사전 기반 규칙 분류이므로 100% 정확하지 않을 수 있습니다. 실제 운영 시 사전 튜닝 또는 모델 연동을 권장합니다.")

# ---------------- requirements.txt (참고) ----------------
# streamlit==1.37.0
# pandas==2.2.2
# numpy==1.26.4
# matplotlib==3.8.4
