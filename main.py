import streamlit as st

# 🌟 앱 기본 설정
st.set_page_config(page_title="🌈 MBTI 진로교육 🎓", page_icon="🦄", layout="centered")

# 🎨 스타일 (커스텀 CSS)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%);
        color: #333;
        font-family: "Comic Sans MS", cursive, sans-serif;
    }
    .title {
        font-size: 40px !important;
        color: #ff4b5c;
        text-align: center;
    }
    .subtitle {
        font-size: 20px !important;
        color: #444;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 🏠 홈 화면
st.markdown('<p class="title">🌈✨ MBTI 기반 진로교육 🎓🚀</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">당신의 성격유형을 찾고 🔍✨ 적합한 진로를 발견하세요! 🌸🦄</p>', unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=150)
    if st.button("🌟 검사 시작하기 📝"):
        st.session_state.page = "test"

# 📝 MBTI 검사 화면
if st.session_state.page == "test":
    st.markdown("## 📝 MBTI 검사 시작 🎯")
    st.write("솔직하게 답변해주세요! 💡✨")

    questions = [
        ("👥 사람들과 함께 있을 때 에너지를 얻는다 🌟", "E"),
        ("📊 아이디어보다는 사실과 데이터가 중요하다 📚", "S"),
        ("⚖️ 결정을 내릴 때 감정보다 논리를 중시한다 🧠", "T"),
        ("📅 계획대로 진행하는 것을 선호한다 ⏳", "J"),
    ]

    answers = {}
    for q, dim in questions:
        answers[q] = st.radio(q, ["😡 전혀 아니다", "🙁 아니다", "😐 보통이다", "🙂 그렇다", "🤩 매우 그렇다"])

    if st.button("✨ 결과 확인하기 🎉"):
        st.session_state.page = "result"
        st.session_state.answers = answers

# 🎉 결과 화면
if st.session_state.page == "result":
    st.markdown("## ✨ 검사 결과 🎊")
    st.success("🌈 당신의 MBTI 유형은 **ENFP 🦄✨🌸** 입니다!")
    
    st.markdown("### 🔮 추천 진로 🌟")
    st.write("💼 마케팅/광고 기획자 📢")
    st.write("🚀 창업가, 스타트업 CEO 👩‍💻")
    st.write("🎓 교육/상담 분야 🧑‍🏫")
    st.write("🎭 크리에이티브 아티스트 🎨")

    st.balloons()  # 🎈 풍선 효과
    st.snow()      # ❄️ 눈 효과
    
    st.download_button("📄 결과 리포트 다운로드 📝", "ENFP - 추천 진로 리포트", "report.txt")
    if st.button("🏠 처음으로 돌아가기 🔄"):
        st.session_state.page = "home"
