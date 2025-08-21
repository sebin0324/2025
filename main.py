import streamlit as st

# --- 1. 앱 기본 설정 ---
st.set_page_config(page_title="MBTI 진로교육", page_icon="🎓", layout="centered")

# --- 2. 홈 화면 ---
st.title("🎓 MBTI 기반 진로교육 사이트")
st.write("자신의 성격 유형을 알아보고, 적합한 진로를 추천받아 보세요!")

if st.button("검사 시작하기"):
    st.session_state.page = "test"

# --- 3. MBTI 테스트 ---
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "test":
    st.header("📝 MBTI 검사")
    
    questions = [
        ("사람들과 함께 있을 때 에너지를 얻는다.", "E"),
        ("아이디어보다는 사실과 데이터가 중요하다.", "S"),
        ("결정을 내릴 때 감정보다 논리를 중시한다.", "T"),
        ("계획대로 진행하는 것을 선호한다.", "J"),
    ]
    
    answers = {}
    for q, dim in questions:
        answers[q] = st.radio(q, ["전혀 아니다", "아니다", "보통이다", "그렇다", "매우 그렇다"])
    
    if st.button("결과 확인"):
        st.session_state.page = "result"
        st.session_state.answers = answers

# --- 4. 결과 페이지 ---
if st.session_state.page == "result":
    st.header("✨ 검사 결과")
    st.write("당신의 MBTI 유형은 **ENFP** 입니다!")  # 여기서는 임시 하드코딩
    
    st.subheader("🔍 추천 진로")
    st.write("- 마케팅/광고 기획자")
    st.write("- 창업가, 스타트업")
    st.write("- 교육/상담 분야")
    
    st.download_button("📄 결과 리포트 다운로드", "ENFP - 추천 진로 리포트", "report.txt")
