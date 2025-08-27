import streamlit as st

# ---------------------------
# 나라 데이터 (문화/위생/특징)
# ---------------------------
country_data = {
    "일본 🇯🇵": {
        "문화": "대중교통에서 조용히 하기, 줄서기 엄격",
        "위생": "매우 청결, 쓰레기통 적음 (개인 수거 필요)"
    },
    "태국 🇹🇭": {
        "문화": "왕실 관련 발언 조심, 불교 사원에서 예의 지키기",
        "위생": "길거리 음식은 맛있지만 위생 편차 있음"
    },
    "베트남 🇻🇳": {
        "문화": "어른에게 존댓말, 두 손으로 물건 건네기",
        "위생": "오토바이 매연, 생수 권장"
    },
    "미국 🇺🇸": {
        "문화": "팁 문화 필수, 개인 공간 존중",
        "위생": "수돗물 염소 성분 있음 → 생수 선호"
    },
    "프랑스 🇫🇷": {
        "문화": "프랑스어 인사 필수, 카페 문화 존중",
        "위생": "물가 비싸고 수돗물 마실 수 있음"
    },
    "영국 🇬🇧": {
        "문화": "차 문화, 줄서기 문화 중요",
        "위생": "대체로 깨끗하나 비 오는 날 습기 많음"
    },
    "이탈리아 🇮🇹": {
        "문화": "천천히 즐기는 식사 문화, 패션 중시",
        "위생": "관광지 소매치기 주의"
    },
    "스페인 🇪🇸": {
        "문화": "시에스타(낮잠 문화), 느긋한 생활",
        "위생": "음식 위생 좋으나 밤늦게 식사"
    },
    "독일 🇩🇪": {
        "문화": "시간 엄수, 규칙 존중",
        "위생": "깨끗하고 정돈된 환경"
    },
    "호주 🇦🇺": {
        "문화": "자연 존중, 자유로운 분위기",
        "위생": "수돗물 마셔도 안전"
    },
    "캐나다 🇨🇦": {
        "문화": "다문화 존중, 예의 바른 대화",
        "위생": "깨끗하고 친환경적"
    },
    "중국 🇨🇳": {
        "문화": "큰 소리 대화 흔함, 가족 중심 문화",
        "위생": "대도시 스모그, 수돗물 비추천"
    },
}

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="🌍 해외여행 문화 가이드", page_icon="🧳", layout="centered")

st.markdown("<h1 style='text-align: center; color: #2C3E50;'>🌍 해외여행 문화 & 위생 가이드</h1>", unsafe_allow_html=True)
st.write("✈️ 여행 전, 나라별 문화를 배우고 위생 정보를 확인하세요!")

# 나라 선택 (라디오 버튼)
country = st.radio(
    "🌏 어느 나라를 원하시나요?",
    list(country_data.keys()),
    index=0,
    horizontal=False
)

# 선택된 나라 정보 출력
if country:
    info = country_data[country]

    st.markdown(f"<h2 style='color:#2980B9;'>📌 선택한 나라: {country}</h2>", unsafe_allow_html=True)

    # 문화 정보
    st.markdown("<h3 style='color:#27AE60;'>🎭 꼭 지켜야 하는 문화</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:18px;'>{info['문화']}</p>", unsafe_allow_html=True)

    # 위생 정보
    st.markdown("<h3 style='color:#E74C3C;'>🧼 위생 정보</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:18px;'>{info['위생']}</p>", unsafe_allow_html=True)

st.write("---")
st.info("💡 더 많은 나라를 원하시면 데이터베이스를 확장할 수 있습니다!")
