import streamlit as st
import random

# ---------------------------
# 퀴즈 데이터 (나라별 특징 기반)
# ---------------------------
quiz_data = [
    {
        "question": "🇯🇵 일본에서 지켜야 하는 문화로 옳은 것은?",
        "options": ["대중교통에서 큰 소리로 통화하기", "줄 서기 엄격히 지키기", "길거리 흡연 자유"],
        "answer": "줄 서기 엄격히 지키기"
    },
    {
        "question": "🇹🇭 태국에서 절 방문 시 올바른 행동은?",
        "options": ["민소매와 반바지 착용 가능", "왕실 비하 금지", "머리 쓰다듬기 허용"],
        "answer": "왕실 비하 금지"
    },
    {
        "question": "🇻🇳 베트남의 대표 음식은?",
        "options": ["스시", "쌀국수", "햄버거"],
        "answer": "쌀국수"
    },
    {
        "question": "🇺🇸 미국에서 꼭 지켜야 하는 문화는?",
        "options": ["팁 문화 지키기", "노상 흡연 자유", "총기 자유 사용"],
        "answer": "팁 문화 지키기"
    },
    {
        "question": "🇫🇷 프랑스의 대표적인 문화는?",
        "options": ["사원 방문 시 신발 벗기", "카페 문화와 예술", "전통 온천 문화"],
        "answer": "카페 문화와 예술"
    },
]

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="여행 문화 퀴즈", page_icon="🧳", layout="centered")

st.title("🧳 해외여행 문화 퀴즈")
st.write("✈️ 각 나라별 문화와 예절을 퀴즈 형식으로 배워보세요!")

# 무작위 문제 선택
quiz = random.choice(quiz_data)
st.subheader(quiz["question"])

# 보기 선택
choice = st.radio("정답을 선택하세요:", quiz["options"])

# 버튼 눌러서 확인
if st.button("정답 확인"):
    if choice == quiz["answer"]:
        st.success("✅ 정답입니다! 멋져요 🎉")
    else:
        st.error(f"❌ 오답입니다. 정답은 👉 **{quiz['answer']}** 입니다!")
