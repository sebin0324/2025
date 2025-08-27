import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# 샘플 데이터 (실제 API나 DB로 대체 가능)
# ---------------------------
country_data = {
    "일본": {"만족도": 4.7, "추천지": ["도쿄", "오사카", "교토", "후쿠오카"]},
    "프랑스": {"만족도": 4.5, "추천지": ["파리", "니스", "리옹", "보르도"]},
    "이탈리아": {"만족도": 4.6, "추천지": ["로마", "피렌체", "밀라노", "베네치아"]},
    "태국": {"만족도": 4.4, "추천지": ["방콕", "푸켓", "치앙마이", "파타야"]},
    "미국": {"만족도": 4.3, "추천지": ["뉴욕", "라스베가스", "샌프란시스코", "마이애미"]},
    "스페인": {"만족도": 4.5, "추천지": ["바르셀로나", "마드리드", "세비야", "발렌시아"]},
}

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="해외여행 추천 웹", page_icon="🌍", layout="centered")

st.title("🌍 해외여행 만족도 & 여행지 추천")
st.write("✈️ 가고 싶은 나라를 선택하면 여행 만족도와 추천 여행지를 알려드려요!")

# 나라 선택
country = st.selectbox("가고 싶은 나라를 골라보세요:", list(country_data.keys()))

if country:
    st.subheader(f"🇨🇭 {country} 여행 정보")

    # 만족도 출력
    rating = country_data[country]["만족도"]
    st.metric(label="여행 만족도 (5점 만점)", value=f"{rating}")

    # 추천 여행지 리스트
    st.write("📍 추천 여행지:")
    for place in country_data[country]["추천지"]:
        st.write(f"- {place}")

    # 만족도 시각화 (비교 그래프)
    st.subheader("📊 나라별 여행 만족도 비교")
    df = pd.DataFrame({
        "나라": list(country_data.keys()),
        "만족도": [country_data[c]["만족도"] for c in country_data]
    })

    fig, ax = plt.subplots()
    ax.bar(df["나라"], df["만족도"])
    ax.set_ylabel("만족도 (5점 만점)")
    ax.set_title("나라별 여행 만족도")
    st.pyplot(fig)

st.write("---")
st.info("💡 실제 데이터를 연결하면 더 현실적인 여행 추천 시스템을 만들 수 있어요! 🌏")
