import streamlit as st
import pandas as pd
import requests

# ---------------------------
# 환경변수(API 키) → Streamlit secrets.toml 에 저장 필수
# ---------------------------
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# ---------------------------
# Google Places API로 음식점 추천 가져오기
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
# 여행 데이터베이스
# ---------------------------
travel_data = {
    "일본": {
        "만족도": 4.7,
        "도시": {"도쿄": ["요코하마", "가마쿠라"], "오사카": ["교토", "고베"]},
        "불편한점": ["영어 소통 어려움", "교통비 비쌈", "현금 사용 비율 높음"],
        "위생": "전반적으로 청결하지만, 일부 오래된 식당에서는 위생 수준이 낮을 수 있음.",
        "문화": {
            "지켜야 하는 문화": ["전철에서 통화 금지", "쓰레기 분리수거 철저", "식사 전 '이타다키마스' 인사"],
            "일반 문화": ["온천 문화 발달", "만화·애니메이션 강국", "사케와 라멘 등 다양한 음식 문화"]
        }
    },
    "태국": {
        "만족도": 4.4,
        "도시": {"방콕": ["아유타야", "파타야"], "푸켓": ["피피섬", "팡아"]},
        "불편한점": ["더운 날씨", "교통 혼잡", "위생 문제"],
        "위생": "관광지 호텔·레스토랑은 위생적이나, 길거리 음식은 조심 필요.",
        "문화": {
            "지켜야 하는 문화": ["왕실 비판 금지", "사원 방문 시 복장 규칙 준수", "머리 쓰다듬기 금지"],
            "일반 문화": ["미소의 나라", "불교 문화 중심", "길거리 음식 다양함"]
        }
    },
    "베트남": {
        "만족도": 4.5,
        "도시": {"하노이": ["하롱베이", "닌빈"], "호치민": ["메콩델타", "붕따우"]},
        "불편한점": ["오토바이 교통 위험", "언어 장벽", "날씨 더움"],
        "위생": "대도시 관광지는 비교적 깨끗하지만, 노점 음식은 위생 문제 가능.",
        "문화": {
            "지켜야 하는 문화": ["호칭·예의 중시", "실내 신발 벗기", "호치민 존경"],
            "일반 문화": ["커피 문화 발달", "쌀국수(포) 유명", "시장 문화 활발"]
        }
    },
    "미국": {
        "만족도": 4.3,
        "도시": {"뉴욕": ["뉴저지", "보스턴"], "LA": ["샌디에이고", "라스베가스"]},
        "불편한점": ["팁 문화 부담", "총기 안전 문제", "물가 비쌈"],
        "위생": "대체로 위생적이나, 일부 지역 노숙자 문제 존재.",
        "문화": {
            "지켜야 하는 문화": ["식당 팁 문화 필수(15~20%)", "공공장소 흡연 금지", "개인 공간 존중"],
            "일반 문화": ["다민족 사회", "패스트푸드 발달", "스포츠 문화 (NBA, NFL) 강세"]
        }
    },
    "프랑스": {
        "만족도": 4.5,
        "도시": {"파리": ["베르사유", "몽생미셸"], "니스": ["칸", "모나코"]},
        "불편한점": ["소매치기 주의", "물가 비쌈", "프랑스어 소통 필요"],
        "위생": "식당 위생은 대체로 괜찮지만, 일부 공공 화장실은 불편할 수 있음.",
        "문화": {
            "지켜야 하는 문화": ["프랑스어 기본 인사 필수", "식사 예절 중시", "박물관 조용히 관람"],
            "일반 문화": ["와인과 치즈 문화", "패션 중심지", "예술과 건축의 나라"]
        }
    },
}

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="해외여행 추천 가이드", page_icon="🌍", layout="centered")
st.title("🌍 한국인 인기 해외여행 가이드")

country = st.selectbox("가고 싶은 나라를 선택하세요:", list(travel_data.keys()))

if country:
    data = travel_data[country]
    st.header(f"🇨🇭 {country} 여행 정보")

    # 만족도
    st.metric("여행 만족도 (5점 만점)", f"{data['만족도']}")

    # 도시 + 소도시
    st.subheader("📍 추천 도시 & 소도시")
    for city, small_cities in data["도시"].items():
        st.write(f"- **{city}** ➝ {', '.join(small_cities)}")

        # 음식점 추천
        with st.spinner(f"{city} 맛집 검색 중..."):
            restaurants = get_top_restaurants(city, "맛집", 3)
        st.write("🍽️ 추천 음식점 (Google 평점 기준)")
        for r in restaurants:
            st.write(f"   • {r}")

    # 불편한 점
    st.subheader("⚠️ 여행 시 불편한 점")
    for issue in data["불편한점"]:
        st.write(f"- {issue}")

    # 위생
    st.subheader("🧼 위생 정보")
    st.write(data["위생"])

    # 문화
    st.subheader("🎎 문화 정보")
    st.write("✅ **지켜야 하는 문화**")
    for rule in data["문화"]["지켜야 하는 문화"]:
        st.write(f"- {rule}")
    st.write("🌐 **일반 문화**")
    for c in data["문화"]["일반 문화"]:
        st.write(f"- {c}")

    # 만족도 비교 그래프
    st.subheader("📊 나라별 여행 만족도 비교")
    df = pd.DataFrame({
        "나라": list(travel_data.keys()),
        "만족도": [travel_data[c]["만족도"] for c in travel_data]
    })
    st.bar_chart(df.set_index("나라"))

st.write("---")
st.info("ℹ️ 음식점 평점 데이터는 Google Places API(또는 Naver 지도 API)를 통해 실시간으로 불러옵니다.\n"
        "Streamlit Cloud에서 실행 시, 반드시 `secrets.toml`에 API 키를 저장해야 합니다.")
