import streamlit as st
import pandas as pd
import requests
import os

# ---------------------------
# 환경변수(API 키)
# ---------------------------
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]  # Streamlit Cloud라면 secrets에 저장하세요

# ---------------------------
# 음식점 데이터 가져오기 (Google Places API)
# ---------------------------
def get_top_restaurants(city, keyword="restaurant", limit=3):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{city} {keyword}",
        "key": GOOGLE_API_KEY,
        "language": "ko"
    }
    response = requests.get(url, params=params).json()

    results = []
    if "results" in response:
        for r in response["results"][:limit]:
            name = r.get("name")
            rating = r.get("rating", "N/A")
            address = r.get("formatted_address", "")
            results.append(f"{name} (⭐{rating}) - {address}")
    return results

# ---------------------------
# 나라별 데이터
# ---------------------------
travel_data = {
    "일본": {
        "만족도": 4.7,
        "도시": {"도쿄": ["요코하마", "가마쿠라"], "오사카": ["교토", "고베"]},
        "불편한점": ["영어 소통 어려움", "교통비 비쌈", "현금 사용 비율 높음"]
    },
    "태국": {
        "만족도": 4.4,
        "도시": {"방콕": ["아유타야", "파타야"], "푸켓": ["피피섬", "팡아"]},
        "불편한점": ["더운 날씨", "교통 혼잡", "위생 문제"]
    },
    "베트남": {
        "만족도": 4.5,
        "도시": {"하노이": ["하롱베이", "닌빈"], "호치민": ["메콩델타", "붕따우"]},
        "불편한점": ["오토바이 교통 위험", "언어 장벽", "날씨 더움"]
    },
    "미국": {
        "만족도": 4.3,
        "도시": {"뉴욕": ["뉴저지", "보스턴"], "LA": ["샌디에이고", "라스베가스"]},
        "불편한점": ["팁 문화 부담", "총기 안전 문제", "물가 비쌈"]
    },
    "프랑스": {
        "만족도": 4.5,
        "도시": {"파리": ["베르사유", "몽생미셸"], "니스": ["칸", "모나코"]},
        "불편한점": ["소매치기 주의", "물가 비쌈", "프랑스어 소통 필요"]
    },
}

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="해외여행 추천 웹", page_icon="🌍", layout="centered")
st.title("🌍 한국인 인기 해외여행 추천 가이드 (실시간 음식점 평점 포함)")

country = st.selectbox("가고 싶은 나라를 선택하세요:", list(travel_data.keys()))

if country:
    data = travel_data[country]
    st.subheader(f"🇨🇭 {country} 여행 정보")

    # 만족도
    st.metric("여행 만족도 (5점 만점)", f"{data['만족도']}")

    # 도시 & 소도시
    st.write("📍 **추천 도시 & 소도시**")
    for city, small_cities in data["도시"].items():
        st.write(f"- **{city}** ➝ {', '.join(small_cities)}")

        # ---------------------------
        # 구글 API → 음식점 TOP3 가져오기
        # ---------------------------
        with st.spinner(f"{city} 맛집 검색 중..."):
            restaurants = get_top_restaurants(city, "맛집", 3)
        st.write("🍽️ **추천 음식점 (Google 평점 기준)**")
        for r in restaurants:
            st.write(f"   • {r}")

    # 불편한 점
    st.write("⚠️ **여행 시 불편한 점**")
    for issue in data["불편한점"]:
        st.write(f"- {issue}")

    # 만족도 비교 그래프
    st.subheader("📊 나라별 여행 만족도 비교")
    df = pd.DataFrame({
        "나라": list(travel_data.keys()),
        "만족도": [travel_data[c]["만족도"] for c in travel_data]
    })
    st.bar_chart(df.set_index("나라"))
