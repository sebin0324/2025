import streamlit as st

# 앱 제목
st.set_page_config(page_title="e스포츠 올인원 웹앱", page_icon="🏆", layout="wide")

st.title("🏆 e스포츠 올인원 웹앱")
st.markdown("📊 **데이터 분석** + 🧩 **참여형 콘텐츠**를 한 곳에서 즐겨보세요!")

# 사이드바 메뉴
menu = st.sidebar.radio(
    "메뉴 선택",
    ["홈", "데이터 대시보드", "참여형 콘텐츠"]
)

# 홈 화면
if menu == "홈":
    st.header("✨ 환영합니다!")
    st.markdown(
        """
        이 앱은 e스포츠 정보를 **데이터 시각화**와  
        **참여형 게임/테스트**로 제공합니다 🎮  
        
        👉 왼쪽 메뉴에서 원하는 기능을 선택해보세요!
        """
    )

# 데이터 대시보드
elif menu == "데이터 대시보드":
    st.header("📊 e스포츠 데이터 대시보드")
    tab1, tab2, tab3 = st.tabs(["팀/리그 통계", "선수 스탯", "메타 트렌드"])
    
    with tab1:
        st.subheader("리그/팀 순위")
        st.info("여기에 팀 순위표와 승률 그래프가 들어갑니다.")
    
    with tab2:
        st.subheader("선수 스탯 조회")
        player = st.text_input("선수 이름을 입력하세요", "")
        if player:
            st.success(f"{player} 선수의 최근 경기 기록과 스탯을 보여줍니다.")
    
    with tab3:
        st.subheader("메타 트렌드")
        st.info("최근 픽률/밴률 TOP 10 챔피언 그래프가 표시됩니다.")

# 참여형 콘텐츠
elif menu == "참여형 콘텐츠":
    st.header("🧩 참여형 콘텐츠")
    tab1, tab2, tab3 = st.tabs(["MBTI 포지션 테스트", "e스포츠 퀴즈", "스트리머 랭킹"])
    
    with tab1:
        st.subheader("MBTI 포지션 테스트")
        st.info("여기에 질문지와 결과 화면이 들어갑니다.")
    
    with tab2:
        st.subheader("e스포츠 퀴즈 게임")
        st.info("퀴즈 문제와 점수 시스템이 들어갑니다.")
    
    with tab3:
        st.subheader("실시간 스트리머 랭킹")
        st.info("Twitch/YouTube API를 연결해 스트리머 순위를 보여줄 수 있습니다.")

